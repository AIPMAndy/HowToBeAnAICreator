<div align="center">

# Anthropic Claude Code × Agent 实战保姆级攻略

**从 Anthropic 10 个团队的真实案例，到普通人可以复制的 AI 协作方法。**

中文原创教程 · 10 部门案例 · 6 类 Agent 模式 · 可用的子 Agent / Skill 模板 · 无依赖 Python 演练

**[30 分钟上手](docs/00-quickstart.md) · [10 个团队](docs/01-ten-teams.md) · [Agent 架构](docs/02-agent-patterns.md) · [商业实战](docs/04-business-cases.md) · [官方证据](sources/official-sources.md)**

作者：[AI 酋长 Andy](https://github.com/AIPMAndy) · [官网](https://metaver.vip/) · [更多免费开源项目](https://github.com/AIPMAndy)

</div>

> 💡 **一句话**：不会写代码，也可以从真实业务任务出发，先用 Claude Code 把可重复的工作跑通，再按需要增加 Skills、工具和专业子 Agent。**复杂并不是先进；能验收的结果才是。**

## 为什么做这个项目？

2025 年 7 月，Anthropic 发布《How Anthropic teams use Claude Code》。官网文章是概要；其公开 PDF 详述了 **10 个部门**如何使用 Claude Code，包括增长营销、法务、设计、数据、产品、安全和基础设施团队。

我们进一步整理 Anthropic 官方公开的 Agent 方法、当前 Claude Code 文档与 2026 年长任务实践，转化为中文可执行教程。**并非 Anthropic 官方项目；不包含其内部私有源码、数据或未公开 Prompt。**

## 从哪个入口开始？

| 你是谁 | 先做什么 | 对应资料 |
| --- | --- | --- |
| 完全零基础 | 安装 CLI，完成一个文件任务 | [30 分钟上手](docs/00-quickstart.md) |
| 工程师 / 产品经理 | 探索 → 计划 → 实现 → 验证 | [Claude Code 方法](docs/03-code-playbook.md) |
| 市场 / 运营 | CSV 广告诊断 → 两个子 Agent 写创意 → 人工审核 | [营销案例](docs/04-business-cases.md) |
| 企业主 / 管理者 | 用流程卡梳理本部门可自动化工作 | [业务落地与 ROI](docs/04-business-cases.md) |
| Agent 开发者 | 判断单 Agent、并行、编排、评估是否必要 | [六种设计模式](docs/02-agent-patterns.md) |
| 想把结果做得可靠 | Evals、安全边界、回滚、人审 | [验证与安全](docs/05-evals-and-safety.md) |

## 10 个内部团队速览

| 官方报道团队 | 典型公开用法 | 可迁移能力 |
| --- | --- | --- |
| 数据基础设施 | Kubernetes 截图定位、财务文本流程、入职读代码 | 故障排查 / 非技术自动化 |
| Claude Code 产品研发 | 原型、Vim 模式、测试、PR 评论处理 | 研发闭环 |
| 安全工程 | Terraform 变更审查、故障运行手册、TDD | 安全审核 / 文档 |
| 推理 | 代码理解、边界测试、跨语言测试 | 技术能力迁移 |
| 数据科学与可视化 | 非前端背景开发 React 看板 | 数据产品化 |
| API Knowledge | 从陌生代码找到相关文件、定位问题 | 代码检索 |
| 增长营销 | 广告 CSV、文案子 Agent、Figma 批量创意、Meta Ads MCP | AI 获客 |
| 产品设计 | 截图做可交互原型、梳理状态边界 | 设计转开发 |
| RL 工程 | 小中型功能、测试、检查点与回滚 | 试错与收敛 |
| 法务 | 律师路由、会议跟踪、无障碍原型 | 非程序员做工具 |

[逐团队案例、适合任务、模仿步骤和证据出处 →](docs/01-ten-teams.md)

## 最短实操路线（先拿结果）

1. 进入本目录，在命令行执行 `claude`。第一次使用先阅读 [安装指南](docs/00-quickstart.md)。
2. 把业务需求写入一个 Markdown 文件，而不是一句“帮我全自动做完”。
3. 请求先扫描文件、提出验收标准，不立即改动。
4. 先做 **单 Agent** 的最小可用版本；只有任务可并行、可独立验证时，才拆分成子 Agent。
5. 以测试结果、人工抽检、git diff / 输出文件为验收，而不是“AI 说完成了”。

### 零 API、零依赖演练

这个模拟广告分析案例无需 Claude 订阅即可运行“确定性分析”部分；接入 Claude Code 后，再练习如何让专门的 Agent 基于指标提出创意建议。

```bash
python3 scripts/ad_audit.py --input examples/ads/sample_ads.csv --output outputs/ad_report.csv
python3 -m unittest discover -s tests -v
```

所有广告数据均为**人工构造的教学数据**，不是 Anthropic 或客户的真实账户。输出只是待改进广告的指标标记，不会自动调用模型、投放广告或承诺收益。详见 [练习步骤](examples/ads/README.md)。

## 项目目录

```text
.
├── README.md
├── CLAUDE.md                     # 本项目的 AI 协作约定
├── docs/
│   ├── 00-quickstart.md
│   ├── 01-ten-teams.md
│   ├── 02-agent-patterns.md
│   ├── 03-code-playbook.md
│   ├── 04-business-cases.md
│   └── 05-evals-and-safety.md
├── .claude/
│   ├── agents/source-researcher.md
│   ├── agents/quality-reviewer.md
│   └── skills/business-to-agent/SKILL.md
├── prompts/
│   ├── discover.md
│   ├── plan-build-verify.md
│   └── marketing-agents.md
├── examples/ads/
├── scripts/ad_audit.py
├── tests/test_ad_audit.py
├── sources/official-sources.md
└── LICENSE.md
```

## 阅读规则与版权

- **[官方报道]**：仅记录公开材料明确说过的做法。关联原始链接与时间。
- **[我们复刻]**：由我们自行设计的 Prompt、检查清单、模板、样例数据与代码，不能声称是 Anthropic 内部资产。
- **[建议/推断]**：来自方法抽象，需要自己用真实流程验证。
- 不转载 Anthropic 原文全文、原版 PDF 或其图片；提供摘要和原始链接。**不保证收录了 Anthropic 未公开的全部实践**。
- 2025 年的交互操作可能随版本变化。以 [Claude Code 官方最新文档](https://code.claude.com/docs/en/overview) 为准。

## 商业合作与作者

这个项目免费公开；想把方法迁移到 AI 获客、企业 IP、团队效率、AI 产品化等真实业务，可查看：

- [星觉科技 / AI 酋长 Andy 官网](https://metaver.vip/)
- [GitHub 开源项目主页](https://github.com/AIPMAndy)

**本项目不是 Anthropic 官方产品、合作项目或认证课程。** 欢迎提交可复现的新案例、勘误与原始证据。项目文本与代码许可见 [LICENSE.md](LICENSE.md)。

最后核查：2026-11-10。

