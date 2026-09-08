基于当前已确认的最小流程输入，使用 `business-flow-html` Skill 生成 HTML 流程图。

要求：
- 先明确 Flow Type：Business / System / Page；
- Business / System 优先使用相关 S/F/D；Page Flow 优先使用 P/M + 相关 S/F/D；
- 先压缩 Flow Spec，不回读无关全文；
- 主路径常显，规则与异常默认折叠；
- 阶段型流程保留“全部展开 / 全部收起”；
- 宽屏和中窄屏连接箭头都必须持续可见；
- 不补造业务规则或页面节点；
- 输出可直接打开的单文件 HTML；
- 工作稿输出到 `flows/workdraft/<流程名称>.html`。
