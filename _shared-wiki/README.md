# Shared Wiki

本目录是多个 Skill 共用的**离线经验池**，不是运行时知识库。

## 访问边界

- Normal Skill Runtime：**WRITE ONLY**，且仅在用户给出明确、可长期复用的方法反馈时写入极简 Feedback Delta。
- Skill Evolution Review：**READ + ANALYZE**，只允许用户手工启动 `skill-evolution-review` 时读取。
- Skill Modification：需要用户明确授权；默认只输出建议。

## 原则

- 正常业务 Skill 禁止读取本目录，不做 Pattern Retrieval。
- 只记录最小 Feedback Delta，不保存完整 Prompt / 输入 / 输出 / PRD / HTML / 操作手册。
- 普通成功执行、普通内容修改、临时业务参数、单项目事实和一次性视觉调整不记录。
- 不自动修改任何 Skill。
