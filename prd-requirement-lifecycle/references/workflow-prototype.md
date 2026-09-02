# HTML 页面原型生成与校验

仅在最终 PRD 已确认且用户明确需要页面原型时读取。

## 1. 生成

1. 状态更新为“原型生成中”。
2. 运行 `python3 .agents/scripts/markdown_sections.py <最终PRD>` 获取标题、行号范围和 SHA256，不把全文输入模型。
3. 先确定本次所有主页面及其所需章节；一个菜单路径对应一个主页面，不把多个独立菜单合并进同一 HTML。
4. 用一次命令的多个 `--select` 批量提取所有页面需要的章节并合并重叠范围。读取集合限于功能描述、界面结构、字段定义、业务规则，以及必要的适用范围、权限、术语和验收。
5. 在同一次源文档理解中，按 [prototype-html.md](prototype-html.md) 为本次所有页面生成 Prototype Spec。Spec 必须记录 PRD SHA256 和来源行号范围。
6. 输出到当前需求目录：
   - `prototype/<page-slug>.html`
   - `prototype/spec/<page-slug>.md`
7. 不把业务字段、业务 CSS 或页面产物写回 `07_Prototype_Base_Styles`。
8. 将基础 CSS、页面 CSS 和页面所需 JavaScript 全部内嵌到 HTML；不得通过 `<link>` 或 `<script src>` 引用工作区文件。

源文档读取闸门：

- Spec 齐全且 SHA256 与当前 PRD 一致时，HTML 生成和校验阶段不得再读 PRD。
- 只有 Spec 明确缺少某个业务定义时，才先通过标题索引定位，增量提取该章节一次，然后更新受影响 Spec。
- PRD SHA256 变化时，只重建受变更章节影响的 Spec；不因其中一页变化重读全文或重建全部页面。

## 2. 校验与回补

生成后不重新读取完整 PRD，检查：

1. 页面路径、字段、表格列、状态和操作覆盖 Prototype Spec，Prototype Spec 中每个界面字段都能映射到 PRD 字段定义；
2. Flexi Base 壳层及基础组件视觉一致；
3. 没有新增 PRD 未定义的页面、导航、统计卡或业务能力；
4. CRUD 使用 Drawer，复杂配置使用独立编辑视图，监控使用概览、进度和下钻；
5. 检查覆盖层层级：弹窗或 Drawer 内只允许继续触发 `confirm` 类型轻量二次确认；若还需展示大量详情、复杂选择或大量结果内容，第一层容器必须为独立页面；确认后的结果优先使用原容器内提示或 Toast；
6. 检查每个数据列表的分页：主页、子页、弹窗和 Drawer 内的列表均须展示条目范围／总数、上下页、页码／省略号／末页及每页条数选择，默认 10 条／页；
7. 运行 `python3 .agents/skills/prd-requirement-lifecycle/scripts/validate_prototype_portability.py <HTML 路径>`，确保文件不依赖本机或外部样式、脚本和资源；
8. 使用可用的浏览器能力实际打开页面，检查首屏、主要交互、折叠／弹层、分页、控制台错误及常见视口下的溢出；
9. 发现字段或业务定义缺失、无法映射或冲突时，不在 Spec 或 HTML 中补造，先回到 PRD 修订并让用户重新确认，只重生成受影响页面。

用户确认所需页面原型后，状态更新为“待归档确认”。
