# Business Flow HTML Skill

基于最终确认的第三版 HTML 设计沉淀。

适合：
- 复杂业务流程
- 多轮策略流转
- 状态流转
- 规则密集型流程
- 传统 Mermaid/SVG 连线过多、跨区回流严重的场景

核心设计：
`阶段分组 + 关键箭头 + 局部 Yes/No + 规则折叠`

业务流程统一输出到需求目录的 `flows/`；页面原型继续使用 `prototype/`。

建议不要并入 `07_Prototype_Base_Styles`。
它属于“业务流程可视化”，与后台页面原型是两套不同能力。
