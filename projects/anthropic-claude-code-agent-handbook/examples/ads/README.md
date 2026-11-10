# 练习｜从广告 CSV 到两个专业子 Agent

这是公开报告中增长营销场景的**独立教学复刻**。样本 CSV 为人工虚构，脚本不连接任何广告平台，也不会调用 Claude。

## 一、只用 Python 先跑确定性分析

在本项目根目录执行：

```bash
python3 scripts/ad_audit.py --input examples/ads/sample_ads.csv --output outputs/ad_report.csv
python3 -m unittest discover -s tests -v
```

脚本默认将 CTR 低于 2% 的广告标为“建议复核”，阈值只是演示参数，可使用 `--min-ctr 0.03` 调整。没有曝光量时不计算 CTR；点击为零时 CPC 留空。**这不是平台行业基准。**

## 二、人工核查报告

打开 `outputs/ad_report.csv`。至少检查一条 1000 曝光、10 点击的样本，CTR 应等于 0.01。比较总点击与原始 CSV 是否一致。记录：哪些问题是定量数据能回答的，哪些必须依赖创意和受众判断。

## 三、交给 Claude Code

> 请读取 outputs/ad_report.csv 和 prompts/marketing-agents.md。只生成标题、描述两组候选 CSV 草稿，并以质量审核者的标准审核，写出每条候选的事实依据与风险。不要连接任何广告平台，不要真实投放。

有权限并正确配置时，可让 Claude Code 使用多个专业子 Agent；否则可以依次用两个 Prompt 跑相同职责，不必强行多 Agent。

## 四、验收

- 所有候选文本符合规定字符数（正式上线以目标平台现行规则为准）。
- 事实主张能从产品资料验证，不能编造收益。
- 输出有假设标签、版本号和人工审批记录。
- 没有外部投放动作。

## 五、想继续？

先做十条样本的人工评估，再决定是否接 MCP / API。真实广告、账户授权、预算与隐私信息不应放进本开源仓库。

