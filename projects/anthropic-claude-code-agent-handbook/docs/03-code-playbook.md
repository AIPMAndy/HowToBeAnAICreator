# 03｜Claude Code 工程实战：从一句话到能交付的结果

参考：[Claude Code Best Practices（现行）](https://code.claude.com/docs/en/best-practices)、[2025 原始工程经验](https://www.anthropic.com/research/claude-code-best-practices)、[长任务 Harness（2025）](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)。

## 方法 1：Explore → Plan → Build → Verify

**探索**：请扫描相关文件并解释调用关系；不要修改任何内容。

**计划**：给出最小改动方案、备选项、影响文件、风险、测试方式。

**实现**：只执行已选方案；每一步优先局部测试，勿越权修改。

**验证**：运行测试/静态检查；对照最初需求逐条核对；展示 diff 和未解决问题。

可复制：[完整 Prompt](../prompts/plan-build-verify.md)。

## 方法 2：用 CLAUDE.md 降低重复解释

把这些写进项目根目录 `CLAUDE.md`：

- 项目目标、输入输出、禁止事项
- 正确的测试和构建命令
- 业务术语和数据口径
- 失败后的处理方式
- 必须人工确认的环节

不要把密码、令牌和客户原始信息写进去；也不要无限追加规则。**2026 年官方最佳实践更强调简短、贴近适用范围、可执行的规则。**

## 方法 3：Skill 用于重复任务，Subagent 用于隔离上下文

例如“每次写增长实验复盘” → Skill；“到很多外部资料中查证” → Subagent。一个 Skill 内可以要求 AI 做检查，但只靠自然语言**无法保证**每次都执行；硬性门槛使用测试、权限规则、Hook 或 CI。

## 方法 4：长期任务要留下交接产物

Anthropic 的长任务实践强调：初始化环境、拆成小块、每次结束留清楚的状态。建议维护：

```text
TASKS.md     待办及完成条件
PROGRESS.md  本轮做了什么 / 验证结果 / 下轮第一步
README.md    如何启动、运行与检查
```

每次结束写：
- 已完成：文件、commit、实际运行的验证
- 未完成：阻碍与证据
- 下一步：最小明确任务

不要把“聊天历史自动压缩”误当成可靠的项目永久记忆。

## 方法 5：多 Agent 仅在任务边界清晰时并行

优先各读各的资料；**不要让多个 Agent 并发编辑同一份文件**。复杂工程建议隔离分支或 worktree，合并前运行总测试。

2026 年 Anthropic 进一步公开了“规划者 / 生成者 / 评估者”的长任务架构，但这属于更高复杂度的方法，详见 [官方研究](https://www.anthropic.com/research/harness-design-long-running-apps)。

## 不可省略的质量门槛

- 写代码之前有验收标准
- 变更前后有测试或明确的人工验证
- 高风险操作有权限隔离与审批
- 故障时有回滚点
- 结果报告必须包含“真正运行过什么”

**一个简单、可验证的脚本，胜过十个互相转述结论的 Agent。**

