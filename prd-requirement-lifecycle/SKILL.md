---
name: prd-requirement-lifecycle
description: 管理正式产品需求的共创、方案确认、PRD、专家评审、HTML 原型、版本与归档。仅用于用户明确要形成、评审、重写、继续正式需求/PRD，或基于已确认 PRD 生成 HTML 原型；普通咨询和轻量讨论不触发。
---

# 需求共创与 PRD 生命周期

目标：先通过共同探讨和流程图确认消除方案歧义，再以最少过程记录形成可执行、可验收、可追溯的 PRD，并在需要时生成与现有 Flexi 后台风格一致的 HTML 原型。

## 按阶段路由

先定位 `03_Requirements/` 中的需求；新需求确认名称后建档。只读当前阶段需要的内容：

- 建档、共创、流程规划与方案确认：读 [workflow-discovery.md](references/workflow-discovery.md)；进入流程规划时再读 [business-flow-integration.md](references/business-flow-integration.md)。
- PRD 与评审：只读 [workflow-prd-review.md](references/workflow-prd-review.md) 中当前任务对应部分。
- HTML 页面原型：读 [workflow-prototype.md](references/workflow-prototype.md)，再读 [prototype-html.md](references/prototype-html.md)；先用 `.agents/scripts/markdown_sections.py` 一次批量提取全部目标页面的相关章节并建立 Spec，之后不按页回读 PRD。
- 继续进行中需求：只读 `00-需求信息.md` 的“续作索引”，先确定当前目标和下一动作，再按索引定向读取；不因会话重启重读共创、方案、PRD 或评审全文。
- 同一 Session 内，已读取并仍适用于当前目标的文件、标题索引和章节提取结果必须直接复用；仅在文件已变更、当前目标扩大或已持有内容不足以完成下一动作时，才补读最小必要部分。
- 归档或从归档重开：读 [workflow-archive.md](references/workflow-archive.md)；重开后仍使用“续作索引”恢复工作。
- 用户授权生成 PRD 时，运行 `sh .agents/skills/prd-requirement-lifecycle/scripts/create_prd_workdraft.sh <PRD工作稿路径>` 一次生成主 PRD 与独立的 `PRD补充信息-工作稿.md`，不读取骨架正文；再按编写范围读取 [prd-writing-rules.md](references/prd-writing-rules.md) 对应规则。
- 修改已有 PRD 时，先用 `.agents/scripts/markdown_sections.py` 扫描标题索引，再一次批量提取受影响章节并集；已提取章节不因编写、评审或校验分阶段而重读，全文读取条件见 [workflow-prd-review.md](references/workflow-prd-review.md)。
- 产品流程规划与可视化读取 [business-flow-integration.md](references/business-flow-integration.md)：先判断流程图清单和数量，再生成对应流程图供用户确认；需要 HTML 流程视图时直接使用 `$business-flow-html`，无需用户再次单独指定输出形式。

## 不可破坏的闸门

1. 探索只询会改变目标、范围、流程、系统职责、核心规则或验收的问题。页面需求必须确认完整路径及新增／修改页面。
2. 共同探讨消除阻塞问题后，先形成流程图清单，明确总数、每张图的名称、类型、范围和判断依据。每个正式需求至少有一张业务流程图；系统流程图和页面流程图按实际复杂度决定，一类可有多张，不为凑类型或数量拆分。
3. 按流程图清单生成全部工作稿并逐一交用户确认。流程图暴露定义不足时回到共同探讨，只更新受影响的方案和流程图；所有必需流程图确认完成前不得生成 PRD 主文档及其补充信息工作稿。
4. 提交流程图确认时一并说明“确认后即进入 PRD 编写”。用户明确确认全部必需流程图及方案，即视为授权生成成对的 PRD 主文档与补充信息工作稿，不再重复询问一次 PRD 授权。
5. 未确认且不能安全推导的内容标为待确认，不写成事实或确定规则。

## 目标驱动的自更新

- `00-需求信息.md` 必须保持一个可直接续作的“续作索引”，仅保留：当前目标、阶段／下一动作、阻塞问题、当前有效基线路径、本轮受影响范围及按需读取入口。
- 只在上述信息变化，或当前会话结束时无法从现有索引直接恢复下一动作时更新。覆盖已失效的当前值，不追加轮次摘要、对话记录、推理过程或文档内已存在的规则副本。
- 继续任务时先根据续作索引判断实现当前目标所需的最小读取集。索引缺失或失效时，只通过文件名、标题索引和局部章节重建一次；除非当前目标确实要求整体重写或全局定稿，不读全文。
- 当前 Session 已持有的有效内容优先于再次读取同一文件；同一文件的标题索引、局部章节和全文均不得因阶段切换、校验或普通续作而重复读取。
- 自更新的成功标准是“下次能用更少 Token 直接执行正确的下一动作”。不为记录完整性、备忘或 Wiki 积累而写入。

## 轻量经验学习（共享 Wiki）

- 正常执行本 Skill 时，禁止读取 `_shared-wiki`。
- 不进行 Pattern Retrieval，不因历史经验扩大当前上下文。
- 只有当用户明确纠正、接受或拒绝一个“未来可复用的方法”时，才允许记录一条 Feedback Delta。
- 已在当前任务中直接固化进 Skill 的方法不再写 Feedback Delta，避免重复存储和未来召回。
- 普通成功执行、普通内容修改、临时业务参数、单项目事实、一次性视觉调整均不记录。
- Feedback 只保存最小变化，不保存完整 Prompt、完整输入、完整输出、PRD、HTML 或操作手册。
- Wiki 中的经验只允许在用户手工启动 `skill-evolution-review` 时读取。
- Wiki 不得自动修改本 Skill。
