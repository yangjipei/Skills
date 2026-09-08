# Global Patterns

## G-001 事实与推断分离
用户明确提供的内容记为 Fact；模型推断标为 Assumption；缺失信息保持 Unknown。

## G-002 只追问阻塞项
只追问阻塞当前阶段执行的 Required / Conditional 信息，不为填满所有槽位而追问。

## G-003 大文档单次消费
status: promoted
scope: requirement-analysis, prd-html-prototype, prd-writing, operation-manual-generator

先建标题行号索引，一次批量提取当前阶段所需章节；形成 Fact Inventory、Flow Spec、Prototype Spec 或其他稳定中间产物后，后续阶段不回读已消费源内容。
