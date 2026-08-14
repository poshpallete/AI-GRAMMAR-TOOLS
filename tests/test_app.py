import importlib
import sqlite3
import sys
import tempfile
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"


def install_engine_stubs():
    package = types.ModuleType("ai_engine")
    package.__path__ = []

    grammar = types.ModuleType("ai_engine.grammar_ai")
    grammar.grammar_engine = lambda text: (
        "This is corrected text.",
        "This is <span>corrected</span> text.",
        ["Example grammar issue"],
        "This is corrected text.",
        "This is corrected text.",
        "This is corrected text.",
        ["Review the highlighted issue."],
    )

    ocr = types.ModuleType("ai_engine.ocr_engine")
    ocr.extract_text = lambda _path: "Extracted text"

    features = types.ModuleType("ai_engine.features_ai")
    features.make_notes_ai = lambda text: f"Notes: {text}"
    features.improve_assignment_ai = lambda text: f"Improved: {text}"
    features.simplify_ai = lambda text: f"Simple: {text}"
    features.expand_ai = lambda text: f"Expanded: {text}"
    features.paragraph_ai = lambda text: f"Paragraph: {text}"

    sys.modules["ai_engine"] = package
    sys.modules["ai_engine.grammar_ai"] = grammar
    sys.modules["ai_engine.ocr_engine"] = ocr
    sys.modules["ai_engine.features_ai"] = features


class ApplicationSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(BACKEND_DIR))
        install_engine_stubs()
        cls.app_module = importlib.import_module("app")
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.app_module.DB_PATH = Path(cls.temp_dir.name) / "test.sqlite3"
        cls.app_module.init_db()
        cls.client = cls.app_module.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()
        sys.path.remove(str(BACKEND_DIR))

    def setUp(self):
        with sqlite3.connect(self.app_module.DB_PATH) as conn:
            conn.execute("DELETE FROM writing_analysis")

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_text_analysis_is_scored_and_saved(self):
        response = self.client.post(
            "/analyze-text",
            json={"text": "This are example text."},
        )
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["score"], 95)
        self.assertEqual(payload["corrected"], "This is corrected text.")

        dashboard = self.client.get("/get-dashboard-data").get_json()
        self.assertEqual(dashboard["total"], 1)
        self.assertEqual(dashboard["scores"], [95])

    def test_empty_text_returns_zero_score(self):
        response = self.client.post("/analyze-text", json={"text": "   "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["score"], 0)


if __name__ == "__main__":
    unittest.main()
