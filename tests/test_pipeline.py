import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CLAUSES_PATH, FINDINGS_PATH, SUMMARY_PATH
from src.pipeline import run_pipeline


class PipelineTestCase(unittest.TestCase):
    def test_pipeline_runs_in_fallback_mode(self):
        summary = run_pipeline(use_llm=False)
        self.assertTrue(CLAUSES_PATH.exists())
        self.assertTrue(FINDINGS_PATH.exists())
        self.assertTrue(SUMMARY_PATH.exists())
        self.assertGreaterEqual(summary["findings"], 1)
        self.assertEqual(summary["review_mode"], "fallback")


if __name__ == "__main__":
    unittest.main()
