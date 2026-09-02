# operation-manual-generator

将已上线需求目录中的多份定稿 Markdown 产品文档，生成 HTML 培训操作手册。

## 推荐目录结构

无需 YAML 或其他配置文件，目录本身就是配置：

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

## 核心流程

需求目录 → 扫描 Primary / Reference → 批量本地化 Primary 图片 → Primary 操作事实提取 → 合并轻量 Fact Inventory → 冲突检查 → 必要时按需读取 Reference → 场景编排 → 操作步骤 → 截图挂载 → HTML

## Token 原则

核心是“最小充分读取”：

- 先看目录、manifest、文件名和标题，不直接全文读所有资料。
- Primary 每份只深读一次，只提取操作事实。
- Reference 默认不深读。
- 成功生成 `.localized.md` 后，不再重复读取对应原始 Markdown。
- 有语雀 OCR 注释时优先使用 OCR 做截图定位，不重复视觉识图。
- Fact Inventory 建立后，后续不再全文扫描 Primary。
- Manifest 保存完整标题行号索引；使用 `.agents/scripts/markdown_sections.py` 一次批量提取任务所需章节。
- Fact Inventory 记录文件 hash、已读行号与 `consumed` 状态，后续不回读已消费范围。
- 不生成不会直接影响最终 HTML 的中间长文档。

## 目录级预处理（推荐）

```bash
python3 scripts/prepare_requirement_directory.py \
"/path/to/08_已上线需求/预测式外呼系统"
```

脚本会：

1. 扫描 `primary/` 原始 Markdown。
2. 只对含远程图片的 Primary 做图片本地化。
3. 仅轻量登记 `reference/`（文件名、hash、标题等），不深度解析。
4. 忽略 `.localized.md`、图片报告和 output 等派生产物。
5. 生成：

```text
.operation-manual-manifest.json
```

这个 manifest 用于后续快速确定应该读取哪些文件，避免重复扫描。

## 单文件图片预处理

```bash
python3 scripts/preprocess_yuque_markdown.py \
"/path/to/产品文档.md" \
--domain cdn.nlark.com
```

默认生成：

- `产品文档.localized.md`
- `images/`
- `产品文档.localized.md.image-report.json`

语雀图片下载支持：

- CDN 域名预检
- `User-Agent`
- `Referer: https://www.yuque.com/`
- DNS / timeout / 403 / 404 / network error 分类
- 下载失败保留原 URL

## Skill 文件

- `SKILL.md`：完整执行规范
- `scripts/prepare_requirement_directory.py`：需求目录扫描 + Primary 批量图片预处理 + manifest
- `scripts/preprocess_yuque_markdown.py`：单 Markdown 图片本地化
- `templates/manual-template.html`：默认 HTML 页面骨架
