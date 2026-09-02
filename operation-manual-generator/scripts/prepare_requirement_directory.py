#!/usr/bin/env python3
"""Prepare a requirement directory for operation-manual generation.

Directory convention (no config file required):

<requirement>/
  primary/     authoritative Markdown sources (multiple allowed)
  reference/   optional reference Markdown, not authoritative by default
  output/      generated manuals

The script scans files cheaply, localizes remote images in Primary Markdown only,
and writes a compact manifest. Derived files (*.localized.md, reports, images,
output files) are excluded from source discovery.

Standard-library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

REMOTE_IMAGE_RE = re.compile(
    r"!\[[^\]]*\]\((https?://[^\s)]+)|<img\b[^>]*?\bsrc=[\"'](https?://[^\"']+)",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
DERIVED_SUFFIXES = (".localized.md", ".localized.markdown")
REPORT_SUFFIX = ".image-report.json"


def sha1_file(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_source_markdown(path: Path) -> bool:
    if not path.is_file() or path.suffix.lower() not in {".md", ".markdown"}:
        return False
    low = path.name.lower()
    if low.endswith(DERIVED_SUFFIXES):
        return False
    if path.name.startswith("."):
        return False
    return True


def build_heading_index(lines: List[str]) -> List[Dict]:
    headings = []
    for line_number, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match:
            headings.append(
                {
                    "level": len(match.group(1)),
                    "title": match.group(2).strip(),
                    "start_line": line_number,
                }
            )

    for index, heading in enumerate(headings):
        end_line = len(lines)
        for candidate in headings[index + 1 :]:
            if candidate["level"] <= heading["level"]:
                end_line = candidate["start_line"] - 1
                break
        heading["end_line"] = end_line
    return headings


def cheap_inspect(path: Path, heading_limit: int = 24) -> Dict:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    lines = text.splitlines()
    heading_index = build_heading_index(lines)
    remote_count = len(REMOTE_IMAGE_RE.findall(text))
    return {
        "path": str(path),
        "name": path.name,
        "size_bytes": path.stat().st_size,
        "sha1": sha1_file(path),
        "line_count": len(lines),
        "headings": [item["title"] for item in heading_index[:heading_limit]],
        "heading_index": heading_index,
        "remote_image_refs": remote_count,
    }


def run_localizer(script: Path, source: Path, images_dir_name: str, domain: str, overwrite: bool) -> Dict:
    output = source.with_name(f"{source.stem}.localized{source.suffix}")
    cmd = [
        sys.executable,
        str(script),
        str(source),
        "-o",
        str(output),
        "--images-dir",
        images_dir_name,
        "--domain",
        domain,
    ]
    if overwrite or output.exists():
        cmd.append("--overwrite")
    proc = subprocess.run(cmd, text=True, capture_output=True)
    report = output.with_suffix(output.suffix + REPORT_SUFFIX)
    result = {
        "localized_path": str(output) if output.exists() else None,
        "report_path": str(report) if report.exists() else None,
        "return_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }
    if report.exists():
        try:
            data = json.loads(report.read_text(encoding="utf-8"))
            result["image_success"] = data.get("success", 0)
            result["image_failed"] = data.get("failed", 0)
        except Exception:
            pass
    return result


def main() -> int:
    p = argparse.ArgumentParser(description="准备一个操作手册需求目录：扫描 primary/reference，并批量本地化 primary 图片")
    p.add_argument("requirement_dir", help="需求目录，内含 primary/ reference/ output/")
    p.add_argument("--domain", default="cdn.nlark.com", help="图片域名，默认 cdn.nlark.com")
    p.add_argument("--images-dir", default="images", help="每个 primary 目录中的本地图片目录名，默认 images")
    p.add_argument("--overwrite", action="store_true", help="覆盖已存在的 localized Markdown")
    p.add_argument("--manifest", help="manifest 输出路径；默认需求目录/.operation-manual-manifest.json")
    args = p.parse_args()

    root = Path(args.requirement_dir).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: 需求目录不存在: {root}", file=sys.stderr)
        return 2

    primary_dir = root / "primary"
    reference_dir = root / "reference"
    output_dir = root / "output"
    if not primary_dir.is_dir():
        print(f"ERROR: 缺少 primary/ 目录: {primary_dir}", file=sys.stderr)
        return 2
    reference_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    localizer = Path(__file__).with_name("preprocess_yuque_markdown.py")
    if not localizer.is_file():
        print(f"ERROR: 找不到图片预处理脚本: {localizer}", file=sys.stderr)
        return 2

    primary_sources = sorted([x for x in primary_dir.rglob("*") if is_source_markdown(x)])
    reference_sources = sorted([x for x in reference_dir.rglob("*") if is_source_markdown(x)])

    primary_records = []
    for src in primary_sources:
        rec = cheap_inspect(src)
        # Only localize when remote image references exist; otherwise use original source directly.
        if rec["remote_image_refs"] > 0:
            rec["preprocess"] = run_localizer(localizer, src, args.images_dir, args.domain, args.overwrite)
            rec["effective_path"] = rec["preprocess"].get("localized_path") or str(src)
        else:
            rec["preprocess"] = {"skipped": True, "reason": "no_remote_images"}
            rec["effective_path"] = str(src)
        primary_records.append(rec)

    # Reference files are deliberately only cheap-inspected. No image localization and no deep content processing.
    reference_records = []
    for src in reference_sources:
        rec = cheap_inspect(src)
        rec["reading_policy"] = "on_demand_only"
        reference_records.append(rec)

    manifest = {
        "schema_version": "operation-manual-manifest-v1",
        "requirement_dir": str(root),
        "primary_dir": str(primary_dir),
        "reference_dir": str(reference_dir),
        "output_dir": str(output_dir),
        "policy": {
            "primary": "authoritative; use heading_index, batch-read selected sections once, then use Fact Inventory",
            "reference": "non-authoritative by default; read only when needed",
            "derived": "do not treat localized/report/images/output as source facts",
        },
        "primary_count": len(primary_records),
        "reference_count": len(reference_records),
        "primary": primary_records,
        "reference": reference_records,
    }

    manifest_path = Path(args.manifest).expanduser().resolve() if args.manifest else root / ".operation-manual-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    image_ok = sum((x.get("preprocess") or {}).get("image_success", 0) for x in primary_records)
    image_fail = sum((x.get("preprocess") or {}).get("image_failed", 0) for x in primary_records)
    print(f"Requirement: {root}")
    print(f"Primary: {len(primary_records)} source file(s)")
    print(f"Reference: {len(reference_records)} source file(s)")
    print(f"Images: {image_ok} success, {image_fail} failed")
    print(f"Manifest: {manifest_path}")
    print(f"Output: {output_dir}")
    return 0 if image_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
