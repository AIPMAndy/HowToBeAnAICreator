#!/usr/bin/env python3
"""Build markdown chapters, site data and offline single-file HTML from canonical data."""
from pathlib import Path
import csv, json, html, re, hashlib
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data'/'cards.json';OUT=ROOT/'book';WEB=ROOT/'docs'
cards=json.loads(D.read_text(encoding='utf8'))
assert len(cards)>=50 and len({x['id'] for x in cards})==len(cards)
from collections import OrderedDict
groups=OrderedDict()
for c in cards:groups.setdefault(c['category'],[]).append(c)
for i,(k,rows) in enumerate(groups.items(),1):
 lines=[f'# {i:02d} · {k}', '', '> 每条都包含行动、时间预算、验收物和常见错误。时间是建议，按实际情况调整。','']
 for r in rows:
  lines+=[f"## {r['id']} {r['title']}",'',f"- **建议时间**：约 {r['minutes']} 分钟",f"- **成本**：{r['cost']}",f"- **依据性质**：{r['evidence']}（不等于平台算法）",'','**照着做：**','']
  lines.extend(f'{n}. {a}' for n,a in enumerate(r['steps'],1))
  lines+=['',f"**验收物：**{r['output']}",f"**注意：**{r['pitfall']}"]
  if r['sources']:lines+=['','**原始入口/依据：**']+[f'- {url}' for url in r['sources']]
  lines+=['','---','']
 (OUT/f'{i:02d}-{k}.md').write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')
