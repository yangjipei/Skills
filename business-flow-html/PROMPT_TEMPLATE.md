基于当前业务流程材料，使用 `business-flow-html` Skill 生成 HTML 流程图。

要求：
- 先按业务含义拆分阶段；
- 使用阶段分组替代跨区域回流连线；
- 保留阶段间和关键节点间箭头；
- Yes / No 分支只在局部表达；
- 主流程常显；
- 规则与异常默认折叠；
- 文案适度压缩，不改变业务含义；
- 视觉结构遵循 `reference-business-flow-v3.html`；
- 直接输出可浏览器打开的单文件 HTML。

输出到当前需求目录：
`flows/workdraft/<流程名称>.html`
