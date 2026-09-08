# 页面 IA、原型与 Delta 工作流

仅在页面结构设计、Page Spec、HTML 生成或既有原型局部修改时读取。

## 1. 页面事实一次消费

优先从以下压缩输入获取页面事实：

1. 相关 S/F/D + Product Skeleton；
2. 已确认 Flow Spec；
3. 用户明确提供的页面材料；
4. 外部 PRD 的局部页面章节（仅独立原型任务）。

先确定本轮全部目标页面和所需来源章节，再一次批量提取。形成 Page IA / Spec 后，HTML 阶段不回读原始需求全文。

## 2. Page IA

工作稿：`prototype/workdraft/page-ia.md`。

```markdown
# Page IA

## 页面清单
| Page ID | 页面 / 路径 | 目的 | 角色 | 覆盖场景 | 建设方式 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| P001 | ... | ... | ... | S001 | 新增/修改/复用 | Draft |

## P001 页面模块
| Module ID | 模块 | 目的 | 核心信息 / 操作 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- |
| M001 | ... | ... | ... | S001,D002 | EDITABLE |

## 页面流程判断
| Page / Task | 是否需要 Page Flow | 原因 | 涉及 P/M |
| --- | --- | --- | --- |
```

IA 只确定页面与模块层级，不把完整字段定义塞进一张总表。

## 3. Prototype Spec

每页：`prototype/workdraft/spec/<page-slug>.md`。

```markdown
# Prototype Spec

## Page
- Page ID: P001
- Name:
- Path:
- Mode: crud | complex-config | monitor | workspace
- Source: Sxxx / Fxxx / Dxxx / Flow

## Modules
### M001 模块名称
- Status: EDITABLE | LOCKED
- Purpose:
- Source:
- Main Content:
- Actions:
- State / Feedback:

## Query / List / Form / Detail
- ...

## Field Definitions
| Field | Definition | UI use | Source type | Source |
| --- | --- | --- | --- | --- |
| ... | ... | ... | FACT / DECISION / FLOW / UI-DERIVED | F001 |

## Interaction
- ...

## Permission
- ...

## Page Flow
- Required: Yes / No
- Flow path:

## Open Issues
- ...
```

`UI-DERIVED` 只允许表示不改变业务口径的布局、分组、展示方式、通用交互。以下内容缺失时不得标为 UI-DERIVED：权限、账务、状态转换、真实枚举 / 码值、核心资格、重要校验、数据来源。

## 4. Page Flow Gate

以下情况才要求页面流程：

- 多页面 / 多步骤任务；
- 页面、Drawer、Modal 之间存在关键顺序；
- 不同状态导致不同路径；
- 存在失败恢复 / 重试；
- 多角色页面路径明显不同。

需要时交给 `business-flow-html`：目标 Pxxx + Mxxx + 入口 + 操作 + 反馈 + 相关 S/F/D。

必要 Page Flow 未确认前，不进入完整 HTML 交互生成；简单单页记录 No 后直接继续。

## 5. HTML Gate 与最小读取

当 Page Spec 足够后，HTML 阶段只允许读取：

1. 当前页面 Spec；
2. `07_Prototype_Base_Styles/prototype.rules.md`；
3. `07_Prototype_Base_Styles/assets/base.css`；
4. 当前页面模式对应 **1 个** Reference；
5. 页面确需公共脚本时对应的最小脚本。

禁止再次读取完整需求分析、完整流程、完整 PRD 或其他 Reference。

## 6. 生成与模块锚点

HTML 每个 Mxxx 必须带：

```html
<!-- MODULE:M001 START -->
<section data-module-id="M001">...</section>
<!-- MODULE:M001 END -->
```

模块 ID 与 Spec 一致。全局 Shell 不作为业务 Mxxx 反复编号。

## 7. Delta 迭代

用户提出修改时：

1. 先把反馈映射到 Pxxx / Mxxx；
2. 判断是否改变 S/F/D / Flow：若改变，先回责任 Skill；
3. 只读取受影响 Mxxx 的 Spec；
4. 通过 HTML 注释锚点定位并读取对应片段；
5. Patch Spec + HTML 片段；
6. 只重测受影响交互，除非改动 Shell / 全局布局；
7. 用户确认后将 Mxxx 标记 LOCKED。

示例：

```text
LOCKED: M001, M002, M005
EDITABLE: M003, M004
本轮 Delta: P001/M003
```

“再整体优化一下”如果没有明确全局意图，默认只针对当前 EDITABLE 模块，不解锁已经确认模块。

## 8. 固化与 PRD 交接

页面整体确认后同步固化：

- `prototype/page-ia.md`
- `prototype/spec/<page>.md`
- `prototype/<page>.html`
- `prototype/原型清单.md`

交给 `prd-writing` 的事实源是 Page IA / Spec + 原型链接；HTML 只作为视觉参考。这样 PRD 无需重读 HTML 反推字段和交互。
