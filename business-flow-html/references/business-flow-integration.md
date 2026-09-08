# 产品流程 HTML 集成规则

用于判断流程必要性和最小交接。视觉、HTML 和模板规则由 `business-flow-html` 自身维护。

## 1. 默认时机

### 业务流程

需求分析形成核心 S/F/D 和 Product Skeleton 后判断。存在多角色、状态变化、业务分支、跨系统协作或重要异常出口时，建议在原型前先画。

简单静态展示或局部字段调整若不改变业务过程，可以记录“不需要业务流程图”。

### 系统流程

存在多系统调用、异步、回调、任务编排、锁定 / 解锁、状态同步、数据交接或异常补偿时按需生成。

### 页面流程

**必须等 Page IA / Page Spec 基本稳定后再判断。**

只有存在多页面、多步骤、多状态、关键弹层、不同角色路径或失败恢复路径时生成。简单单页信息展示 / CRUD 不强制页面流程。

## 2. 最小输入

### 需求分析 → 业务 / 系统流程

```text
Flow Goal
Start / End
覆盖 Sxxx
相关 Fxxx / Dxxx
仍影响流向的 Qxxx
```

### Page Spec → 页面流程

```text
目标 Pxxx
涉及 Mxxx
入口
关键操作
状态反馈
页面 / Drawer / Modal 节点
相关 S/F/D
```

禁止为了流程图全文读取整个需求、PRD 或全部 Page Spec。

## 3. Flow Spec

生成前在当前上下文压缩：

```text
Flow Name:
Flow Type: Business | System | Page
Goal:
Start:
End:
Source IDs: Sxxx / Fxxx / Dxxx / Pxxx / Mxxx

Actors / Lanes / Page Nodes:
Stages:
1. ...
   - Main steps
   - Decisions
   - Exit / Exception

Key Rules:
Open Issues:
```

Flow Spec 足够后，HTML 生成和校验不再回读上游全文。

## 4. 拆分

一张图围绕一个可独立评审的目标。只有主线因为多个独立业务场景、系统边界或用户任务变得难以辨认时才拆分，不按“业务 / 系统 / 页面”机械各画一张。

## 5. 交接

- 业务事实缺失：回 `requirement-analysis`。
- 页面节点 / 页面行为不明确：回 `prd-html-prototype` 的 Page IA / Spec。
- PRD 已存在但文字需要同步：交 `prd-writing`，流程 Skill 不改 PRD。
- 页面流程确认后，只向原型阶段返回流程路径、Flow Spec 和涉及 P/M ID。

流程 HTML 是可视化确认物，但正文关键事实仍应在需求分析 / Page Spec / PRD 中独立可理解。