(WEB/'data'/'cards.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# 30 day plan
TASKS=[
('确定账号用户','一句定位描述'),('研究10个对标账号','账号链接与受众'),('研究10个低粉对标','同账号基线记录'),('搜集15个选题','有来源的选题行'),('再搜15个选题','选题库共30行'),('实测排名前3的选题','工具可用性与截图'),('发布第1条','作品链接与原始文件'),
('记录第1条24h表现','真实指标快照'),('实测第二个任务','原始输入与输出'),('发布第2条','作品链接'),('评论区采集10条问题','用户问题清单'),('制作第三条脚本','分镜脚本'),('发布第3条','作品链接'),('首次横向复盘','本周假设与实验计划'),
('研究表现好的5条同类内容','选题共性说明'),('制作第4条','完整素材'),('发布第4条','作品链接'),('整理5个高频问题','系列内容提纲'),('制作第5条','同类选题不同开头'),('发布第5条','作品链接'),('明确一个系列','3集连续选题'),
('制作系列第1集','实测记录'),('发布系列第1集','作品链接'),('制作系列第2集','实际对比内容'),('发布系列第2集','作品链接'),('整理最好的3条作品','作品集与统计日期'),('完成一页媒体介绍','真实数据与能力'),('找5个适合的品牌','官方公开合作方式'),('提出个性化合作方案','发出记录，不群发骚扰'),('完成月度复盘','保留方向+下月实验')]
assert len(TASKS)==30
task_objects=[{'id':f'D{i:02d}','task':a,'output':b} for i,(a,b) in enumerate(TASKS,1)]
(WEB/'data'/'tasks.json').write_text(json.dumps(task_objects,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (ROOT/'templates'/'30-day-plan.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.writer(f);writer.writerow(['Day','任务','验收交付','完成状态','日期','备注'])
 for i,(act,out) in enumerate(TASKS,1):writer.writerow([f'D{i:02d}',act,out,'待开始','',''])
with (ROOT/'templates'/'topic-library.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.writer(f);writer.writerow(['发现日期','平台','作者/粉丝量','作品链接','公开播放/阅读(未知则留空)','点赞','收藏','评论','同类内容基线','问题与评论需求','独立验证来源','我能复现吗','估计耗时','评分','状态','发布日期','结果链接'])
 writer.writerow(['2026-10-09','（示例）','账号A/1000','示例，不是真实链接','','600','','','近10条同类点赞中位40','想学提示词','需补另外两个来源','待验证','20','待评分','待验证','',''])
with (ROOT/'templates'/'metrics.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.writer(f);writer.writerow(['平台','作品链接','发布时间','选题','复盘时间点','真实阅读/播放','真实曝光(如有)','收藏','评论','新增关注','咨询数','制作时间','观察事实','下一个实验','备注'])
with (ROOT/'templates'/'deals.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.writer(f);writer.writerow(['品牌','公开联系方法','产品/受众匹配理由','询盘日期','当前阶段','报价金额','交付平台/数量','授权范围','审核/修改','合同日期','发布日期','验收日期','已收款','待收款','下一步'])
# Render the complete real first-post example into the web page and offline page.
# Tiny dependency-free Markdown converter, scoped to the subset used in examples.
def convert_example(md):
 lines=md.splitlines();out=[];i=0;paragraph=[]
 def inline(t):
  t=html.escape(t)
  return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
 def flush():
  if paragraph:
   out.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
 while i<len(lines):
  line=lines[i]; st=line.strip()
  if not st:flush();i+=1;continue
  if st.startswith('```'):
   flush();block=[];i+=1
   while i<len(lines) and not lines[i].strip().startswith('```'):
    block.append(lines[i]);i+=1
   out.append('<pre><code>'+html.escape('\n'.join(block))+'</code></pre>');i+=1;continue
  if st.startswith('|') and i+1<len(lines) and re.match(r'^\|[\s:|\-]+\|$',lines[i+1].strip()):
   flush();heads=[x.strip() for x in st.strip('|').split('|')];i+=2;trs=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    vals=[x.strip() for x in lines[i].strip().strip('|').split('|')]
    trs.append('<tr>'+''.join('<td>'+inline(v)+'</td>' for v in vals)+'</tr>');i+=1
   out.append('<table><thead><tr>'+''.join('<th>'+inline(v)+'</th>' for v in heads)+'</tr></thead><tbody>'+''.join(trs)+'</tbody></table>');continue
  if st.startswith('#'):
   flush();depth=min(len(st)-len(st.lstrip('#'))+2,4);out.append(f'<h{depth}>'+inline(st.lstrip('# ').strip())+f'</h{depth}>');i+=1;continue
  if st.startswith('> '):
   flush();out.append('<blockquote>'+inline(st[2:])+'</blockquote>');i+=1;continue
  if re.match(r'^\d+\. ',st) or st.startswith('- '):
   flush();ordered=bool(re.match(r'^\d+\. ',st));tag='ol' if ordered else 'ul';items=[]
   while i<len(lines):
    text=lines[i].strip()
    if (ordered and not re.match(r'^\d+\. ',text)) or (not ordered and not text.startswith('- ')):break
    item=re.sub(r'^\d+\. ', '',text) if ordered else text[2:]
    items.append('<li>'+inline(item)+'</li>');i+=1
   out.append('<'+tag+'>'+''.join(items)+'</'+tag+'>');continue
  paragraph.append(st);i+=1
 flush();return '\n'.join(out)

example_html=convert_example((ROOT/'examples'/'ai-resume-walkthrough.md').read_text(encoding='utf-8'))
example_path=WEB/'index.html';web_text=example_path.read_text(encoding='utf8')
web_text=re.sub(r'(<div id="exampleContents" class="example-contents">).*?(</div>)',lambda m:m.group(1)+example_html+m.group(2),web_text,count=1,flags=re.S)
example_path.write_text(web_text,encoding='utf8')
# make offline HTML: inline local CSS, JS and canonical JSON, no network or framework needed
homepage=(WEB/'index.html').read_text(encoding='utf8')
css=(WEB/'assets'/'site.css').read_text(encoding='utf8')
js=(WEB/'assets'/'site.js').read_text(encoding='utf8')
homepage=homepage.replace('<link rel="stylesheet" href="assets/site.css">',f'<style>{css}</style>')
homepage=re.sub(r'<link rel="icon"[^>]+>', '',homepage)
homepage=homepage.replace('<script src="assets/site.js" defer></script>',
'<script id="embedded-data" type="application/json">'+json.dumps(cards,ensure_ascii=False).replace('</','<\\/')+'</script><script id="embedded-tasks" type="application/json">'+json.dumps(task_objects,ensure_ascii=False).replace('</','<\\/')+'</script><script>'+js+'</script>')
# offline links stay useful: complete example is in the file; 30-day CSV is embedded as download data URL.
import base64
csv64=base64.b64encode((ROOT/'templates'/'30-day-plan.csv').read_bytes()).decode('ascii')
homepage=homepage.replace('href="examples.html"','href="#first-example"').replace('href="downloads/30-day-plan.csv"',f'href="data:text/csv;base64,{csv64}" download="30-day-plan.csv"')
(WEB/'offline.html').write_text(homepage,encoding='utf8')
# sync CSV for hosted website so links do not leave Pages mount root
(WEB/'downloads').mkdir(exist_ok=True)
(WEB/'downloads'/'30-day-plan.csv').write_bytes((ROOT/'templates'/'30-day-plan.csv').read_bytes())
print(f'built {len(cards)} cards / {len(groups)} chapters / 30 days / offline {len(homepage):,} chars')
