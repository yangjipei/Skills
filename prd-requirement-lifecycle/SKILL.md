---
name: prd-requirement-lifecycle
description: 兼容既有正式需求入口：定位当前产物与阶段，并引导至需求澄清、流程、PRD、评审、原型或归档的专业 Skill；不再承担各阶段交付物作业。
---

# 正式需求兼容入口

本 Skill 用于兼容既有调用，不再编写任何阶段产物。先读[正式需求产物与状态协议](../_shared-requirement-protocol.md)，定位需求目录并只读取 `00-需求信息.md` 的续作索引或用户明确提供的当前材料，按输入条件定位当前目标，再按用户已授权范围建议或调用对应专业 Skill；单独调用不扩展到后续阶段，串联调用不因缺少历史阶段记录而回退：

| 当前目标 | 专业 Skill |
|---|---|
| 建档、澄清、方案确认 | `requirement-clarification` |
| 生成或维护流程 HTML | `business-flow-html` |
| 编写、修订或确认 PRD | `prd-writing` |
| 产品专家评审或复审 | `prd-product-review` |
| 最终 PRD 页面原型 | `prd-html-prototype` |
| 归档或重开 | `requirement-archiving` |
| 基于指定事实源生成操作手册 | `operation-manual-generator` |

若续作索引缺失，只通过目录文件名、标题索引和局部章节定位当前基线，交给实际执行阶段维护最小索引；不代替专业 Skill 写入产物，也不要求先执行本兼容入口。

## 轻量经验学习（共享 Wiki）

- 正常执行本 Skill 时，禁止读取 `_shared-wiki`。
- 不进行 Pattern Retrieval，不因历史经验扩大当前上下文。
- 只有当用户明确纠正、接受或拒绝一个“未来可复用的方法”时，才允许记录一条 Feedback Delta。
- 已在当前任务中直接固化进 Skill 的方法不再写 Feedback Delta，避免重复存储和未来召回。
- 普通成功执行、普通内容修改、临时业务参数、单项目事实、一次性视觉调整均不记录。
- Feedback 只保存最小变化，不保存完整 Prompt、完整输入、完整输出、PRD、HTML 或操作手册。
- Wiki 中的经验只允许在用户手工启动 `skill-evolution-review` 时读取。
- Wiki 不得自动修改本 Skill。
