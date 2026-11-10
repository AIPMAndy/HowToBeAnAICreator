# 00｜30 分钟真正上手 Claude Code

> 目标：完成一次“读文件 → 明确任务 → 小改动 → 检查”的闭环。零基础不必先学习 Agent 框架。

## 0. 准备

你需要可以使用 Claude Code 的账号或受支持的 API / 云服务访问资格、电脑终端，以及**一个自己有权处理的项目目录**。可用地区、付费方案和版本以 [官方 Quickstart](https://code.claude.com/docs/en/quickstart) 为准。

## 1. 安装

macOS / Linux / WSL（官方原生安装方式；执行外部安装脚本前先核对域名和内容）：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://claude.ai/install.ps1 | iex
```

若你不希望直接执行远程脚本，请使用官方页面给出的包管理器方式：[安装说明](https://code.claude.com/docs/en/quickstart)。

安装后执行：

```bash
claude --version
```

## 2. 建立练习目录

如果你从这个教程的 GitHub 父仓库下载，请进入 `projects/anthropic-claude-code-agent-handbook`。也可以自行创建一个空目录：

```bash
mkdir my-claude-practice
cd my-claude-practice
printf '# 任务：整理一个每周销售复盘表\n输入：公开或虚构的 CSV\n输出：一份 200 字摘要\n限制：不得编造营收\n' > TASK.md
claude
```

首次启动遵循屏幕上的登录指引；在交互窗口中发送：

> 请先读取 TASK.md，只解释你理解的目标、缺失信息、风险和验收标准。先不要写代码或改文件。

## 3. 第二条指令：让它给出最小方案

> 请给我两种方案，说明成本、实施步骤、失败风险。推荐最少依赖的方案。此时不修改文件。

## 4. 第三条指令：执行并验收

> 按选定方案实施。只处理练习目录内的文件，先生成 3 行虚构数据。完成后运行你能运行的检查，给我产出文件路径、检查结果与尚未验证项。

如需写入文件或运行系统命令，Claude Code 可能请求授权；应审查工具动作，不要为了省事开放所有权限。

## 5. 三个概念一次记住

- **CLAUDE.md**：项目长期约定和上下文，不是万能保障。
- **Skill**：把重复的方法固化为可复用步骤，通常位于 `.claude/skills/<name>/SKILL.md`。
- **Subagent**：有独立上下文的专门助手，适合文件搜索、研究、审核等会占用大量上下文的任务，不是越多越好。

## 6. 合格标准

你能够准确指出：输入文件、修改了什么、执行了哪条测试、测试是否通过、下一次如何复现。做不到这一点，就还没有完成。

下一步：[10 个团队的应用场景](01-ten-teams.md) → [Agent 六模式](02-agent-patterns.md)。

