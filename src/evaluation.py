from __future__ import annotations

import json

import pandas as pd

from .config import GROUND_TRUTH_PATH, METRICS_PATH, PROCESSED_DIR


def _pair_key(left_clause_id: str, right_clause_id: str) -> str:
    left, right = sorted([left_clause_id, right_clause_id])
    return f"{left}||{right}"


def _finding_key(left_clause_id: str, right_clause_id: str, issue_type: str) -> str:
    return f"{_pair_key(left_clause_id, right_clause_id)}||{issue_type}"


def _safe_metrics(tp: int, fp: int, fn: int) -> dict[str, float | int]:
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {
        "tp": int(tp),
        "fp": int(fp),
        "fn": int(fn),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def evaluate_pipeline(similar_pairs: pd.DataFrame, findings: pd.DataFrame) -> dict:
    ground_truth = pd.read_csv(GROUND_TRUTH_PATH)

    expected_pair_keys = {
        _pair_key(row.left_clause_id, row.right_clause_id)
        for row in ground_truth.itertuples()
    }
    retrieved_pair_keys = {
        _pair_key(row.left_clause_id, row.right_clause_id)
        for row in similar_pairs.itertuples()
    }

    retrieval_tp = len(retrieved_pair_keys & expected_pair_keys)
    retrieval_fp = len(retrieved_pair_keys - expected_pair_keys)
    retrieval_fn = len(expected_pair_keys - retrieved_pair_keys)

    expected_finding_keys = {
        _finding_key(row.left_clause_id, row.right_clause_id, row.issue_type)
        for row in ground_truth.itertuples()
        if bool(row.expected_inconsistency)
    }
    predicted_finding_keys = {
        _finding_key(row.left_clause_id, row.right_clause_id, row.issue_type)
        for row in findings.itertuples()
    }

    detection_tp = len(predicted_finding_keys & expected_finding_keys)
    detection_fp = len(predicted_finding_keys - expected_finding_keys)
    detection_fn = len(expected_finding_keys - predicted_finding_keys)

    metrics = {
        "retrieval": _safe_metrics(retrieval_tp, retrieval_fp, retrieval_fn),
        "consistency_detection": _safe_metrics(detection_tp, detection_fp, detection_fn),
        "ground_truth_pairs": int(len(expected_pair_keys)),
        "ground_truth_inconsistencies": int(len(expected_finding_keys)),
    }

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics
