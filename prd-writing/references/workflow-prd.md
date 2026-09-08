# PRD 编译与终态交付

PRD 默认后置于需求分析、必要流程和页面原型验证。独立任务若用户已经提供充分确认材料，可以直接执行，不机械补跑前序阶段。

## 1. 输入优先级

### 业务事实

1. `01-需求分析.md` 中 F/S/D、Problem / Goal、Scope、Core Rules；
2. 已确认业务 / 系统流程事实；
3. 用户明确给出的等效确认材料。

### 页面事实

1. 已确认 `prototype/page-ia.md`；
2. 已确认 `prototype/spec/*.md`；
3. 已确认页面流程；
4. HTML 只作为视觉链接，不作为唯一字段事实源。

如果外部 PRD 是本次唯一事实源，仍可直接编写 / 修订，但不得假称前面的内部阶段执行过。

## 2. PRD Compilation Input

进入正文前先在当前上下文压缩本轮需要的信息，不强制落盘：

```text
Goal / Scope
Source IDs: S/F/D
Confirmed Flow facts
Target Pages: Pxxx
Relevant Modules: Mxxx
Prototype Spec paths
Prototype HTML links
Open Issues
```

该 Input 足够后，本轮不回读已消费上游全文。

## 3. 工作稿

不存在工作稿时：

```bash
sh .agents/skills/prd-writing/scripts/create_prd_workdraft.sh <需求目录>/03-PRD/PRD-工作稿.md
```

生成：

- `PRD-工作稿.md`
- `PRD补充信息-工作稿.md`

已有工作稿直接修订，不重复创建。

修改已有 PRD：先建标题 / 行号 / SHA256 索引，再一次批量提取全部受影响章节并集；除整体定稿、跨多个核心流程或无法判断影响外，不读全文。

## 4. 页面功能编译

每个页面功能：

- 功能描述：来自场景、能力与页面目的；
- 界面原型：使用已确认 HTML 相对链接；
- 字段说明：来自 Prototype Spec 的 Field Definitions；
- 交互规则：来自 Spec / Page Flow；
- 业务规则：来自需求分析 F/D 和 Flow，不从视觉布局推导。

“界面原型”章节保留现有四列表：`字段｜类型｜字段说明｜交互规则`。按查询条件、列表、表单、详情、复杂配置等实际区域分组。

不使用“详见原型”代替关键业务定义。

## 5. 无页面功能

定义输入、输出、系统处理、依赖、权限、状态、规则和异常。验收标准仍维护在配套补充信息中。

## 6. 缺口路由

- Problem / Goal / Scope / 核心规则缺失：`requirement-analysis`
- 流程闭环 / 分支缺失：`business-flow-html`
- Page / Module / 字段 / 页面交互缺失：`prd-html-prototype`
- 单纯 PRD 表达：本 Skill 自行修订

不在 PRD 阶段“顺手补设计”，防止 PRD 与已确认原型重新分叉。

## 7. 用户确认与评审

用户确认后成对固化为 `PRD-最终确认版.md` 和 `PRD补充信息-最终确认版.md`，两者共同构成唯一当前确认终态。若用户已要求产品评审，交 `prd-product-review`。评审发现问题后仅回退受影响责任阶段；修订完成再更新受影响 PRD 章节，不全量重编。

PRD 阶段后不再自动进入页面原型，因为页面原型默认已经在上游完成。
