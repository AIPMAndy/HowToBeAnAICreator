# 02｜Agent 六种架构：什么时候拆，怎么拆

> 依据：[Building effective agents（2024）](https://www.anthropic.com/research/building-effective-agents)、[Multi-agent research（2025）](https://www.anthropic.com/engineering/multi-agent-research-system)、[Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)、[Agent teams](https://code.claude.com/docs/en/agent-teams)。

**先用最简单方法解决问题。** 以下是把官方介绍的方法转为中文的教学分类；并非声称 Anthropic 规定了统一的“六步法”。

| 模式 | 适合什么任务 | 不适合什么任务 | 验收 |
| --- | --- | --- | --- |
| 1. 单次调用 | 规范清晰的分类、改写 | 多步外部操作 | 结果符合规则 |
| 2. Prompt 链 | 先抽取事实→再写总结 | 顺序无依赖 | 每关可独立核验 |
| 3. 路由分发 | 按问题类型交给不同专家 | 类别无法判断 | 路由准确率 |
| 4. 并行工作者 | 多来源核实、多角度审稿 | 共享写同一个文件 | 结果独立且可合并 |
| 5. 编排者—工作者 | 子任务随问题变化 | 简单固定步骤 | 覆盖率、冲突处理 |
| 6. 生成者—评估者 | 有明确质量标准、值得迭代 | 没有评分标准 | 多轮质量增益/成本 |

## 核心心智模型

```text
用户任务
   │
   ▼
能否用明确规则/一个脚本解决？ ── 是 ──> 普通软件，不必调用 Agent
   │否
   ▼
单个 Claude 能否完成并验证？ ──────── 是 ──> 单 Agent
   │否
   ▼
子任务能否彼此独立？ ─────────────── 是 ──> 并行工作者
   │否
   ▼
需要动态分解？ ────────────────── 是 ──> 编排者—工作者
   │
   └─ 输出必须反复打磨？ ───────────────> 加评估者
```

## Claude Code 的三个对象不要混淆

- **Skill**：可重复步骤与约定，用在“同一种任务经常做”。本项目 [.claude/skills/business-to-agent](../.claude/skills/business-to-agent/SKILL.md) 是范例。
- **Subagent**：单个 Claude Code 会话里，独立上下文的研究/审查助手。适用于搜索几十份文件、做独立审查。本项目提供 [source-researcher](../.claude/agents/source-researcher.md) 和 [quality-reviewer](../.claude/agents/quality-reviewer.md)。
- **Agent team**：多个可协同的 Claude Code 会话；截至本次核查，官方文档注明 **实验性、默认关闭**，有已知限制和更高资源消耗。不能与普通 subagents 等同。

## 官方多 Agent 研究系统的可迁移部分

Anthropic 在 2025 年介绍的 Research 系统：**主 Agent 定研究方向，多个工作者并行搜集，最后综合与评估。**

复刻一个市场研究任务：

1. 主 Agent 写出要回答的 3 个可验证问题。
2. 子 Agent A 只查市场规模原始公开数据；B 只查竞品产品与定价；C 只查用户痛点证据。
3. 各自输出“原始 URL / 日期 / 事实 / 不确定性”。
4. 主 Agent 对冲突说清楚，禁止把无法核实的数字写成确定事实。
5. 审核者根据引用覆盖率、计算复核、缺失证据判定是否达标。

### 什么时候不加 Agent

如果“每周汇总一个 CSV”可以用 50 行 Python 稳定完成，就不要部署三层 Agent。只有**非结构化理解、跨来源搜集、需要自主判断的部分**值得交给语言模型。

## 最小可执行配置

在 Claude Code 目录中放：

```text
CLAUDE.md
.claude/agents/source-researcher.md
.claude/agents/quality-reviewer.md
.claude/skills/business-to-agent/SKILL.md
```

然后向 Claude Code 说：

> 先用 source-researcher 只读核对这个问题的资料，再用 quality-reviewer 对最终回答做独立审查。各自给出证据链接。不要发布或修改真实业务系统。

Claude Code 是否启动具体 subagent，取决于当前版本、权限和调度；必要时按 [官方 Subagent 文档](https://code.claude.com/docs/en/sub-agents) 显式指定。多 Agent 不保证更快、更便宜或更准确。

