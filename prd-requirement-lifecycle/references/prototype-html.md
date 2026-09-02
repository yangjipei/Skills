# HTML 原型执行规则

仅在 `workflow-prototype.md` 触发页面原型任务时读取。本文件用于压缩 Token 和限制 Codex 乱读文件。

## 1. 核心链路

```text
最终确认 PRD
→ 标题索引
→ 全部目标页面所需章节一次性批量读取
→ 批量 Prototype Spec
→ 选择 1 个 Reference
→ HTML
→ 轻量校验
```

不要让 HTML 生成阶段直接全文理解 PRD。

## 2. Prototype Spec

每个主页面生成一份：
`<当前需求目录>/prototype/spec/<page-slug>.md`

只写 HTML 真正需要的信息：

```markdown
# Prototype Spec

## Page
- Name:
- Path:
- Mode: crud | complex-config | monitor

## Query
- ...

## List / Main Content
- Columns:
- Primary Actions:
- Row Actions:
- Status:

## Form / Editor
- Sections:
- Fields:
- Validation:

## Field Definitions
| Field | PRD definition | UI use |
| --- | --- | --- |
| ... | PRD 章节或字段定义行 | Query / List / Form / Detail |

## Interaction
- ...

## Permission
- ...

## Complex UI
- ...

## Source
- PRD SHA256:
- PRD lines:
- PRD section:
```

规则：
- 不复制 PRD 大段正文；
- 同一轮多页原型先一次性生成全部 Spec，再进入逐页 HTML 生成；不得在生成每个页面时回读同一 PRD；
- 每条用短语或一句话；
- 业务规则只保留会影响页面字段、状态、交互、校验和权限的部分；
- Query、List、Form、Detail 中每个字段都必须出现在 `Field Definitions`，并能映射到 PRD 的逐字段定义；无法映射时停止生成并回补 PRD；
- `Field Definitions` 用于覆盖校验，不要求把每条字段说明都显示在 HTML 中；仅在用户操作需要理解或避免误用时展示帮助文案、占位提示或 Tooltip；
- 自动任务、接口、指标、风险等不影响页面表达时不要放入 Spec。

## 3. 页面模式路由

页面模式选择前先检查覆盖层层级：

- 原则上只允许一层业务内容弹窗或 Drawer；弹窗或 Drawer 内可继续触发 `confirm` 类型轻量二次确认，不将其视为业务内容弹窗嵌套。
- 确认完成后优先在原容器内展示结果提示或 Toast，不从覆盖层内再打开承载大量结果内容的弹窗。
- 若详情或配置容器内还需展示大量详情、复杂选择或大量结果内容，该容器改为同菜单独立页面，再由独立页面打开一层业务内容弹窗。
- 单纯只读且不会触发其他弹层的详情可使用弹窗。

只允许三种：

### crud
适用：
- 普通列表；
- 查询 + 表格；
- 新增／编辑字段较少；
- 新增／编辑适合右侧 Drawer。

Reference：
`07_Prototype_Base_Styles/examples/reference-list-drawer.html`

### complex-config
适用：
- 多轮策略；
- SOP；
- 流程编排；
- 条件分支；
- 复杂规则配置；
- 编辑内容明显超过普通 Drawer 容量。

Reference：
`07_Prototype_Base_Styles/examples/reference-complex-config.html`

复杂配置原则：
- 列表仍保持标准 Flexi 列表；
- Create / Edit 进入同一菜单页面内的独立编辑视图，不把 5～10 轮配置塞入窄 Drawer；
- 编辑视图优先按“基础信息 → 准入/筛选条件 → 流程节点 → 校验 → 底部操作”组织。

### monitor
适用：
- 执行记录；
- 运行监控；
- 汇总指标；
- 进度；
- 多层下钻；
- 异常明细。

Reference：
`07_Prototype_Base_Styles/examples/reference-monitor.html`

## 4. HTML 生成时的唯一读取白名单

在 Prototype Spec 完成后，HTML 生成阶段只允许读取：

1. 当前页面的 `prototype/spec/<page-slug>.md`
2. `07_Prototype_Base_Styles/prototype.rules.md`
3. `07_Prototype_Base_Styles/assets/base.css`
4. 当前页面 Mode 对应的 **一个** Reference

禁止：
- 再次读取完整 PRD；
- 遍历需求目录；
- 搜索其他 HTML/CSS/Markdown；
- 读取其他 Reference；
- 读取 Base README、meta、examples 中其他文件。

若页面交互确实使用公共脚本，可额外读取对应的 `assets/base.js` 或 `assets/multi-select.js`，但必须把所需代码内嵌到最终 HTML，不能生成 `<script src>`。

## 5. 生成约束

