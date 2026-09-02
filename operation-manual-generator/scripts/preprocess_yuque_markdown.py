#!/usr/bin/env python3
"""Preprocess Yuque-exported Markdown.

Downloads remote images (especially cdn.nlark.com/yuque URLs) into a local
images directory and rewrites Markdown/HTML image references to relative paths.
Failures keep the original URL and are recorded in a JSON report.

Standard-library only: no third-party dependency required.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import shutil
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple

MD_IMAGE_RE = re.compile(r"(!\[[^\]]*\]\()(?P<url>https?://[^\s)]+)(?P<tail>(?:\s+[\"'][^\"']*[\"'])?\))", re.IGNORECASE)
HTML_IMAGE_RE = re.compile(r"(<img\b[^>]*?\bsrc=[\"'])(?P<url>https?://[^\"']+)(?P<tail>[\"'][^>]*>)", re.IGNORECASE)

ALLOWED_SCHEMES = {"http", "https"}
DEFAULT_UA = "Mozilla/5.0 (compatible; operation-manual-generator/1.0)"


def is_remote_image(url: str, domains: Optional[List[str]]) -> bool:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        return False
    if not domains:
        return True
    host = (parsed.hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in domains)


def extension_from_response(url: str, content_type: str) -> str:
    content_type = (content_type or "").split(";", 1)[0].strip().lower()
    ext = mimetypes.guess_extension(content_type) if content_type else None
    if ext == ".jpe":
        ext = ".jpg"
    if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".avif"}:
        return ext

    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".avif"}:
        return suffix
    return ".img"


def download(url: str, timeout: float, retries: int) -> Tuple[bytes, str]:
    last_error: Optional[Exception] = None
    request = urllib.request.Request(url, headers={"User-Agent": DEFAULT_UA, "Referer": "https://www.yuque.com/"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = response.read()
                if not data:
                    raise RuntimeError("empty response")
                return data, response.headers.get("Content-Type", "")
        except Exception as exc:  # retain exact network error in report
            last_error = exc
            if attempt < retries:
                time.sleep(min(1.0 * (attempt + 1), 3.0))
    assert last_error is not None
    raise last_error



def classify_error(exc: Exception) -> Tuple[str, str]:
    """Return a stable error category and human-readable message."""
    if isinstance(exc, urllib.error.HTTPError):
        if exc.code == 403:
            return "http_403", "HTTP 403 Forbidden"
        if exc.code == 404:
            return "http_404", "HTTP 404 Not Found"
        return f"http_{exc.code}", f"HTTP {exc.code}: {exc.reason}"
    if isinstance(exc, urllib.error.URLError):
        reason = exc.reason
        if isinstance(reason, socket.timeout):
            return "timeout", "Network timeout"
        if isinstance(reason, socket.gaierror):
            return "dns_failure", f"DNS resolution failed: {reason}"
        text = str(reason).lower()
        if "name or service not known" in text or "temporary failure in name resolution" in text or "nodename nor servname" in text:
            return "dns_failure", f"DNS resolution failed: {reason}"
        if "timed out" in text:
            return "timeout", f"Network timeout: {reason}"
        return "network_error", f"Network error: {reason}"
    if isinstance(exc, (socket.timeout, TimeoutError)):
        return "timeout", f"Network timeout: {exc}"
    if isinstance(exc, socket.gaierror):
        return "dns_failure", f"DNS resolution failed: {exc}"
    return "other_error", f"{type(exc).__name__}: {exc}"


def preflight_domains(domains: List[str], timeout: float) -> Dict[str, dict]:
    """Fast per-domain DNS preflight so an unreachable CDN does not timeout per image."""
    results: Dict[str, dict] = {}
    previous_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        for domain in sorted(set(domains)):
            try:
                infos = socket.getaddrinfo(domain, 443, type=socket.SOCK_STREAM)
                addresses = sorted({item[4][0] for item in infos})
                results[domain] = {"status": "ok", "addresses": addresses[:4]}
            except Exception as exc:
                category, message = classify_error(exc)
                results[domain] = {"status": "failed", "error_type": category, "error": message}
    finally:
        socket.setdefaulttimeout(previous_timeout)
    return results


def replace_refs(text: str, mapper) -> str:
    def repl_md(match: re.Match) -> str:
        url = match.group("url")
        mapped = mapper(url)
        return f"{match.group(1)}{mapped}{match.group('tail')}"

    def repl_html(match: re.Match) -> str:
        url = match.group("url")
        mapped = mapper(url)
        return f"{match.group(1)}{mapped}{match.group('tail')}"

    text = MD_IMAGE_RE.sub(repl_md, text)
    text = HTML_IMAGE_RE.sub(repl_html, text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="下载语雀 Markdown 远程图片并改写为本地相对路径")
    parser.add_argument("input", help="输入 Markdown 文件")
    parser.add_argument("-o", "--output", help="输出 Markdown 文件；默认在原文件旁生成 *.localized.md")
    parser.add_argument("--images-dir", default="images", help="图片目录名，默认 images")
    parser.add_argument("--domain", action="append", dest="domains", help="仅下载指定域名，可重复；默认下载所有远程图片")
    parser.add_argument("--timeout", type=float, default=20.0, help="单次下载超时秒数，默认 20")
    parser.add_argument("--retries", type=int, default=2, help="失败重试次数，默认 2")
    parser.add_argument("--overwrite", action="store_true", help="允许覆盖输出 Markdown 和已有同名图片")
    parser.add_argument("--report", help="下载报告 JSON 路径；默认 <输出文件>.image-report.json")
    parser.add_argument("--preflight-timeout", type=float, default=3.0, help="域名 DNS 预检超时秒数，默认 3")
    parser.add_argument("--skip-preflight", action="store_true", help="跳过域名预检，直接逐图下载")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.is_file():
        print(f"ERROR: 输入文件不存在: {input_path}", file=sys.stderr)
        return 2
    if input_path.suffix.lower() not in {".md", ".markdown"}:
        print("ERROR: 输入文件必须是 Markdown", file=sys.stderr)
        return 2

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    else:
        output_path = input_path.with_name(f"{input_path.stem}.localized{input_path.suffix}")

    if output_path.exists() and not args.overwrite:
        print(f"ERROR: 输出文件已存在，使用 --overwrite 覆盖: {output_path}", file=sys.stderr)
        return 2

    output_path.parent.mkdir(parents=True, exist_ok=True)
    images_dir = output_path.parent / args.images_dir
    images_dir.mkdir(parents=True, exist_ok=True)

    text = input_path.read_text(encoding="utf-8-sig")
    cache: Dict[str, str] = {}
    records: List[dict] = []
    counter = 0

    domains = [d.lower().strip() for d in args.domains] if args.domains else None

    # Fast preflight for explicitly constrained domains (recommended for Yuque CDN).
    preflight = {}
    blocked_domains = set()
    if domains and not args.skip_preflight:
        preflight = preflight_domains(domains, max(args.preflight_timeout, 0.1))
        blocked_domains = {d for d, r in preflight.items() if r.get("status") == "failed"}
        for d in blocked_domains:
            r = preflight[d]
            print(f"WARN: 域名预检失败 {d}: {r.get('error_type')} - {r.get('error')}", file=sys.stderr)

    def mapper(url: str) -> str:
        nonlocal counter
        if url in cache:
            return cache[url]
        if not is_remote_image(url, domains):
            cache[url] = url
            return url

        counter += 1
        host = (urllib.parse.urlparse(url).hostname or "").lower()
        matched_domain = next((d for d in (domains or []) if host == d or host.endswith("." + d)), None)
        if matched_domain in blocked_domains:
            r = preflight[matched_domain]
            cache[url] = url
            records.append({
                "url": url,
                "status": "failed",
                "local_path": None,
                "error_type": r.get("error_type", "preflight_failed"),
                "error": f"Preflight failed for {matched_domain}: {r.get('error')}",
            })
            return url

        try:
            data, content_type = download(url, args.timeout, max(args.retries, 0))
            digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
            ext = extension_from_response(url, content_type)
            filename = f"image_{counter:03d}_{digest}{ext}"
            target = images_dir / filename
            if target.exists() and not args.overwrite:
                # Same generated filename is deterministic for this run/order; avoid accidental overwrite.
                pass
            else:
                target.write_bytes(data)
            relative = Path(args.images_dir, filename).as_posix()
            cache[url] = relative
            records.append({
                "url": url,
                "status": "success",
                "local_path": relative,
                "bytes": len(data),
                "content_type": content_type,
            })
            return relative
        except Exception as exc:
            cache[url] = url  # Important: retain source URL on failure.
            category, message = classify_error(exc)
            records.append({
                "url": url,
                "status": "failed",
                "local_path": None,
                "error_type": category,
                "error": message,
            })
            return url

    rewritten = replace_refs(text, mapper)
    output_path.write_text(rewritten, encoding="utf-8")

    report_path = Path(args.report).expanduser().resolve() if args.report else output_path.with_suffix(output_path.suffix + ".image-report.json")
    report = {
        "input": str(input_path),
        "output": str(output_path),
        "images_dir": str(images_dir),
        "total_unique_remote_images": len(records),
        "success": sum(1 for r in records if r["status"] == "success"),
        "failed": sum(1 for r in records if r["status"] == "failed"),
        "preflight": preflight,
        "records": records,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Markdown: {output_path}")
    print(f"Images:   {images_dir}")
    print(f"Report:   {report_path}")
    print(f"Images: {report['success']} success, {report['failed']} failed")
    return 0 if report["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
