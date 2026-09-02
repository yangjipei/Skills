# prd-requirement-lifecycle

## PRD-001 诉求与需求分离
业务诉求 Request 与正式 Requirement 是独立对象；已受理诉求不等于已形成需求。

## PRD-002 阶段独立
需求分析、方案设计、PRD 生成分别维护阶段状态，避免一次性从模糊输入直接生成完整 PRD。

## PRD-003 目标驱动的续作索引
status: promoted

需求过程只覆盖更新能支撑正确下一动作的最小续作索引；会话重启时按目标定向读取，不重读全文，不为 Wiki 或过程完整性额外写入。该规则已固化进 `prd-requirement-lifecycle`，后续不再召回。
