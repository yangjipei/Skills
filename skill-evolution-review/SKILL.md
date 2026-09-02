---
name: skill-evolution-review
description: 手工检查共享 Wiki 中积累的 Feedback 与 Pattern，判断哪些稳定经验值得固化进现有 Skill，并在用户明确授权时生成和应用最小 Patch。仅在用户明确要求检查、评审或改造 Skill 时触发，不得自动运行。
---

# Skill Evolution Review

目标：以低 Token、最小改动方式检查共享 Wiki 中已沉淀的经验，判断哪些应继续留在 Wiki，哪些值得固化进现有 Skill。

> 本 Skill **仅由用户手工发起**。任何其他 Skill、Wiki 规则或自动流程都不得自动触发本 Skill。

> 本 Skill 是唯一允许读取 `_shared-wiki` 的 Skill。

## 触发边界

仅当用户明确表达以下意图时使用：

- 检查最近 Wiki 经验；
- 看哪些 Skill 值得改造；
- 做 Skill Evolution Review；
- 把稳定 Pattern 固化进 Skill；
- 优化某个 Skill 的长期规则。

普通 Skill 执行、普通用户反馈、单次纠正，不触发本 Skill。

## 输入与最小读取

按顺序最小读取：

1. `../_shared-wiki/patterns/` 中与目标 Skill 相关的 Pattern；
2. 只有 Pattern 证据不足时，才读取 `../_shared-wiki/feedback/` 中相关 Feedback Delta；
3. 只有需要判断重复、冲突或生成 Patch 时，才读取目标 Skill 的 `SKILL.md`；
4. 默认不读取 references、scripts、templates、agents；
5. 只有用户明确要求改造且 Patch 必须同步其他文件时，才按需读取对应文件。

禁止无差别扫描全部 Wiki 或全部 Skill 文件。
标记为 `promoted` / `archived` 的 Pattern 不再分析或召回。

## 低 Token 原则

- 每个目标 Skill 默认最多评估 5 条候选 Pattern。
- 已存在于正式 Skill 的规则直接判为 `ALREADY_IN_SKILL`，不重复分析。
- 不输出完整历史，只引用最小必要证据。
- Patch 必须是最小增量，不重写整个 `SKILL.md`。
- 已固化进 Skill 的 Pattern 应标记为 `promoted` / `archived`，后续不再默认召回。

## 评审标准

每条 Pattern 判断：

- 是否重复出现；
- 是否用户明确长期确认；
- 是否跨任务稳定；
- 是否属于方法，而不是一次性项目事实；
- 是否与现有 Skill 规则重复或冲突；
- 固化后是否能减少未来 Wiki 召回和 Token 消耗。

Feedback 不等于 Pattern。只有满足以下任一条件才允许晋升：

- 用户明确表示“以后都这样”；
- 同类反馈重复 >= 2 次；
- 属于明显跨任务稳定的方法论。

## 输出决策

每条 Pattern 只能给出以下之一：

- `KEEP_IN_WIKI`：继续作为经验保留；
- `PROMOTE_TO_SKILL`：建议固化进 Skill；
- `ALREADY_IN_SKILL`：Skill 已有正式规则；
- `REJECT`：不建议继续采用。

默认只输出评审建议，**不得修改 Skill**。

## 用户授权后的改造流程

只有用户明确说“执行改造”“把这些规则写入 Skill”等，才允许：

1. 读取目标 `SKILL.md`；
2. 定位最合适章节；
3. 生成最小 Patch；
4. 应用 Patch；
5. 检查 YAML front matter、目录结构和现有规则是否被破坏；
6. 必要时做最小验证；
7. 必须把已固化 Pattern 标记为 `promoted` / `archived`，使其后续不再分析或召回。

若改造涉及 references、scripts、templates 或 agents，必须先说明原因；默认不得修改。

## 推荐输出格式

```markdown
# Skill Evolution Review

## prd-requirement-lifecycle

- Pattern: PRD-001
- Decision: PROMOTE_TO_SKILL
- Reason: 高频、跨任务、用户已明确长期确认
- Suggested Patch: 在“不可破坏的闸门”追加 1 条规则

## business-flow-html

- Pattern: FLOW-003
- Decision: KEEP_IN_WIKI
- Reason: 更偏特定视觉偏好，暂不扩大正式 Skill 规则
```

## 权限边界

- Feedback Delta 只能由正常 Skill 在用户给出明确、可长期复用的方法反馈时以最小变化写入；
- Pattern Candidate 只能在用户手工启动本 Skill 后提炼；
- Skill 改造建议只能在用户手工启动本 Skill 后生成；
- **Skill 文件不得自动修改**；
- 是否真正改造由用户决定；
- 用户拥有最终接受、拒绝与回滚权。
