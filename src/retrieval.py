from __future__ import annotations

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .config import PROCESSED_DIR, SIMILARITY_PATH


def build_similarity_pairs(clauses: pd.DataFrame, threshold: float = 0.35) -> pd.DataFrame:
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(clauses["clause_text"])
    similarity = cosine_similarity(matrix)

    pairs: list[dict] = []
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            if clauses.iloc[i]["document_id"] == clauses.iloc[j]["document_id"]:
                continue
            score = float(similarity[i, j])
            if score >= threshold:
                pairs.append(
                    {
                        "left_clause_id": clauses.iloc[i]["clause_id"],
                        "right_clause_id": clauses.iloc[j]["clause_id"],
                        "left_document": clauses.iloc[i]["document_name"],
                        "right_document": clauses.iloc[j]["document_name"],
                        "left_text": clauses.iloc[i]["clause_text"],
                        "right_text": clauses.iloc[j]["clause_text"],
                        "similarity": round(score, 4),
                    }
                )

    df = pd.DataFrame(pairs)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(SIMILARITY_PATH, index=False)
    return df
