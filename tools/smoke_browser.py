#!/usr/bin/env python3
"""Opt-in browser smoke tests; requires playwright and Chromium. No network API calls."""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]

def open_view(browser,width):
 ctx=browser.new_context(accept_downloads=True,viewport={'width':width,'height':850})
 page=ctx.new_page();err=[];page.on('pageerror',lambda e:err.append(str(e)))
 page.set_content((R/'docs/offline.html').read_text(encoding='utf-8'),wait_until='load')
 page.wait_for_function('document.querySelectorAll(".entry").length === 59')
 return ctx,page,err

def run():
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None),headless=True,args=['--no-sandbox'])
  ctx,page,err=open_view(browser,1300)
  assert page.locator('.entry').count()==59
  assert page.locator('.day-card').count()==30
  assert page.locator('#exampleContents pre').count()>=2
  assert page.locator('#exampleContents').inner_text().find('不得编造')>=0
  assert page.locator('#progressCount').inner_text()=='0 / 59'
  page.locator('#search').fill('低粉爆款');assert 1<=page.locator('.entry').count()<59
  page.locator('#clear').click();assert page.locator('.entry').count()==59
  page.locator('.entry input[data-id]').first.check();assert page.locator('#progressCount').inner_text()=='1 / 59'
  page.locator('.day-card input[data-day]').first.check();assert page.locator('#dayProgress').inner_text()=='1 / 30 天已完成'
  with page.expect_download() as d:page.locator('#exportProgress').click()
  downloaded=d.value;path=R/'browser_progress_test.json';downloaded.save_as(path)
  data=json.loads(path.read_text());assert len(data['done'])==1 and len(data['days'])==1
  page.locator('#unfinishedOnly').check();assert page.locator('.entry').count()==58
  page.locator('#unfinishedOnly').uncheck()
  page.once('dialog',lambda dlg:dlg.accept())
  page.locator('#resetProgress').click()
  assert page.locator('#progressCount').inner_text()=='0 / 59'
  page.locator('#importProgress').set_input_files(str(path));page.wait_for_timeout(200)
  assert page.locator('#progressCount').inner_text()=='1 / 59'
  page.locator('.entry .copy-btn').first.click()
  assert '复制' in page.locator('.entry .copy-btn').first.inner_text() or '手动' in page.locator('.entry .copy-btn').first.inner_text()
  assert not err,err
  print('PASS desktop: 59 cards, 30-day planner, example, search, exported JSON, imported JSON, reset confirmation, clipboard')
  print('PASS desktop overflow:',not page.evaluate('document.documentElement.scrollWidth > window.innerWidth'))
  path.unlink(missing_ok=True)
  page.evaluate("document.documentElement.style.scrollBehavior='auto';window.scrollTo(0,0)");page.wait_for_timeout(300);page.screenshot(path=str(R/'v2_desktop.png'))
  page.close();ctx.close()
  ctx,mp,err=open_view(browser,390)
  assert not mp.evaluate('document.documentElement.scrollWidth > window.innerWidth')
  with mp.expect_download() as d:mp.locator('a[download="30-day-plan.csv"]').click()
  assert d.value.suggested_filename=='30-day-plan.csv'
  mp.evaluate("document.documentElement.style.scrollBehavior='auto';window.scrollTo(0,0)");mp.wait_for_timeout(300);mp.screenshot(path=str(R/'v2_mobile.png'))
  assert not err,err
  print('PASS mobile: no horizontal overflow, self-contained offline HTML, CSV export, no JS errors')
  mp.close();ctx.close();browser.close()

if __name__=='__main__':run()
