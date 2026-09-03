---
name: operation-manual-generator
description: 基于用户指定的单份或多份定稿文档独立生成 HTML 操作手册，也可读取上游有效 PRD；不强制转换目录，区分事实源、参考资料与实际上线范围。
---

# Operation Manual Generator

将指定的定稿产品事实转为面向业务用户、运营、管理员或一线坐席的可执行 HTML 操作手册。先读[阶段产物与交接协议](../_shared-requirement-protocol.md)，独立调用完成本阶段即交付；不改写 PRD，不推测未定义的产品逻辑。

## 不可破坏的原则

1. 菜单、页面、按钮、字段、状态、权限、校验、顺序和结果必须可追溯到定稿 Primary。未知内容保持未知，不用经验补齐。
2. Primary 是默认事实源；Reference 只用于解释缺口或定位冲突，不自动覆盖 Primary。草稿、TBD、TODO、待确认或待评审内容不得写成最终事实。
3. 源文档的处理单位是“章节集合”，不是整篇文件。同一内容在一轮任务中只进入模型上下文一次。
4. 先形成轻量 Fact Inventory，再编排场景、生成 HTML 和校验；Inventory 完成后不回读 Primary。

## 输入与输出

- **独立调用**：接受用户指定且已确认可作手册事实源的一份或多份 Markdown，不要求先建档、编写 PRD 或归档。
- **串联调用**：从续作索引定位有效 PRD、补充信息和必要参考资料，直接使用原路径，不搬运或复制成另一套原始文档。
- Primary 表示权威事实源，Reference 表示按需参考，是输入角色，不是必须建立的目录。保留原有 `primary/`、`reference/` 目录模式兼容既有材料。
- 已上线系统手册须确认实际上线范围与指定文档一致；已有明确确认直接复用。归档日期或文件名不能作为上线证明；上线差异影响步骤时先确认。
- 默认输出到 `08_已上线需求/<已确认需求名称>/output/`，也接受用户指定位置。名称或位置不能确定时只补问缺项。将输出位置显式传给预处理脚本。
- `.localized.md`、图片报告、`images/`、manifest 和 output 为派生产物，不再作为第二份事实源。

## 源文档单次读取协议

### 1. 预处理与索引

直接指定来源，无需转换目录：

```bash
python3 .agents/skills/operation-manual-generator/scripts/prepare_requirement_directory.py \
  --primary '<当前PRD路径>' \
  --primary '<配套补充信息路径>' \
  --reference '<按需参考路径>' \
  --output-dir '08_已上线需求/<需求名称>/output'
```

`--primary`、`--reference` 可重复，未提供参考时省略 `--reference`。单文件也可作为位置参数：

```bash
python3 .agents/skills/operation-manual-generator/scripts/prepare_requirement_directory.py \
  '<定稿文档.md>' --output-dir '<输出目录>'
```

兼容既有目录：`python3 .agents/skills/operation-manual-generator/scripts/prepare_requirement_directory.py <需求目录>`。

只读取脚本返回的 manifest。指定文件模式默认位于输出目录，传统目录模式默认位于需求根；不要自行假定路径。Primary 记录包含原始来源 `source_path`、`source_sha256`、`effective_path`、有效文本的 `sha256` 和 `heading_index`；Reference 使用 `path`、`sha256` 和 `heading_index` 按需读取，不再扫描正文获取标题。该脚本只准备输入，不判断文档是否已确认或实际上线。

含远程图片时，沿用图片本地化流程，在源文件旁生成派生 Markdown、图片及报告，不改原文；后续只消费 `effective_path`，不同时读取原文。记录本地化失败，不能把失败当作图片已齐全。

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

将最终手册会使用的操作事实保存到输出目录的 `fact-inventory.yaml`，包括前述 sources 与 consumed 范围；不保存无关全文：

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

生成完整、可直接打开的单文件 HTML，保存到本次确定的输出目录。仅在进入 HTML 生成时读取 `templates/manual-template.html`，内嵌必要 CSS，不依赖外部 CSS 或 JS。文档包含说明、整体流程和各场景；FAQ 或异常处理只在 Inventory 有事实时生成。

完成后在交付说明中列明事实源、上线范围确认情况、未决项和输出路径，不自动启动其他阶段。不回读 Primary，直接对照 Inventory 检查：所有产品事实有来源；场景无跳步；图片路径可用并就近挂载；一名未参与产品设计但具备基本业务知识的用户能按手册完成已定义操作。

## 轻量经验学习

正常执行时禁止读取 `_shared-wiki`。只有用户明确纠正或长期确认可复用方法时，才记录最小 Feedback Delta；不保存完整输入、输出、PRD 或手册。Wiki 只在用户手工启动 `skill-evolution-review` 时定向读取，不自动修改本 Skill。
