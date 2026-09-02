#!/usr/bin/env python3
"""Validate that a prototype HTML file is a portable, self-contained artifact."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class PrototypeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.errors: list[str] = []
        self.style_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name.lower(): value or "" for name, value in attrs}
        tag = tag.lower()

        if tag == "style":
            self.style_count += 1
        if tag == "link" and "stylesheet" in values.get("rel", "").lower().split():
            self.errors.append("发现外部样式表 <link rel=\"stylesheet\">")
        if tag == "script" and values.get("src"):
            self.errors.append(f"发现外部脚本 <script src=\"{values['src']}\">")
        if tag in {"img", "audio", "video", "source", "iframe"}:
            source = values.get("src", "")
            if source and not source.startswith("data:"):
                self.errors.append(f"发现未内嵌资源 <{tag} src=\"{source}\">")

        for name in ("href", "src"):
            value = values.get(name, "")
            if re.match(r"^(?:file:|/(?:Users|home)/|[A-Za-z]:[\\/])", value, re.I):
                self.errors.append(f"发现本机绝对路径 {name}=\"{value}\"")


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: validate_prototype_portability.py <prototype.html>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"文件不存在: {path}", file=sys.stderr)
        return 2

    html = path.read_text(encoding="utf-8")
    parser = PrototypeParser()
    parser.feed(html)

    errors = parser.errors
    if parser.style_count == 0:
        errors.append("未发现内嵌 <style>，基础样式可能没有写入 HTML")
    if re.search(r"@import\s+(?:url\s*\()?\s*['\"]?", html, re.I):
        errors.append("发现 CSS @import 外部依赖")
    for raw_url in re.findall(r"url\(\s*([^)]+?)\s*\)", html, re.I):
        url = raw_url.strip().strip("'\"")
        if not url.lower().startswith("data:") and not url.startswith("#"):
            errors.append("发现 CSS url(...) 外部资源依赖")
            break

    if errors:
        print(f"可移植性检查失败: {path}", file=sys.stderr)
        for error in dict.fromkeys(errors):
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"可移植性检查通过: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
