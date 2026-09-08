---
name: prd-html-prototype
description: 在完整 PRD 之前，基于已确认需求分析与必要业务流程完成 Page IA、Prototype Spec、按需页面流程规划、可移植 HTML 原型，以及模块级 Delta 迭代与锁定；也可独立接收等效页面事实。
---

# 页面 IA 与 HTML 原型

先读[阶段产物与交接协议](../_shared-requirement-protocol.md)，再按任务读取[页面 IA、原型与 Delta 工作流](references/workflow-prototype.md)和[HTML 原型规则](references/prototype-html.md)。

## 定位

本 Skill 不再要求“先有最终 PRD”。对有页面的需求，默认顺序是：

```text
需求分析 + 必要业务流程
→ Page IA
→ Prototype Spec
→ 页面流程必要性判断
→ 必要 Page Flow 确认
→ HTML
→ Delta 迭代 / 模块锁定
→ 交给 prd-writing 编译 PRD
```

Page IA / Spec 与 HTML 放在同一个 Skill，是为了避免把同一页面上下文交给两个 Skill 重复读取。

## 输入

接受：

- `01-需求分析.md` 中与页面相关的 S/F/D、Product Skeleton；
- 已确认业务 / 系统流程的 Flow Spec 或必要事实；
- 用户直接提供的页面基线、截图、字段材料或外部 PRD 局部章节；
- 已有 Page IA / Spec / HTML 的 Delta 修改请求。

缺少影响业务结果的事实时生成 Qxxx 建议并交 `requirement-analysis`；仅缺普通布局 / 信息层级时可在 Page Spec 阶段做明确标记的 UI 设计选择，不伪造成业务规则。

## 核心产物

```text
prototype/
├── 原型清单.md
├── workdraft/
│   ├── page-ia.md
│   ├── spec/
│   │   └── <page-slug>.md
│   └── <page-slug>.html
├── page-ia.md
├── spec/
│   └── <page-slug>.md
└── <page-slug>.html
```

工作稿确认后同步固化 Page IA、受影响 Spec 和 HTML。

## 稳定 ID 与锁定

- Page：`P001...`
- 每个页面 Module：`M001...`，页面内稳定，不因布局移动重编号。
- Spec 中记录模块状态：`EDITABLE / LOCKED`。
- HTML 中每个业务模块必须使用注释锚点：

```html
<!-- MODULE:M001 START -->
...
<!-- MODULE:M001 END -->
```

局部修改只读取受影响 Mxxx 的 Spec 和 HTML 标记片段；除非用户明确要求全局改版，不重做其他 LOCKED 模块。

## 执行

1. 读取最小页面事实，形成 / 更新 `page-ia.md`，确认页面集合、路径、职责和模块层级。
2. 为本轮全部目标页面一次生成 Prototype Spec；业务事实引用 S/F/D / Flow，UI 设计选择标记 `UI-DERIVED`。
3. 判断是否需要页面流程。需要时只把目标 P/M 和动作交给 `business-flow-html`；独立调用则停在页面流程建议，已有串联授权时流程确认后继续。
4. Page Spec 和必要 Page Flow 足够后，HTML 生成阶段只读当前 Spec + Base + 1 个 Reference。
5. 生成结构完整、可操作的单文件 HTML；不新增未经确认的业务能力。
6. 结构确认后再做视觉层 Delta，不在早期为了“更好看”改变业务结构。
7. 用户反馈时识别受影响 P/M，更新 Spec，再局部 Patch HTML；重新校验受影响交互。
8. 用户确认模块或整页后标记 LOCKED；页面整体确认后固化终态。
9. 向 `prd-writing` 交接 Page IA、Spec、原型链接和相关 Flow，不要求 PRD 重新解析 HTML 提取字段。

## 边界

- 不修改 `01-需求分析.md` 中的业务事实与核心规则。
- 不自己生成 Page Flow HTML；流程图由 `business-flow-html` 负责。
- 不编写完整 PRD。
- 不因 UI 缺口创造生产码值、权限、账务或状态规则。
- 不读取 `_shared-wiki`，不自动修改公共 Base。
