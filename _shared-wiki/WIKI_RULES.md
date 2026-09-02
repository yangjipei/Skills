# Wiki Rules

## Feedback Delta

仅当用户明确纠正、长期确认或否决一个未来可复用的方法时记录。每条只保存最小变化，禁止保存完整对话、Prompt、输入、输出或完整产物。

```yaml
skill: business-flow-html
type: correction
issue: 一级阶段缺少主流程连接符
accepted_rule: 一级阶段之间必须保持主流程视觉连续
rejected_rule:
scope: business-flow-html
```

不记录：普通成功执行、普通内容或字段修改、临时业务参数、国家配置、单项目事实、具体业务数据、正常 PRD 或页面调整、一次性视觉微调。

## Pattern 晋升

Feedback 不等于 Pattern。只有满足以下任一条件才能在 `skill-evolution-review` 中晋升：

- 用户明确表示“以后都这样”；
- 同类反馈重复出现 >= 2 次；
- 属于明显跨任务稳定的方法论。

## 读取与召回

- 正常业务 Skill 禁止读取 Wiki，不进行 Pattern Retrieval。
- 只有用户手工启动 `skill-evolution-review` 时，才可按 Skill scope 定向读取最小必要的 Pattern 和 Feedback。
- `promoted` / `archived` Pattern 不再分析、不再召回。

## Skill 改造权限边界

- Feedback Delta：正常 Skill 运行时仅可按上述明确反馈条件写入。
- Pattern Candidate：只可在用户手工启动 `skill-evolution-review` 后提炼。
- Skill 改造建议：只可在用户手工启动 `skill-evolution-review` 后生成。
- **禁止自动修改任何现有 Skill 文件。**
- 只有用户明确手工发起 `skill-evolution-review`，并明确要求执行改造时，才允许生成或应用最小 Patch。
- 未得到用户明确要求时，只能输出建议，不得写回 `SKILL.md`、references、scripts、templates 或 agents。
- Skill 改造完成后，必须把已固化的 Wiki Pattern 标记为 `promoted` / `archived`，后续不再分析或重复召回。
