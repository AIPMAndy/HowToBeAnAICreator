# 将项目发布到自己的 GitHub（3 分钟操作）

本项目已于 **2026-10-09** 发布到公开仓库 [AIPMAndy/HowToBeAnAICreator](https://github.com/AIPMAndy/HowToBeAnAICreator)，并配置 GitHub Pages：[在线互动手册](https://aipmandy.github.io/HowToBeAnAICreator/)。当前仓库后续更新只需提交改动后 `git push`；以下创建步骤供首次发布或 Fork 参考。

## 最简单的网页上传方式

1. 打开 https://github.com/new
2. Owner 选 `AIPMAndy`；Repository name 输入 `HowToBeAnAICreator`；建议选 **Public**。
3. 不要勾选“Add a README file”，因为压缩包里已经有 README。
4. 创建仓库，然后把本项目压缩包解压到电脑，用 Git 将完整目录一次推上去；GitHub 的网页上传适合少量文件，包含数十文件时推荐下面的 Git 命令。

## 使用 GitHub CLI（推荐）

先安装 GitHub CLI，并通过 `gh auth login` 登录自己的账号。确保当前终端所在位置是项目文件夹，然后执行：

```bash
cd HowToBeAnAICreator
git init -b main
git add .
git commit -m "feat: launch AI creator open-source playbook"
gh repo create AIPMAndy/HowToBeAnAICreator --public --source=. --remote=origin --push
```

注意：以上创建命令只能在尚不存在同名仓库时执行。

## 使用 Git（已在网页创建空仓库）

```bash
cd HowToBeAnAICreator
git init -b main
git add .
git commit -m "feat: launch AI creator open-source playbook"
git remote add origin https://github.com/AIPMAndy/HowToBeAnAICreator.git
git push -u origin main
```

## 开通免费网页

进入新仓库 `Settings → Pages`，选择 `Deploy from a branch`、分支 `main`、目录 `/docs`，保存。部署成功后站点才会出现在：

`https://AIPMAndy.github.io/HowToBeAnAICreator/`

如果 GitHub 提示你的仓库设置、免费套餐或安全策略无法使用 Pages，按照该账号的当前提示解决。

## 最后检查

- README 顶部封面是否出现。
- `docs/index.html` 在 Pages 中是否成功加载全部卡片。
- 手机是否能输入关键词搜索并打勾。
- `docs/offline.html` 下载后能否在无网络情况下打开。
- 一手来源链接、商单及粉丝口径是否真实。
