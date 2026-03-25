from __future__ import annotations

import json

from .agents import ConsistencyAgent, RetrievalAgent, ReviewAgent
from .config import SUMMARY_PATH
from .data_generation import generate_documents
from .evaluation import evaluate_pipeline
from .extraction import extract_clauses
from .retrieval import build_similarity_pairs


def run_pipeline(use_llm: bool = False) -> dict:
    documents = generate_documents()
    clauses = extract_clauses(documents)
    pairs = build_similarity_pairs(clauses)

    retrieval_agent = RetrievalAgent()
    consistency_agent = ConsistencyAgent()
    review_agent = ReviewAgent()

    ranked_pairs = retrieval_agent.run(pairs)
    findings = consistency_agent.run(ranked_pairs)
    reviewed = review_agent.run(findings, use_llm=use_llm)
    metrics = evaluate_pipeline(ranked_pairs, reviewed)

    summary = {
        "documents": int(len(documents)),
        "clauses": int(len(clauses)),
        "similar_pairs": int(len(ranked_pairs)),
        "findings": int(len(findings)),
        "reviewed_findings": int(len(reviewed)),
        "review_mode": "llm" if use_llm else "fallback",
        "retrieval_f1": metrics["retrieval"]["f1"],
        "consistency_detection_f1": metrics["consistency_detection"]["f1"],
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
