from pathlib import Path
import json,re,subprocess,tempfile,unittest,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
U='https://aipmandy.github.io/HowToBeAnAICreator/topic-lab.html'
class TopicLabTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.h=(R/'docs/topic-lab.html').read_text()
    def test_metadata(self):
        self.assertIn('rel="canonical" href="'+U+'"',self.h)
        self.assertEqual(self.h.count('<h1>'),1)
        m=re.search(r'<script type="application/ld\+json">(.+?)</script>',self.h,re.S)
        d=json.loads(m.group(1));self.assertEqual(d['@type'],'WebApplication')
        self.assertEqual(d['url'],U)
        self.assertEqual(d['publisher']['url'],'https://www.a6no1.cn/')
    def test_controls(self):
        for s in ['topicForm','exportCsv','clearAll','rows','localStorage','csv(s)','const esc=','https:','confirm(','AIPMAndy','https://metaver.vip/services']:
            self.assertIn(s,self.h)
        self.assertNotIn('fetch(',self.h)
    def test_links(self):
        self.assertIn(U,(R/'docs/offline.html').read_text())
        self.assertIn('href="topic-lab.html"',(R/'docs/index.html').read_text())
        xml=ET.fromstring((R/'docs/sitemap.xml').read_text())
        self.assertIn(U,[x.text for x in xml.iter() if x.tag.endswith('loc')])
    def test_js_syntax(self):
        scripts=re.findall(r'<script>(.*?)</script>',self.h,re.S)
        self.assertEqual(len(scripts),1)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'app.js';p.write_text(scripts[0])
            r=subprocess.run(['node','--check',str(p)],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
