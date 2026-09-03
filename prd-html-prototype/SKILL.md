---
name: prd-html-prototype
description: 基于用户确认的最终 PRD 独立生成 Prototype Spec 与可移植 HTML 页面原型；可接上游产物，不承担需求澄清、PRD 编写或流程确认。
---

# PRD HTML 页面原型

先读[阶段产物与交接协议](../_shared-requirement-protocol.md)，再按任务读取[原型生成与校验](../prd-requirement-lifecycle/references/workflow-prototype.md)和[HTML 原型规则](../prd-requirement-lifecycle/references/prototype-html.md)。

## 输入与产物

- 接受用户确认可作为页面基线的最终 PRD，来源可为上游产物或外部文档，不要求补走澄清、流程、编写或评审。
- 以需求目录或用户指定输出目录为产物根目录；位置不明再询问。
- 工作稿放在 `prototype/workdraft/` 及其 `spec/`；确认后每页成对固化为 `prototype/<page-slug>.html` 和 `prototype/spec/<page-slug>.md`，再次确认前保留当前终态。

## 执行

1. 对 PRD 建标题索引，一次批量提取目标页面所需章节，生成带来源与 SHA256 的 Prototype Spec；充分的 Spec 建成后不回读原文。
2. 根据 `crud`、`complex-config`、`monitor` 选择一个参考页面，遵守基础样式白名单、内嵌资源和字段可追溯规则。
3. 运行可移植性校验并做浏览器验收；定义不足时说明缺口，需要改 PRD 则交给 `prd-writing`，不补造业务事实。
4. 用户确认后同步固化 Spec 与 HTML，更新索引及交接信息；PRD 中的原型链接由 `prd-writing` 维护。
5. 本阶段交付后停止，不自动归档；已有串联授权时按协议继续。

不修改 PRD、评审或流程，不读取 `_shared-wiki`，不自动修改公共原型样式。
