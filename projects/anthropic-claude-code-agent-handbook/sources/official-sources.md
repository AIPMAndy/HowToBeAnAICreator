# 官方原始资料与证据登记

本项目仅从公开的 Anthropic / Claude 文档中提炼方法。所有教学实现均为自行撰写，不复制原版 PDF、文章全文、配图或内部代码。

| ID | 日期 | 材料 | 能证实什么 |
| --- | --- | --- | --- |
| S01 | 2025-07-24 | [How Anthropic teams use Claude Code：22 页 PDF](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) | 10 个内部团队的具体实践、建议与自述影响 |
| S02 | 2025-07-24 | [Claude 官网概览](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code) | 公开的团队方法概要 |
| S03 | 2024-12-19 | [Building effective agents](https://www.anthropic.com/research/building-effective-agents) | 工作流、Agent、路由、并行、编排、评估等模式；较早版本的工程思想 |
| S04 | 2025-04-18 | [Claude Code：Best practices（当时）](https://www.anthropic.com/research/claude-code-best-practices) | CLAUDE.md、探索-计划-编码-提交、Git、自动化的历史实践 |
| S05 | 2025-06-13 | [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | 主 Agent + 并行研究工作者的经验 |
| S06 | 2025-09-11 | [Writing tools for agents](https://www.anthropic.com/research/writing-tools-for-agents) | 工具设计、描述、评估与迭代 |
| S07 | 2025-09-29 | [Context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) | 上下文选择与维护 |
| S08 | 2025-11-26 | [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) | 初始化、分批执行、交接文件 |
| S09 | 2026-01-09 | [Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) | Agent 评估方法 |
| S10 | 2026-03-24 | [Harness design for long-running application development](https://www.anthropic.com/research/harness-design-long-running-apps) | 规划者-生成者-评估者、可评分的设计质量 |
| D01 | 动态更新 | [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart) | 现行安装与登录 |
| D02 | 动态更新 | [Best practices](https://code.claude.com/docs/en/best-practices) | 现行指导与安全边界 |
| D03 | 动态更新 | [Subagents](https://code.claude.com/docs/en/sub-agents) | 子 Agent 配置 |
| D04 | 动态更新 | [Skills](https://code.claude.com/docs/en/skills) | Skill 格式和使用 |
| D05 | 动态更新 | [Hooks](https://code.claude.com/docs/en/hooks-guide) | 确定性动作门槛 |
| D06 | 动态更新 | [MCP](https://code.claude.com/docs/en/mcp) | 外部工具接入 |
| D07 | 动态更新 | [Agent teams](https://code.claude.com/docs/en/agent-teams) | 多会话协作、实验性限制 |

## 引用规则

1. 引用 S01 的数字，必须保留其“原报告中的受访团队自述”语境。
2. 2025 报告里的快捷键、自动批准方法不一定适用于当前版本，操作以 D01–D07 为准。
3. 本项目的练习数据均为合成内容，不能作为 Anthropic 官方效果数据。
4. 引用外部原始文档请链接原文，而不是复制全部段落。
5. 如发现官方链接迁移，请记录迁移前后地址、核查日期与是否影响方法。

## 来源覆盖说明

“10 个团队”表示这份公开 PDF 的 10 个章节；**不等于 Anthropic 公开过的全部工程文章，更不等于其全部内部实践**。这是一份可持续扩展的中文手册，不是非法抓取或私有文档汇编。

最近人工核查：2026-11-10。

