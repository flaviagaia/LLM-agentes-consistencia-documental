from __future__ import annotations

import json

import pandas as pd

from .config import DOCUMENTS_PATH, GROUND_TRUTH_PATH, RAW_DIR


DOCUMENTS = [
    {
        "document_id": "DOC-001",
        "document_name": "Mechanical Execution Guideline",
        "document_type": "guideline",
        "document_text": (
            "1. The contractor shall deliver the 3D mechanical model within 10 calendar days after kickoff. "
            "2. Quality verification shall be performed by the contractor quality lead before issue. "
            "3. Measurement for progress shall be based on isometric sheets approved by engineering. "
            "4. The applicable technical standard is ENG-VAL-01."
        ),
    },
    {
        "document_id": "DOC-002",
        "document_name": "Mechanical Annex for Field Delivery",
        "document_type": "annex",
        "document_text": (
            "1. The contractor shall deliver the 3D mechanical model within 15 calendar days after kickoff. "
            "2. Quality verification shall be performed by the client inspection team before issue. "
            "3. Measurement for progress shall be based on bill of quantities signed by planning. "
            "4. The applicable technical standard is ENG-VAL-02."
        ),
    },
    {
        "document_id": "DOC-003",
        "document_name": "Instrumentation Design Memo",
        "document_type": "memo",
        "document_text": (
            "1. The instrumentation panel list shall be delivered within 12 calendar days after kickoff. "
            "2. Quality verification shall be performed by the engineering coordinator before issue. "
            "3. Measurement for progress shall be based on approved panel list packages. "
            "4. The applicable technical standard is ENG-INS-05."
        ),
    },
    {
        "document_id": "DOC-004",
        "document_name": "Instrumentation Construction Appendix",
        "document_type": "appendix",
        "document_text": (
            "1. The instrumentation panel list shall be delivered within 12 calendar days after kickoff. "
            "2. Quality verification shall be performed by the engineering coordinator before issue. "
            "3. Measurement for progress shall be based on approved panel list packages. "
            "4. The applicable technical standard is ENG-INS-07."
        ),
    },
]

GROUND_TRUTH = [
    {
        "left_clause_id": "DOC-001-1",
        "right_clause_id": "DOC-002-1",
        "issue_type": "deadline_days",
        "expected_inconsistency": True,
    },
    {
        "left_clause_id": "DOC-001-2",
        "right_clause_id": "DOC-002-2",
        "issue_type": "responsibility",
        "expected_inconsistency": True,
    },
    {
        "left_clause_id": "DOC-001-3",
        "right_clause_id": "DOC-002-3",
        "issue_type": "measurement_basis",
        "expected_inconsistency": True,
    },
    {
        "left_clause_id": "DOC-001-4",
        "right_clause_id": "DOC-002-4",
        "issue_type": "technical_standard",
        "expected_inconsistency": True,
    },
    {
        "left_clause_id": "DOC-003-1",
        "right_clause_id": "DOC-004-1",
        "issue_type": "deadline_days",
        "expected_inconsistency": False,
    },
    {
        "left_clause_id": "DOC-003-2",
        "right_clause_id": "DOC-004-2",
        "issue_type": "responsibility",
        "expected_inconsistency": False,
    },
    {
        "left_clause_id": "DOC-003-3",
        "right_clause_id": "DOC-004-3",
        "issue_type": "measurement_basis",
        "expected_inconsistency": False,
    },
    {
        "left_clause_id": "DOC-003-4",
        "right_clause_id": "DOC-004-4",
        "issue_type": "technical_standard",
        "expected_inconsistency": True,
    },
]


def generate_documents() -> pd.DataFrame:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(DOCUMENTS)
    df.to_csv(DOCUMENTS_PATH, index=False)
    pd.DataFrame(GROUND_TRUTH).to_csv(GROUND_TRUTH_PATH, index=False)
    return df
