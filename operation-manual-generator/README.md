# operation-manual-generator

根据指定的一份或多份定稿 Markdown 生成 HTML 操作手册。支持独立调用和读取上游有效 PRD；已上线手册须确认实际上线范围。

## 兼容目录结构

既有资料可以继续使用以下结构；直接提供文件时不必转换目录：

```text
08_已上线需求/
└── 某个需求/
    ├── primary/
    │   ├── 主文档1.md
    │   └── 主文档2.md
    ├── reference/
    │   ├── 参考资料1.md
    │   └── 参考资料2.md
    └── output/
```

- `primary/`：正式事实源，可多份。
- `reference/`：默认只作参考，按需读取。
- `output/`：最终 HTML。
- `.localized.md`、图片报告、`images/`：派生产物，不作为第二份事实源重复分析。

## 直接指定事实源

```bash
python3 scripts/prepare_requirement_directory.py \
  --primary '/path/to/PRD.md' \
  --primary '/path/to/补充信息.md' \
  --reference '/path/to/参考资料.md' \
  --output-dir '/path/to/08_已上线需求/需求名称/output'
```

单文件可直接作为位置参数，或使用一次 `--primary`；没有参考资料时省略 `--reference`。调用脚本前由使用者确认事实源及上线范围，脚本不自动判定。

原目录模式保持兼容：

```bash
python3 scripts/prepare_requirement_directory.py '/path/to/已上线需求目录'
```

显式文件模式的 manifest 默认在输出目录，传统模式默认在需求根；以脚本返回路径为准。含远程图片时在源文件旁生成 `.localized.md`、`images/` 与报告，不修改原始文件，也不把派生文件重新作为 Primary。新 manifest 提供原始与有效文本的 SHA256，标题索引对应实际消费的 `effective_path`。

## 最小读取与交付

先读 manifest，按标题一次提取必要章节，建立 `fact-inventory.yaml` 后生成手册；Reference 仅按需读取。通过来源范围与 consumed 标记避免反复回读。

默认交付位置为 `08_已上线需求/<需求名称>/output/`，允许指定其他目录。归档不等于上线，已归档 PRD 可作为来源，但不能代替上线范围确认。

## 文件

- `SKILL.md`：输入、事实提取、截图与交付规范。
- `scripts/prepare_requirement_directory.py`：单文件、多文件或目录预处理与来源 manifest。
- `scripts/preprocess_yuque_markdown.py`：图片本地化，失败保留远程 URL 并记录原因。
- `templates/manual-template.html`：HTML 骨架。
- `tests/test_prepare_requirement_directory.py`：输入模式、来源索引与兼容性检查。
