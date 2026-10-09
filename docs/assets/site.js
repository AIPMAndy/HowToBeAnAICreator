(()=>{'use strict';
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const KEY='aicreator-progress-v2',OLD='aicreator-progress-v1';
const state={cards:[],days:[],category:'',priority:'',query:'',undone:false,dayUndone:false,done:{},dayDone:{},storageOk:true};
const isObject=o=>Boolean(o)&&typeof o==='object'&&!Array.isArray(o);
function msg(s,warn=false){const el=$('#saveStatus');el.textContent=s;el.classList.toggle('warn',warn)}
function load(){
 try{const raw=localStorage.getItem(KEY);const old=localStorage.getItem(OLD);
   const obj=raw?JSON.parse(raw):{done:old?JSON.parse(old):{},days:{}};
   if(isObject(obj)){state.done=isObject(obj.done)?obj.done:{};state.dayDone=isObject(obj.days)?obj.days:{}}
   localStorage.setItem('aicreator-storage-probe','1');localStorage.removeItem('aicreator-storage-probe')
 }catch{state.storageOk=false;state.done={};state.dayDone={}}
}
function save(){
 if(!state.storageOk)return;
 try{localStorage.setItem(KEY,JSON.stringify({version:2,done:state.done,days:state.dayDone}))}
 catch{state.storageOk=false;msg('当前浏览器不允许保存进度。请使用“导出进度”备份，或换正常浏览模式。',true)}
}
function hydrate(){const valid=new Set(state.cards.map(c=>c.id));state.done=Object.fromEntries(Object.entries(state.done).filter(([k,v])=>valid.has(k)&&v===true));const dayset=new Set(state.days.map(d=>d.id));state.dayDone=Object.fromEntries(Object.entries(state.dayDone).filter(([k,v])=>dayset.has(k)&&v===true));save()}
function upd(){const n=state.cards.filter(c=>state.done[c.id]).length;$('#progressCount').textContent=`${n} / ${state.cards.length}`;$('#progressBar').style.width=(state.cards.length?n/state.cards.length*100:0)+'%';$('#dayProgress').textContent=`${state.days.filter(d=>state.dayDone[d.id]).length} / ${state.days.length} 天已完成`}
function filtered(){let q=state.query.toLocaleLowerCase().trim();return state.cards.filter(c=>(!state.category||c.category===state.category)&&(!state.priority||c.priority===state.priority)&&(!state.undone||!state.done[c.id])&&(!q||[c.id,c.title,c.category,c.output,c.pitfall,c.cost,c.evidence,c.example||'',c.if_blocked||'',...c.steps].join(' ').toLocaleLowerCase().includes(q)))}
function renderCards(){const arr=filtered();$('#resultCount').textContent=`找到 ${arr.length} 条操作卡 · 每条都有步骤、交付物和避坑提示`;$('#empty').hidden=arr.length!==0;
 $('#cards').innerHTML=arr.map(c=>`<article class="entry" id="card-${esc(c.id)}"><div class="entry-top"><span class="entry-num">${esc(c.id)} · ${esc(c.category)}</span><span class="entry-time">约 ${esc(c.minutes)} 分钟</span></div><h3>${esc(c.title)}</h3><h4>照着操作</h4><ol>${c.steps.map(x=>`<li>${esc(x)}</li>`).join('')}</ol><div class="entry-output"><b>验收交付</b>${esc(c.output)}</div>${c.example?`<div class="entry-example"><b>实际例子</b>${esc(c.example)}</div>`:''}${c.if_blocked?`<div class="entry-blocked"><b>卡住时</b>${esc(c.if_blocked)}</div>`:''}<p class="entry-pitfall">⚠️ ${esc(c.pitfall)}</p><div class="entry-meta">优先级：${c.priority==='高'?'先做':'进阶'} · 依据：${esc(c.evidence)} · 成本：${esc(c.cost)}</div>${c.sources?.length?`<div class="entry-links">${c.sources.map((u,i)=>`<a href="${esc(u)}" target="_blank" rel="noopener noreferrer">一手来源 ${i+1} ↗</a>`).join('')}</div>`:''}<div class="entry-actions"><label class="done-label"><input type="checkbox" data-id="${esc(c.id)}" ${state.done[c.id]?'checked':''}><span>${state.done[c.id]?'已完成':'标记完成'}</span></label><button class="copy-btn" type="button" data-copy="${esc(c.id)}">复制操作卡</button></div></article>`).join('');upd()}
function renderDays(){const list=state.days.filter(d=>!state.dayUndone||!state.dayDone[d.id]);$('#dayGrid').innerHTML=list.map(d=>`<article class="day-card ${state.dayDone[d.id]?'is-done':''}"><label><input type="checkbox" data-day="${esc(d.id)}" ${state.dayDone[d.id]?'checked':''}><strong><b>${esc(d.id)}</b>${esc(d.task)}</strong></label><p>验收：${esc(d.output)}</p></article>`).join('');upd()}
function category(cat){state.category=cat;$('#category').value=cat;[...$('#pills').children].forEach(x=>x.classList.toggle('active',x.dataset.category===cat));renderCards()}
function download(name,content,type='application/json;charset=utf-8'){
 const blob=new Blob([content],{type});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;a.style.display='none';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),3000)
}
function copyFallback(text,allowPrompt){const node=document.createElement('textarea');node.value=text;node.style.cssText='position:fixed;top:0;left:0;opacity:0;';document.body.append(node);node.focus();node.select();let ok=false;try{ok=document.execCommand('copy')}catch{}node.remove();if(!ok){if(allowPrompt)window.prompt('自动复制未获授权。请选择以下文字后复制：',text);return false}return true}
async function copy(text,allowPrompt=true){try{if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(text);return true}}catch{}return copyFallback(text,allowPrompt)}
function init(){const categories=[...new Set(state.cards.map(c=>c.category))];$('#category').innerHTML='<option value="">全部分类</option>'+categories.map(c=>`<option value="${esc(c)}">${esc(c)}</option>`).join('');$('#pills').innerHTML=['',...categories].map(c=>`<button type="button" data-category="${esc(c)}" class="${c===''?'active':''}">${esc(c||'全部')}</button>`).join('');$('#statCards').textContent=state.cards.length;
 $('#search').addEventListener('input',e=>{state.query=e.target.value;renderCards()});$('#category').addEventListener('change',e=>category(e.target.value));$('#priority').addEventListener('change',e=>{state.priority=e.target.value;renderCards()});$('#unfinishedOnly').addEventListener('change',e=>{state.undone=e.target.checked;renderCards()});$('#daysUnfinished').addEventListener('change',e=>{state.dayUndone=e.target.checked;renderDays()});
 $('#clear').addEventListener('click',()=>{state.query='';state.priority='';state.undone=false;$('#unfinishedOnly').checked=false;$('#search').value='';$('#priority').value='';category('')});$('#pills').addEventListener('click',e=>{const b=e.target.closest('button[data-category]');if(b)category(b.dataset.category)});
 $('#cards').addEventListener('change',e=>{const id=e.target.dataset.id;if(id){state.done[id]=e.target.checked;save();renderCards()}});
 $('#dayGrid').addEventListener('change',e=>{const id=e.target.dataset.day;if(id){state.dayDone[id]=e.target.checked;save();renderDays()}});
 $('#cards').addEventListener('click',async e=>{const b=e.target.closest('button[data-copy]');if(!b)return;const c=state.cards.find(x=>x.id===b.dataset.copy);if(!c)return;const t=[c.id+' '+c.title,'操作：',...c.steps.map((x,i)=>(i+1)+'. '+x),'验收：'+c.output,'避坑：'+c.pitfall,...(c.example?['示例：'+c.example]:[]),...(c.if_blocked?['卡住时：'+c.if_blocked]:[])].join('\n');const ok=await copy(t);b.textContent=ok?'已复制 ✓':'请手动复制';setTimeout(()=>b.isConnected&&(b.textContent='复制操作卡'),2000)});
 $('#exportProgress').addEventListener('click',()=>{download('AI博主打卡进度.json',JSON.stringify({schema:'aicreator-progress',version:2,exportedAt:new Date().toISOString(),done:state.done,days:state.dayDone},null,2));msg('进度备份已下载。可在另一设备使用“导入进度 JSON”继续。')});
 $('#importProgress').addEventListener('change',async e=>{const file=e.target.files?.[0];if(!file)return;try{if(file.size>200000)throw Error('文件超过 200KB');let obj=JSON.parse(await file.text());if(!isObject(obj)||obj.schema!=='aicreator-progress'||obj.version!==2||!isObject(obj.done)||!isObject(obj.days))throw Error('格式或版本不匹配');const ids=new Set(state.cards.map(c=>c.id)),days=new Set(state.days.map(d=>d.id));const newDone={},newDays={};for(const [k,v] of Object.entries(obj.done)){if(ids.has(k)&&typeof v==='boolean'&&v)newDone[k]=true}for(const [k,v] of Object.entries(obj.days)){if(days.has(k)&&typeof v==='boolean'&&v)newDays[k]=true}state.done=newDone;state.dayDone=newDays;save();renderCards();renderDays();msg('进度导入成功。导入会替换当前浏览器的原有进度。')}catch(err){msg('导入失败：'+err.message,true)}e.target.value=''});
 $('#resetProgress').addEventListener('click',()=>{if(!confirm('确认清空操作卡和30天任务的本机勾选记录？建议先导出备份。'))return;state.done={};state.dayDone={};save();renderCards();renderDays();msg('进度已清空。')});
 renderCards();renderDays();if(!state.storageOk)msg('浏览器禁止本地存储：本页勾选只在当前会话有效。建议及时导出进度 JSON。',true);
 if(location.hash.startsWith('#card-')){const id=decodeURIComponent(location.hash.slice(6));const c=state.cards.find(x=>x.id===id);if(c){state.query='';state.priority='';state.undone=false;state.category='';renderCards();requestAnimationFrame(()=>document.getElementById('card-'+id)?.scrollIntoView({block:'center'}))}}
}
async function loadJson(path,embedded){const script=$(embedded);if(script)return JSON.parse(script.textContent);const r=await fetch(path);if(!r.ok)throw Error('HTTP '+r.status);return r.json()}
async function start(){load();try{[state.cards,state.days]=await Promise.all([loadJson('data/cards.json','#embedded-data'),loadJson('data/tasks.json','#embedded-tasks')]);if(!Array.isArray(state.cards)||!Array.isArray(state.days))throw Error('数据格式错误');hydrate();init()}catch(err){$('#resultCount').textContent='加载操作卡失败：'+err.message+'。可改用离线单文件版本。';console.error(err)}}
$('#copyWechat').addEventListener('click',async()=>{const id=$('#wechatId').textContent;const ok=await copy(id,false);$('#contactStatus').textContent=ok?'微信号 '+id+' 已复制':'请手动复制微信号：'+id;$('#copyWechat').focus({preventScroll:true})});
start();
})();
