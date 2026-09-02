---
name: operation-manual-generator
description: 基于需求目录中的多份定稿 Markdown 主文档（primary）与按需参考资料（reference），以最小充分读取方式提取操作事实，自动本地化语雀图片并生成 HTML 培训操作手册。强调事实约束、低 Token 消耗、冲突确认和截图挂载。
---

# Operation Manual Generator

将一个已上线需求目录中的定稿产品事实，转为面向业务用户、运营、管理员或一线坐席的可执行 HTML 操作手册。不改写 PRD，不推测未定义的产品逻辑。

## 不可破坏的原则

1. 菜单、页面、按钮、字段、状态、权限、校验、顺序和结果必须可追溯到定稿 Primary。未知内容保持未知，不用经验补齐。
2. Primary 是默认事实源；Reference 只用于解释缺口或定位冲突，不自动覆盖 Primary。草稿、TBD、TODO、待确认或待评审内容不得写成最终事实。
3. 源文档的处理单位是“章节集合”，不是整篇文件。同一内容在一轮任务中只进入模型上下文一次。
4. 先形成轻量 Fact Inventory，再编排场景、生成 HTML 和校验；Inventory 完成后不回读 Primary。

## 目录边界

默认一次只处理 `08_已上线需求/` 下一个能唯一定位的需求目录：

```text
<requirement>/
├── primary/      # 多份定稿事实源
├── reference/    # 按需参考
└── output/       # 最终产物
```

`.localized.md`、图片报告、`images/` 和 `output/` 是派生产物，不得再当作事实源。单文件任务也使用下述索引与单次提取协议。

## 源文档单次读取协议

### 1. 预处理与索引

先运行：

```bash
python3 .agents/skills/operation-manual-generator/scripts/prepare_requirement_directory.py <需求目录>
```

只读 `.operation-manual-manifest.json`。Manifest 已包含文件 hash、有效路径和完整 `heading_index` 行号范围；不要再为获取目录或标题扫描 Markdown 正文。

有远程图片时，后续只使用 manifest 中的 `effective_path`，不再读对应原始 Markdown。

### 2. 一次批量提取

根据所有 Primary 的 `heading_index`，先确定手册需要的章节并求并集。对每份 `effective_path` 只运行一次：

```bash
python3 .agents/scripts/markdown_sections.py <effective_path> \
  --select '<功能或页面标题>' \
  --select '<流程、规则或权限标题>'
```

优先选取会改变实际操作的功能、页面、流程、字段、状态、权限、规则、异常、验收和截图上下文。背景、收益、架构、API、数据库、排期和测试计划默认不读，除非索引显示存在操作依赖。

### 3. 标记已消费

Fact Inventory 头部记录：

```yaml
sources:
  - path: <effective_path>
    sha256: <hash>
    ranges: ["120:188", "240:315"]
    state: consumed
```

`consumed` 表示后续场景编排、HTML 生成、截图挂载和验收不得再读该范围。只有发现明确事实缺口时，才从 `heading_index` 定位并增量提取新章节一次，然后更新 Inventory。不得用“再确认一下”作为回读理由。

Reference 只在 Primary 无法解释、Primary 明确引用、用户点名或冲突定位时，按同样方式增量读取相关章节。

## Fact Inventory

只记录最终手册会使用的操作事实：

```yaml
- id: F01
  feature:
  role:
  entry:
  preconditions: []
  actions: []
  fields: []
  rules: []
  result: []
  images: []
  source: "<path>#L120-L188"
```

空字段保持空值，不推测。多份 Primary 的不同范围直接合并；同一功能的入口、顺序、权限、状态或结果冲突时，不自行选择。

待确认项一次集中提出：P0 为不确认会导致操作错误的阻塞项；P1 影响完整度但可生成保守版本；P2 是按默认规范处理的视觉或排版选择。

## 场景与步骤

不按 PRD 目录机械改写。只基于 Inventory 按“角色 → 场景 → 前置条件 → 操作路径 → 操作步骤 → 结果”组织。默认顺序为前置配置、核心操作、执行过程、结果查询、补充或异常操作；无事实的环节不生成。

每个场景只写适用角色与时机、前置条件、明确的菜单路径、顺序步骤、必要字段、结果和会影响操作的注意事项。不写需求背景、泛化口号或无来源的按钮名。

## 截图

- 优先根据 Markdown 上下文和语雀 OCR 注释映射页面、功能和 Step；OCR 只用于定位，不覆盖正文事实。
- OCR 缺失、严重不完整或无法确认关键操作时，才视觉分析该图一次。
- 无法可靠映射时，放到场景末尾或列为 P1，不强行挂载，不伪造截图。

## HTML 交付与检查

生成完整、可直接打开的单文件 HTML，保存到 `<requirement>/output/`。仅在进入 HTML 生成时读取 `templates/manual-template.html`，内嵌必要 CSS，不依赖外部 CSS 或 JS。文档包含说明、整体流程和各场景；FAQ 或异常处理只在 Inventory 有事实时生成。

不回读 Primary，直接对照 Inventory 检查：所有产品事实有来源；场景无跳步；图片路径可用并就近挂载；一名未参与产品设计但具备基本业务知识的用户能按手册完成已定义操作。

## 轻量经验学习

正常执行时禁止读取 `_shared-wiki`。只有用户明确纠正或长期确认可复用方法时，才记录最小 Feedback Delta；不保存完整输入、输出、PRD 或手册。Wiki 只在用户手工启动 `skill-evolution-review` 时定向读取，不自动修改本 Skill。
