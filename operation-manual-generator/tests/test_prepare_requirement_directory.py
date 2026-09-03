import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/prepare_requirement_directory.py"
spec = importlib.util.spec_from_file_location("prepare_requirement_directory", SCRIPT)
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


class PrepareSourcesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def write(self, name, text="# 页面\n\n操作事实。\n"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def run_script(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                                cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def manifest(self, directory):
        return json.loads((directory / ".operation-manual-manifest.json").read_text())

    def test_conventional_directory_excludes_derived_documents(self):
        source = self.write("legacy/primary/PRD.md")
        self.write("legacy/primary/PRD.localized.md")
        self.write("legacy/primary/output/generated.md")
        self.write("legacy/primary/images/notes.md")
        self.write("legacy/reference/background.md")
        self.run_script(self.root / "legacy")
        data = self.manifest(self.root / "legacy")
        self.assertEqual(data["input_mode"], "directory")
        self.assertEqual((data["primary_count"], data["reference_count"]), (1, 1))
        self.assertEqual(data["primary"][0]["effective_path"], str(source))
        self.assertEqual(data["primary"][0]["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())

    def test_single_file_uses_original_source_and_selected_output(self):
        source = self.write("external/已确认 PRD.md")
        output = self.root / "manual/output"
        before = source.read_bytes()
        self.run_script(source, "--output-dir", output)
        data = self.manifest(output)
        self.assertEqual(data["input_mode"], "files")
        self.assertEqual(data["primary"][0]["source_path"], str(source))
        self.assertEqual(data["primary"][0]["effective_path"], str(source))
        self.assertEqual(source.read_bytes(), before)
        self.assertFalse((source.parent / "primary").exists())
        self.assertFalse((source.parent / "reference").exists())

    def test_explicit_multiple_sources_without_requirement_directory(self):
        prd = self.write("03-PRD/最终 PRD.md")
        supplement = self.write("03-PRD/补充信息.md")
        reference = self.write("参考资料/说明.md")
        output = self.root / "08_已上线需求/需求/output"
        self.run_script("--primary", prd, "--primary", supplement, "--primary", prd,
                        "--reference", reference, "--output-dir", output)
        data = self.manifest(output)
        self.assertEqual(data["primary_count"], 2)
        self.assertEqual(data["reference_count"], 1)
        self.assertIsNone(data["primary_dir"])
        self.assertEqual([row["source_path"] for row in data["primary"]], [str(prd), str(supplement)])

    def test_invalid_inputs_do_not_create_output(self):
        derived = self.write("source.localized.md")
        source = self.write("source.md")
        empty = self.root / "empty"
        (empty / "primary").mkdir(parents=True)
        output = self.root / "output"
        for args in [
            ["--primary", derived],
            ["--primary", self.root / "missing.md"],
            ["--primary", source, "--reference", source],
            [empty],
        ]:
            with self.subTest(args=args):
                self.run_script(*args, "--output-dir", output, expected=2)
                self.assertFalse(output.exists())

    def test_localized_hash_and_index_describe_effective_text(self):
        source = self.write("source.md", "# 原文\n![图](https://cdn.nlark.com/test.png)\n")
        localized = self.write("source.localized.md", "说明\n\n# 本地化页面\n![图](images/test.png)\n")
        output = self.root / "output"
        argv = [str(SCRIPT), str(source), "--output-dir", str(output)]
        result = {"localized_path": str(localized), "return_code": 0,
                  "image_success": 1, "image_failed": 0}
        with patch.object(sys, "argv", argv), patch.object(prepare, "run_localizer", return_value=result):
            self.assertEqual(prepare.main(), 0)
        record = self.manifest(output)["primary"][0]
        self.assertEqual(record["source_sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
        self.assertEqual(record["sha256"], hashlib.sha256(localized.read_bytes()).hexdigest())
        self.assertEqual(record["heading_index"][0]["start_line"], 3)
        self.assertEqual(record["effective_path"], str(localized))

    def test_preprocessing_failure_is_not_reported_as_success(self):
        source = self.write("source.md", "![图](https://cdn.nlark.com/test.png)\n")
        output = self.root / "output"
        argv = [str(SCRIPT), str(source), "--output-dir", str(output)]
        with patch.object(sys, "argv", argv), patch.object(prepare, "run_localizer",
                return_value={"localized_path": None, "return_code": 2}):
            self.assertEqual(prepare.main(), 1)
        self.assertEqual(self.manifest(output)["primary"][0]["effective_path"], str(source))


if __name__ == "__main__":
    unittest.main()
