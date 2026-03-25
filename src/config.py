from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
ASSETS_DIR = BASE_DIR / "assets"

DOCUMENTS_PATH = RAW_DIR / "synthetic_documents.csv"
CLAUSES_PATH = PROCESSED_DIR / "clauses.csv"
SIMILARITY_PATH = PROCESSED_DIR / "similar_pairs.csv"
FINDINGS_PATH = PROCESSED_DIR / "findings.csv"
SUMMARY_PATH = PROCESSED_DIR / "summary.json"

BASE_MODEL_NAME = "google/flan-t5-small"
