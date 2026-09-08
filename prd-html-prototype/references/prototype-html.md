# HTML 原型执行规则

仅在 Page IA / Prototype Spec 已建立且进入 HTML 或 Delta 修改时读取。

## 1. 核心链路

```text
已确认需求分析 / Flow
→ Page IA
→ Prototype Spec
→ Page Flow（按需）
→ 1 个 Reference
→ HTML
→ Delta / LOCK
```

HTML 生成阶段不承担需求发现。

## 2. 页面模式

- `crud`：查询 + 列表 + 普通新增 / 编辑；普通表单优先 Drawer。
- `complex-config`：多轮策略、SOP、复杂规则；编辑使用独立页面视图。
- `monitor`：执行记录、指标、进度、异常下钻。
- `workspace`：高密度作业台、案件详情 / 呼叫工作台等持续操作场景；以任务效率和信息层级为优先，不机械套普通 CRUD。

参考页只允许读取当前 Mode 对应的 1 个 Reference。若 Base 尚无 `workspace` Reference，复用最接近的已确认壳层并把业务特有结构写在页面 CSS，不创造第二套全局视觉体系。

## 3. 业务事实与 UI 设计选择

Prototype Spec 中字段 / 交互来源类型：

- `FACT`：Fxxx 或明确外部事实；
- `DECISION`：Dxxx；
- `FLOW`：已确认流程；
- `UI-DERIVED`：不改变业务口径的页面组织选择。

HTML 不得把 `UI-DERIVED` 升格为新的业务规则。

## 4. HTML 读取白名单

Spec 足够后只读：

1. 当前页面 Spec；
2. `07_Prototype_Base_Styles/prototype.rules.md`；
3. `07_Prototype_Base_Styles/assets/base.css`；
4. 当前 Mode 的 1 个 Reference；
5. 必须用到的最小公共脚本。

禁止：全文读取上游文档、遍历需求目录、读取多个 Reference、读取其他页面 HTML 作为“灵感”。

## 5. 生成约束

- Reference 是结构 / 视觉锚点，不是业务数据源。
- 不重新设计公共 Sidebar / Header / Tabs / Breadcrumb / 基础组件。
- 一个菜单路径对应一个主页面，不把多个独立菜单塞入单个 HTML。
- 不新增未在 Spec 中定义的业务能力。
- Mock 数据 2～3 条即可；未知生产码值不得伪造。
- 基础 CSS、页面 CSS、运行 JS 全部内嵌，最终 HTML 单文件可复制运行。
- 不使用本机绝对路径、`file://`、外部 URL 或未内嵌本地依赖。
- 所有主交互必须可点击，不允许只做 hover 展示。
- 普通业务弹层最多一层；其内只允许轻量 confirm。复杂详情 / 选择改独立页。
- 数据列表按现有 Base 规则提供完整分页。

## 6. Module Delta

每个业务模块必须：

```html
<!-- MODULE:M001 START -->
<section data-module-id="M001">...</section>
<!-- MODULE:M001 END -->
```

Delta 修改只读目标标记范围。锁定 Mxxx 不因邻近模块调整而重写。

如果用户要求全局视觉改版，可以解锁全局视觉层，但仍不得未经确认改变业务模块结构。

## 7. 枚举 / 字典 / 码值

1. 来源明确：原样使用。
2. 明确复用现有字典但值未知：默认 `Please select`，演示值必须明显为占位。
3. 来源未知：禁止生成看似真实的内部 Code。

允许占位：`GROUP_001`、`STRATEGY_001`；不得伪装为生产码值。

## 8. 列表工具栏

默认整体靠右：

```text
[业务按钮 ...] [Refresh] [Column Configuration]
```

具体页面若已确认不同布局，以 Page Spec 为准。

## 9. 校验

运行：

```bash
python3 .agents/skills/prd-html-prototype/scripts/validate_prototype_portability.py <HTML路径>
```

浏览器检查首屏、核心操作、弹层 / 折叠、分页、控制台和常见视口。Delta 只重测受影响区域；Shell / 全局布局变化时再做全页检查。

## 10. Base 进化

单次页面不自动修改公共 Base。同一种业务特有 UI 模式至少在 2 个已确认原型重复出现后，才单独形成 Base 升级候选。
