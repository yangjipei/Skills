# 产品经理助手 Skills

## 默认低 Token 产品需求链路

```text
business-request-registration（按需）
业务诉求登记
        ↓
requirement-analysis
需求分析
├─ Fact Inventory
├─ Scenario Discovery
├─ Problem / Goal
├─ Scope
├─ Core Rules
└─ Product Skeleton
        ↓
business-flow-html
业务流程图
        ↓
prd-html-prototype
页面 IA / Page Spec
        ↓
business-flow-html（按需再次调用）
页面流程
        ↓
prd-html-prototype
HTML 原型
        ↓
prd-html-prototype
原型 Delta 迭代 / 模块锁定
        ↓
prd-writing
PRD 编译 / 定稿
        ↓
prd-product-review（按需）
产品专家评审
        ↓
requirement-archiving（按需）
归档
```

> 页面 IA / Page Spec 与 HTML 原型由同一个 `prd-html-prototype` Skill 连续负责，不额外拆一个 Skill。这样避免重复读取同一批页面上下文。页面流程需要时，才把最小 Page Spec 交给 `business-flow-html`，确认后再回到原型 Skill。

## 方法原则

1. **越不确定，使用越低成本的表达方式**：先文字与场景，再流程，再页面结构，最后 HTML。
2. **PRD 后置**：有页面的需求默认先通过流程和原型验证，PRD 最后把已确认方案结构化固化，而不是承担早期探索。
3. **事实、场景、决策、问题稳定编号**：`Fxxx / Sxxx / Dxxx / Qxxx`。
4. **只传最小上下文**：下游优先读取编号、Spec 和受影响章节，不重复全文消费上游资料。
5. **原型只改 Delta**：Page / Module 使用稳定 ID；已确认模块锁定，只读取和修改受影响模块。
6. **按需跳过**：轻量诉求登记、系统流程、页面流程、页面原型、产品评审、归档都可以按任务性质跳过；不为流程完整性创建空产物。

完整阶段协议见：[`_shared-requirement-protocol.md`](_shared-requirement-protocol.md)。
