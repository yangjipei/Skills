---
name: business-flow-html
description: 将业务流程、系统流程或页面流程转换为语义分层清晰的单文件 HTML。需求分析后优先用于验证业务逻辑；页面 IA 稳定后按需再次用于验证跨页 / 多步骤页面流程。
---

# Business Flow HTML

目标：用低于完整原型的成本，先验证业务 / 系统 / 页面流转逻辑。

先读[阶段产物与交接协议](../_shared-requirement-protocol.md)。判断和交接时读取[流程集成规则](references/business-flow-integration.md)；生成阶段型流程时读取[流程视觉规则](references/business-flow-rules.md)。

## 三类主视图

- **业务流程**：角色、业务阶段、关键判断、业务结果。默认在需求分析后优先判断。
- **系统流程**：系统边界、触发、状态 / 数据交接、异步与异常补偿。按需。
- **页面流程**：入口、Page / Drawer / Modal、关键操作、反馈、结果。必须在 Page IA / Page Spec 基本稳定后判断，不从模糊需求直接猜页面节点。

一张图只表达一种主语义，不把业务、系统、页面三层混在同一主视图。

## 输入边界

接受：

- `requirement-analysis` 提供的目标 Sxxx + 相关 F/D/Q；
- `prd-html-prototype` 提供的 Page ID / Module ID / 页面动作；
- 用户直接提供的已确认流程事实；
- 外部 PRD 中与目标流程直接相关的局部章节。

不要求先执行指定上游 Skill，但不得为了画图全文读取所有资料。

## 执行

1. 明确 `Flow Type`、目标、Start / End 和覆盖场景。
2. 将输入压缩为内存 Flow Spec，只保留会改变流向的节点、判断、出口和规则。
3. 复杂阶段型流程拆成 4～8 个阶段；简单流程用紧凑视图，不凑阶段。
4. 主路径、关键判断、结束状态常显；规则、异常和补充口径默认折叠。
5. 生成单文件 HTML 到 `flows/workdraft/`，维护 `flows/流程清单.md`。
6. 对照 Flow Spec 做轻量验收，不回读完整上游材料。
7. 用户确认后固化到 `flows/最终确认版/`。
8. 页面流程确认后，只把流程引用与受影响 Page / Module ID 交回 `prd-html-prototype`；不直接修改 Page Spec 或 HTML。

## 视觉硬规则

- 主流程在宽屏横向、中窄屏纵向，连接箭头始终可见，不在响应式断点隐藏。
- 主流程使用明显强于子流程的连接关系。
- 阶段型流程必须提供“全部展开 / 全部收起”，同时保留局部折叠。
- 节点标题尽量 4～12 个字，PRD 长规则不塞进节点。
- 规则、异常默认折叠，但主路径不能因为折叠而断裂。

## 输出

```text
flows/
├── 流程清单.md
├── workdraft/
│   └── <flow-name>.html
└── 最终确认版/
    └── <flow-name>.html
```

页面原型仍放 `prototype/`，不混用目录。

## 完成 Gate

- 主路径从明确 Start 到 End；
- 关键 Yes / No、失败 / 异常出口可辨识；
- 与当前 Flow Spec 一致；
- 浏览器首屏、折叠、箭头和常见视口无明显错误；
- 用户确认当前流程基线。

流程定义缺失时只提出最小问题；需要修改需求事实交 `requirement-analysis`，需要修改页面结构交 `prd-html-prototype`，不越界代写。

不读取 `_shared-wiki`。
