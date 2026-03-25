from __future__ import annotations

import json

import pandas as pd

from .config import DOCUMENTS_PATH, RAW_DIR


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


def generate_documents() -> pd.DataFrame:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(DOCUMENTS)
    df.to_csv(DOCUMENTS_PATH, index=False)
    return df