- Reference 是页面结构与视觉锚点，不是业务数据来源。
- Base CSS 是唯一公共基础样式来源。
- 不重新设计 Sidebar / Header / Tabs / Breadcrumb / Page Title。
- 不新建一套按钮、输入框、表格、分页视觉。
- 不把多个独立菜单页面塞进同一个 HTML。
- 不新增 PRD 未定义的业务能力。
- Mock 数据 2～3 条即可。
- 页面级 CSS 只允许表达业务特有 UI；禁止覆盖公共壳层和基础组件。
- 复杂业务组件可新增，但不得为了“更好看”重做系统视觉。
- Reference 中的 `<link rel="stylesheet">` 和 `<script src>` 只是来源提示，不得复制到交付文件。
- 将 `assets/base.css` 的内容放入 HTML 的 `<style data-source="flexi-base">`；页面级 CSS 放入另一个内嵌 `<style>`。
- 将页面运行所需 JavaScript 放入内嵌 `<script>`。不得依赖工作区中的 `base.js`、`multi-select.js` 或其他本地文件。
- 不得使用本机绝对路径、`file://`、相对资源路径、CSS `@import` 或外部 URL 加载样式、脚本、字体和图片；必要图片使用内嵌 SVG 或 `data:` URL。

## 6. 输出路径

必须输出到当前需求文件夹：

```text
prototype/
├── spec/
│   └── <page-slug>.md
└── <page-slug>.html
```

禁止输出到工作区根目录或 `07_Prototype_Base_Styles`。

每个 `<page-slug>.html` 都是独立、可复制的单文件交付物。只把该 HTML 发给另一台电脑，也必须保持完整样式和主要交互，无需同时复制 `07_Prototype_Base_Styles` 或其他资源目录。

生成后必须运行：

```bash
python3 .agents/skills/prd-requirement-lifecycle/scripts/validate_prototype_portability.py <prototype/page-slug.html>
```

检查不通过时先修复依赖，再进行浏览器校验。

## 7. 自我进化

Base 不在单次页面生成中自动修改。

当同一种“业务特有 UI 模式”在至少 2 个已确认原型中重复出现时，才形成 Base 升级候选。升级时单独执行：

1. 对比两个已确认原型；
2. 提取共性组件；
3. 升级 `base.css` 或对应 Reference；
4. 保持旧页面兼容；
5. 记录 `07_Prototype_Base_Styles/meta/evolution-log.md`。

普通字段差异、一次性样式和单个业务规则不进入 Base。


## 8. 枚举 / 字典 / 码值策略

HTML 原型不得把未知生产码值当成真实数据。

### 8.1 来源优先级

1. **PRD 明确给出码值 / 枚举值**：原样使用。
2. **PRD 明确说明“复用现有字典 / 现有关联关系”但未给出值**：
   - 下拉框默认只展示 `Please select`；
   - 如确有演示需要，可使用明显的原型占位值，但不得伪装为真实生产码值。
3. **PRD 未提供来源**：
   - 禁止自行创造看似真实的内部 Code、Group ID、Result Code、Provider Code 等。

### 8.2 Mock 值规范

允许的原型占位示例：
- `GROUP_001`
- `STRATEGY_001`
- `PROVIDER_001`
- `RESULT_001`

禁止：
- 无来源地生成看似生产真实值，如 `Online_S1`、`1001`、`CONNECTED`，除非 PRD / 已确认 Reference 明确支持。
- 将示例值表达成真实生产字典。

### 8.3 Label 策略

- PRD 已给英文：原样使用。
- Base / Reference 已有稳定英文命名：复用。
- 只有中文且无系统既有英文：可做语义直译，但不得创造内部缩写、内部码或新术语。

## 9. 列表工具栏固定布局

Flexi 列表页工具栏整体靠右。

固定规则：

```text
[业务按钮 ...] [Refresh] [Column Configuration]
```

- 整个 Toolbar 必须右对齐。
- 新增、创建、批量操作等业务按钮位于 Refresh / Column Configuration 左侧。
- Refresh 与 Column Configuration 始终是最右侧两个固定工具。
- 不得把业务按钮放到左侧。
- 不得交换 Refresh 与 Column Configuration 的固定位置。
- 没有业务按钮时，只保留右侧固定工具。

## 10. 列表分页固定样式

所有数据列表都要展示分页，包括主页、独立子页、弹窗和 Drawer 内的数据列表。固定行数的属性矩阵、规则矩阵或非数据列表不强制分页。

分页从左到右展示：

```text
1-10 of 511 items  <  1  2  3  4  5  …  52  >  10 / page
```

- 默认 10 条／页，每页条数提供 10、20、50、100。
- 必须同时展示当前条目范围和总条数，格式为 `<start>-<end> of <total> items`。
- 当前页使用主色边框和主色文字；其他页码不使用边框。
- 首页禁用上一页，末页禁用下一页。
- 页数较多时展示连续的起始页码、省略号和末页；页数较少时不强制省略号。
- 分页作为一个整体组件，固定位于对应列表正下方并整体右对齐；不与列表工具栏或表格内容混排。
- 在窄视口下允许整体组件换行，不得溢出页面或弹窗。
