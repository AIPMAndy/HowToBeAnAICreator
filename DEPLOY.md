# 一键部署思路（无需数据库、无需云函数）

### 1. 建仓库

本项目已发布至公开仓库 [AIPMAndy/HowToBeAnAICreator](https://github.com/AIPMAndy/HowToBeAnAICreator)。首次发布自己的副本时，新建 Public 仓库，把 ZIP 文件解压后上传到仓库根目录或使用 `git push`。

### 2. 开启 GitHub Pages

仓库 → Settings → Pages → Deploy from a branch → 分支 `main` → 文件夹 `/docs` → Save。

本仓库已启用 GitHub Pages，站点地址：

`https://AIPMAndy.github.io/HowToBeAnAICreator/`

部署来源为 `main` 分支的 `/docs` 目录；后续推送会自动触发更新，部署结果可在仓库 Actions 中查看。

### 3. 本地调试

```bash
python3 tools/build.py
python3 -m http.server 8000 --directory docs
```

打开 `http://localhost:8000/`。下载 `docs/offline.html` 可以直接双击使用，数据与脚本都内嵌在单文件内。

### 4. 更新内容

只编辑 `data/cards.json`（卡片唯一数据源）。执行 `python3 tools/build.py` 更新网页版数据、离线版、章节和 CSV。检查：

```bash
python3 -m unittest discover -s tests -v
```

### 5. 最终发布前

检查仓库链接、封面、手机端导航、搜索、筛选、离线模式、链接跳转，以及法律和平台规则日期。`README` 已提供在线互动手册入口。


## 部署后的手动验收

1. 首页操作卡应显示 **59** 条，30 天日历显示 **30** 条。
2. 检索“低粉爆款”能出现相关操作卡；选择“只看未完成”会改变列表。
3. 给任意一条操作卡、任意一天任务打勾；重载页面检查本地浏览器能否保留。
4. 下载“进度 JSON”，清空后再导入，恢复计数。该文件只保存任务状态，不保存私人简历、商单或评论。
5. “完整跟拍案例”有输入、Prompt、合格输出和完整分镜；离线 HTML 不应请求本地以外的脚本和数据。
6. 用 390px 宽的手机视口打开，检查没有横向滚动、列表与操作按钮可以点击。
7. 确认站点位于 `https://aipmandy.github.io/HowToBeAnAICreator/`，并检查最新部署工作流成功。
