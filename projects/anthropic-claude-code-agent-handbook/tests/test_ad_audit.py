import csv
import importlib.util
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ad_audit", ROOT / "scripts" / "ad_audit.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def row(impressions="1000", clicks="10", spend="30.00"):
    return {"ad_id": "T1", "campaign": "test", "headline": "demo",
            "description": "demo text", "impressions": impressions,
            "clicks": clicks, "spend": spend}


class TestAdAudit(unittest.TestCase):
    def test_ctr_and_cpc(self):
        output = mod.audit_row(row())
        self.assertEqual(output["ctr"], "0.01")
        self.assertEqual(output["cpc"], "3.0000")
        self.assertEqual(output["status"], "review_candidate")

    def test_good_ctr(self):
        self.assertEqual(mod.audit_row(row(clicks="30"))["status"], "not_flagged")

    def test_zero_impressions(self):
        output = mod.audit_row(row(impressions="0", clicks="0"))
        self.assertEqual(output["ctr"], "")
        self.assertEqual(output["cpc"], "")
        self.assertEqual(output["status"], "no_impressions")

    def test_zero_clicks(self):
        output = mod.audit_row(row(clicks="0"))
        self.assertEqual(output["cpc"], "")

    def test_invalid_clicks(self):
        with self.assertRaises(ValueError):
            mod.audit_row(row(impressions="1", clicks="2"))

    def test_negative_spend(self):
        with self.assertRaises(ValueError):
            mod.audit_row(row(spend="-1"))

    def test_missing_columns(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "bad.csv"
            source.write_text("ad_id,clicks\nA,2\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                mod.audit_csv(source, Path(temp) / "out.csv", Decimal("0.02"))

    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "out.csv"
            n = mod.audit_csv(ROOT / "examples" / "ads" / "sample_ads.csv",
                              destination, Decimal("0.02"))
            self.assertEqual(n, 4)
            with destination.open(newline="", encoding="utf-8") as f:
                results = list(csv.DictReader(f))
            self.assertEqual(results[0]["status"], "review_candidate")
            self.assertEqual(results[1]["status"], "not_flagged")
            self.assertEqual(results[2]["status"], "no_impressions")


if __name__ == "__main__":
    unittest.main()

