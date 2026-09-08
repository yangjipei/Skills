# 本次重构说明

## 核心变化

1. `requirement-clarification` → `requirement-analysis`。
   - 从“补齐歧义”升级为“事实 → 场景 → 问题 / 目标 → 范围 → 规则 → Product Skeleton”。
   - 新增稳定编号 `Fxxx / Sxxx / Dxxx / Qxxx`。
   - 默认产物由 `01-需求共创记录.md` 改为 `01-需求分析.md`。
   - 删除默认 `02-方案确认.md`，避免重复文档。

2. `business-flow-html` 提前。
   - 需求分析后优先验证 Business Flow。
   - Page IA 后按需再次用于 Page Flow。

3. `prd-html-prototype` 不再依赖“最终 PRD”。
   - 负责 Page IA + Prototype Spec + HTML + Delta / Lock。
   - 使用 `Pxxx / Mxxx` 稳定页面和模块 ID。
   - HTML 使用 `MODULE:Mxxx` 注释锚点，局部修改只读受影响片段。

4. `prd-writing` 后置。
   - 有页面需求默认在原型收敛后再编译 PRD。
   - PRD 使用 Page Spec 生成字段 / 交互定义，不通过重读完整 HTML 反推需求。

5. `prd-product-review` 后置且最小回退。
   - 业务问题 → requirement-analysis
   - 流程问题 → business-flow-html
   - 页面问题 → prd-html-prototype
   - 文档表达 → prd-writing

6. 清理已不存在的 `prd-requirement-lifecycle` Wiki Pattern 和旧验证快照，避免后续 Skill Evolution 误召回。

## 为什么没有新增 Page IA Skill

Page IA / Page Spec 与 HTML 原型高度共享页面上下文。如果拆成独立 Skill，会增加一次交接、一次上下文读取和一套重复规则。因此继续放在 `prd-html-prototype` 中；只有需要页面流程时才把最小 P/M 输入交给 `business-flow-html`，确认后回到原型阶段。

## 目录兼容

为减少脚本和既有项目迁移成本，保留现有 `03-PRD/`、`04-评审记录/`、`prototype/`、`flows/` 目录名，不为了阶段顺序重编号历史目录。
