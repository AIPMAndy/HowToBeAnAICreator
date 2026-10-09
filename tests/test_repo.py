from pathlib import Path
import unittest, json, re, csv
ROOT=Path(__file__).resolve().parents[1]
class RepoQualityTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.cards=json.loads((ROOT/'data/cards.json').read_text(encoding='utf-8'))
 def test_card_count_and_unique_id(self):
  self.assertEqual(len(self.cards),59)
  self.assertEqual(len({c['id'] for c in self.cards}),len(self.cards))
 def test_group_chapters(self):
  self.assertEqual(len({x['category'] for x in self.cards}),10)
  self.assertEqual(len(list((ROOT/'book').glob('*.md'))),10)
 def test_fields_and_outputs(self):
  for x in self.cards:
   for field in ('id','title','category','steps','output','pitfall','minutes','evidence','priority'):
    self.assertTrue(x.get(field),f'{x["id"]} lacks {field}')
   self.assertGreater(len(x['steps']),1,x['id'])
   self.assertGreaterEqual(x['minutes'],1)
   self.assertIn(x['priority'],('中','高'))
   self.assertIn(x['evidence'],('官方规则','实践建议'))
 def test_copy_data_matches(self):
  website=json.loads((ROOT/'docs/data/cards.json').read_text())
  self.assertEqual(website,self.cards)
 def test_offline_embeds_everything(self):
  s=(ROOT/'docs/offline.html').read_text()
  self.assertIn('id="embedded-data"',s)
  self.assertNotIn('assets/site.js',s)
  self.assertNotIn('assets/site.css',s)
  self.assertIn('01-01',s)
 def test_30day_plan(self):
  with (ROOT/'templates/30-day-plan.csv').open(encoding='utf-8-sig') as fp:r=list(csv.DictReader(fp))
  self.assertEqual(len(r),30)
  self.assertEqual([x['Day'] for x in r],[f'D{i:02d}' for i in range(1,31)])
 def test_sites(self):
  self.assertTrue((ROOT/'assets/hero.png').stat().st_size>30000)
  self.assertTrue((ROOT/'docs/index.html').exists())
  self.assertTrue((ROOT/'docs/examples.html').exists())
  self.assertTrue((ROOT/'docs/downloads/30-day-plan.csv').exists())
 def test_source_licenses(self):
  self.assertTrue((ROOT/'LICENSE').exists())
  self.assertTrue((ROOT/'LICENSE-CONTENT.md').exists())
  self.assertTrue((ROOT/'CONTRIBUTING.md').exists())
if __name__=='__main__':unittest.main()

class AdversarialQualityTests(unittest.TestCase):
    """Guard against regressions found during the second review; standard library only."""
    @classmethod
    def setUpClass(cls):
        cls.cards=json.loads((ROOT/'data/cards.json').read_text(encoding='utf-8'))
        cls.site=(ROOT/'docs/index.html').read_text(encoding='utf-8')
        cls.offline=(ROOT/'docs/offline.html').read_text(encoding='utf-8')
    @staticmethod
    def section(source, element):
        m=re.search(r'<div id="'+re.escape(element)+r'"[^>]*>(.*?)</div>',source,re.S)
        assert m, element+' not found'
        return m.group(1)
    def test_every_risk_has_source_and_review_date(self):
        for c in self.cards:
            if c['evidence']=='官方规则':
                self.assertGreater(len(c['sources']),0,c['id'])
                self.assertRegex(c.get('reviewed_on',''),r'^\d{4}-\d{2}-\d{2}$')
                self.assertTrue(all(url.startswith('https://') for url in c['sources']))
    def test_original_cards_have_usable_examples(self):
        enriched=[c for c in self.cards if c.get('example') and c.get('if_blocked')]
        self.assertGreaterEqual(len(enriched),15)
        self.assertTrue(any(c['id']=='02-03' for c in enriched))
        self.assertTrue(any(c['id']=='09-04' for c in enriched))
    def test_all_card_links_https(self):
        for c in self.cards:
            for url in c['sources']:
                self.assertTrue(url.startswith('https://'),f'{c["id"]}: {url}')
    def test_full_example_available_web_and_offline(self):
        for document in (self.site,self.offline):
            section=self.section(document,'exampleContents')
            self.assertGreaterEqual(section.count('<pre>'),2)
            self.assertGreaterEqual(section.count('<table>'),1)
            self.assertIn('严禁',section)
    def test_offline_is_self_contained_and_has_embedded_tasks(self):
        self.assertIn('id="embedded-data"',self.offline)
        m=re.search(r'<script id="embedded-tasks" type="application/json">(.*?)</script>',self.offline,re.S)
        self.assertIsNotNone(m)
        self.assertEqual(len(json.loads(m.group(1))),30)
        self.assertNotRegex(self.offline,r'<script[^>]+src=')
        self.assertNotRegex(self.offline,r'<link[^>]+rel="stylesheet"')
        self.assertIn('download="30-day-plan.csv"',self.offline)
    def test_30_day_online_json_matches_csv(self):
        tasks=json.loads((ROOT/'docs/data/tasks.json').read_text(encoding='utf-8'))
        with (ROOT/'templates/30-day-plan.csv').open(encoding='utf-8-sig') as fp:
            rows=list(csv.DictReader(fp))
        self.assertEqual(len(tasks),30)
        self.assertEqual([(t['id'],t['task'],t['output']) for t in tasks],[(r['Day'],r['任务'],r['验收交付']) for r in rows])
    def test_local_relative_navigation_targets_exist(self):
        from urllib.parse import urlsplit,unquote
        anchors=set(re.findall(r'\bid="([^"]+)"',self.site))
        for url in re.findall(r'<a\b[^>]*\bhref="([^"]+)"',self.site):
            if not url or url.startswith(('https:','http:','mailto:','data:')):continue
            if url.startswith('#'):
                self.assertIn(unquote(url[1:]),anchors,f'broken anchor {url}')
            else:
                parts=urlsplit(url);target=ROOT/'docs'/unquote(parts.path)
                self.assertTrue(target.exists(),f'broken linked file: {url}')
    def test_generated_webpage_sources_are_same(self):
        src=(ROOT/'examples/ai-resume-walkthrough.md').read_text(encoding='utf-8')
        out=self.section(self.site,'exampleContents')
        for phrase in ['原始经历','社群运营专员','严禁伪造真实求职成果']:
            self.assertIn(phrase,src)
        self.assertIn('社群运营专员',out)
        self.assertIn('社群运营专员',(ROOT/'docs/examples.html').read_text())
    def test_build_is_deterministic(self):
        import subprocess,hashlib
        paths=[ROOT/'docs/index.html',ROOT/'docs/examples.html',ROOT/'docs/offline.html',ROOT/'docs/data/cards.json',ROOT/'docs/data/tasks.json']
        before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        subprocess.run(['python3',str(ROOT/'tools/build.py')],check=True,capture_output=True)
        after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        self.assertEqual(before,after)
