from __future__ import annotations

import re

import pandas as pd

from .config import CLAUSES_PATH, PROCESSED_DIR


CLAUSE_PATTERN = re.compile(r"(\d+)\.\s([^\.]+\.)")


def extract_clauses(documents: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    for row in documents.itertuples():
        for match in CLAUSE_PATTERN.finditer(row.document_text):
            clause_no = match.group(1)
            clause_text = match.group(2).strip()
            rows.append(
                {
                    "document_id": row.document_id,
                    "document_name": row.document_name,
                    "document_type": row.document_type,
                    "clause_id": f"{row.document_id}-{clause_no}",
                    "clause_number": int(clause_no),
                    "clause_text": clause_text,
                }
            )

    df = pd.DataFrame(rows)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLAUSES_PATH, index=False)
    return df
