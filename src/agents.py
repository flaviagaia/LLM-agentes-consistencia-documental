from __future__ import annotations

import json
import re
from dataclasses import dataclass

import pandas as pd

from .config import BASE_MODEL_NAME, FINDINGS_PATH, PROCESSED_DIR


DEADLINE_PATTERN = re.compile(r"within\s+(\d+)\s+calendar days", re.I)
STANDARD_PATTERN = re.compile(r"(ENG-[A-Z]+-\d+)", re.I)
RESPONSIBILITY_PATTERN = re.compile(r"performed by the ([^\.]+)", re.I)
MEASUREMENT_PATTERN = re.compile(r"based on ([^\.]+)", re.I)


@dataclass
class RetrievalAgent:
    name: str = "retrieval_agent"

    def run(self, pairs: pd.DataFrame) -> pd.DataFrame:
        return pairs.sort_values("similarity", ascending=False).reset_index(drop=True)


@dataclass
class ConsistencyAgent:
    name: str = "consistency_agent"

    def _extract(self, text: str) -> dict[str, str | None]:
        deadline = DEADLINE_PATTERN.search(text)
        standard = STANDARD_PATTERN.search(text)
        responsibility = RESPONSIBILITY_PATTERN.search(text)
        measurement = MEASUREMENT_PATTERN.search(text)
        return {
            "deadline_days": deadline.group(1) if deadline else None,
            "technical_standard": standard.group(1) if standard else None,
            "responsibility": responsibility.group(1).strip() if responsibility else None,
            "measurement_basis": measurement.group(1).strip() if measurement else None,
        }

    def run(self, ranked_pairs: pd.DataFrame) -> pd.DataFrame:
        findings: list[dict] = []
        for row in ranked_pairs.itertuples():
            left = self._extract(row.left_text)
            right = self._extract(row.right_text)
            for issue_type in ["deadline_days", "technical_standard", "responsibility", "measurement_basis"]:
                if left[issue_type] and right[issue_type] and left[issue_type] != right[issue_type]:
                    findings.append(
                        {
                            "left_clause_id": row.left_clause_id,
                            "right_clause_id": row.right_clause_id,
                            "left_document": row.left_document,
                            "right_document": row.right_document,
                            "left_text": row.left_text,
                            "right_text": row.right_text,
                            "similarity": row.similarity,
                            "issue_type": issue_type,
                            "left_value": left[issue_type],
                            "right_value": right[issue_type],
                        }
                    )
        return pd.DataFrame(findings)


@dataclass
class ReviewAgent:
    name: str = "review_agent"

    def __post_init__(self):
        self._tokenizer = None
        self._model = None

    def _load_model(self):
        if self._tokenizer is not None and self._model is not None:
            return
        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

            self._tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
            self._model = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL_NAME)
            self._model.to("cpu")
        except Exception:
            self._tokenizer = False
            self._model = False

    def _llm_review(self, row) -> tuple[str, str]:
        self._load_model()
        if not self._tokenizer or not self._model:
            return self._fallback_review(row)
        prompt = (
            "You are a document consistency review agent. "
            "Decide whether the pair below is a true inconsistency and explain briefly.\n"
            f"Issue type: {row.issue_type}\n"
            f"Left clause: {row.left_text}\n"
            f"Right clause: {row.right_text}\n"
            "Answer in the format: verdict=<true_inconsistency|needs_human_review>; explanation=<short explanation>"
        )
        inputs = self._tokenizer(prompt, return_tensors="pt", truncation=True, max_length=256)
        output = self._model.generate(**inputs, max_new_tokens=48)
        text = self._tokenizer.decode(output[0], skip_special_tokens=True).strip()
        verdict_match = re.search(r"verdict\s*=\s*([^;]+)", text, re.I)
        explanation_match = re.search(r"explanation\s*=\s*(.+)", text, re.I)
        if verdict_match and explanation_match:
            return verdict_match.group(1).strip(), explanation_match.group(1).strip()
        return self._fallback_review(row)

    def _fallback_review(self, row) -> tuple[str, str]:
        return (
            "true_inconsistency",
            f"The clauses disagree on {row.issue_type}: '{row.left_value}' versus '{row.right_value}'.",
        )

    def run(self, findings: pd.DataFrame, use_llm: bool = False) -> pd.DataFrame:
        reviewed: list[dict] = []
        for row in findings.itertuples():
            verdict, explanation = self._llm_review(row) if use_llm else self._fallback_review(row)
            reviewed.append(
                {
                    "left_clause_id": row.left_clause_id,
                    "right_clause_id": row.right_clause_id,
                    "left_document": row.left_document,
                    "right_document": row.right_document,
                    "issue_type": row.issue_type,
                    "left_value": row.left_value,
                    "right_value": row.right_value,
                    "similarity": row.similarity,
                    "agent_verdict": verdict,
                    "agent_explanation": explanation,
                    "review_mode": "llm" if use_llm else "fallback",
                }
            )
        df = pd.DataFrame(reviewed)
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(FINDINGS_PATH, index=False)
        return df
