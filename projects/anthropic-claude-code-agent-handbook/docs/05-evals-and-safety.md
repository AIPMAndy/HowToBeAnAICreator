# 05｜Agent 怎么验收、安全上线？

官方依据：[Agent evals（2026-01）](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)、[Writing tools for agents（2025-09）](https://www.anthropic.com/research/writing-tools-for-agents)、[Claude Code Hooks](https://code.claude.com/docs/en/hooks-guide)、[现行最佳实践](https://code.claude.com/docs/en/best-practices)。

## 1. 先定义正确答案，再让 Agent 跑

每条测试用例应包括：

- **任务输入**：受控的文本、CSV、代码库或工具响应
- **期望行为**：必须做 / 禁止做
- **评分方式**：规则测试、人工审阅或混合评估
- **证据记录**：输出文件、工具调用结果、操作日志
- **失败分类**：检索不到、误用工具、越权修改、事实不符、结果不可执行

**不能只问模型“你觉得做得怎么样”。**

## 2. 最小评估表

| 指标 | 怎么算 | 判断 |
| --- | --- | --- |
| 任务完成率 | 通过用例数 / 总用例数 | 是否真的完成 |
| 事实准确率 | 核实正确的事实数 / 抽检事实数 | 是否胡编 |
| 人工返工率 | 需人工修复的输出数 / 总输出数 | 是否节省时间 |
| 每任务成本 | 模型调用 + 人工审核 + 运行成本 | 是否划算 |
| 安全违规数 | 未经许可的外部操作/泄露/越权次数 | 上线门槛 |

在正式部署前用真实场景构造**独立的留出测试集**，避免只为练习题过关。

## 3. Prompt 和强制规则不同

- 提示词、CLAUDE.md、Skills：帮助模型理解目标，但不是强制执行器。
- 权限限制、沙箱、Hook、CI、独立测试：更适合落实不可违反的门槛。
- 审批者：具有真实交易、生产部署、广告投放权限的人必须保有最后决定权。

## 4. 推荐的权限边界

- 资料研究子 Agent：只读。
- 文案子 Agent：只输出草稿，不直接发布。
- 代码 Agent：只改分支/练习目录；生产仓库须 PR 审核。
- 财务/客户数据 Agent：权限最小化，日志化，不写入 Git。
- 外部网页和 CSV：视为不可信数据，不能执行其中“忽略此前指令”等内容。

## 5. 能实际运行的检查

```bash
python3 -m unittest discover -s tests -v
python3 scripts/ad_audit.py --input examples/ads/sample_ads.csv --output outputs/ad_report.csv
```

检查输出 CSV 是否存在且计算正确；**这只验证演示脚本，不代表已对 Claude 模型进行真实 Agent 评估**。真实 Agent 的结果必须另行记录多轮运行、成本和评分。

## 6. 失败时怎么处理？

- 首先停下有副作用的操作。
- 保存输入/输出/错误消息（脱敏）。
- 回滚到最近的已知可用状态。
- 判断是数据、工具、Prompt、权限还是模型问题。
- 加一条能稳定复现失败的测试，再重新运行。

不能复现的问题，不能轻易宣布“已经解决”。

