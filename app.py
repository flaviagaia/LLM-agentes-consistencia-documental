from __future__ import annotations

import json

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import CLAUSES_PATH, FINDINGS_PATH, METRICS_PATH, SUMMARY_PATH
from src.pipeline import run_pipeline


def _ensure_artifacts(review_mode: str) -> tuple[dict, dict, pd.DataFrame, pd.DataFrame]:
    try:
        summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
        metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
        clauses = pd.read_csv(CLAUSES_PATH)
        findings = pd.read_csv(FINDINGS_PATH)
        expected_summary_keys = {
            "documents",
            "clauses",
            "similar_pairs",
            "findings",
            "reviewed_findings",
            "review_mode",
        }
        if not expected_summary_keys.issubset(summary):
            raise ValueError("summary incompleto")
        if summary.get("review_mode") != review_mode:
            raise ValueError("summary em modo diferente do selecionado")
        if "retrieval" not in metrics or "consistency_detection" not in metrics:
            raise ValueError("metrics incompleto")
        if clauses.empty or "clause_id" not in clauses.columns:
            raise ValueError("clauses invalido")
        if "issue_type" not in findings.columns:
            raise ValueError("findings invalido")
        return summary, metrics, clauses, findings
    except Exception:
        summary = run_pipeline(use_llm=(review_mode == "llm"))
        metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
        clauses = pd.read_csv(CLAUSES_PATH)
        findings = pd.read_csv(FINDINGS_PATH)
        return summary, metrics, clauses, findings


st.set_page_config(page_title="LLM Agentes de Consistência Documental", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background: #07111f; color: #e5eef9; }
    .hero {
        background: rgba(10, 18, 32, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 22px;
        padding: 1.2rem 1.3rem;
    }
    .hero h1, .hero p { color: #e5eef9; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>LLM Agentes para Consistência Documental</h1>
        <p>Pipeline com agentes de recuperação, detecção de inconsistências e revisão final assistida por LLM para documentos técnicos sintéticos.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

mode = st.radio("Modo de revisão", options=["fallback", "llm"], horizontal=True, format_func=lambda x: "LLM" if x == "llm" else "Fallback")
if st.button("Atualizar análise"):
    run_pipeline(use_llm=(mode == "llm"))

summary, metrics, clauses, findings = _ensure_artifacts(mode)

cols = st.columns(6)
cols[0].metric("Documentos", summary["documents"])
cols[1].metric("Cláusulas", summary["clauses"])
cols[2].metric("Pares similares", summary["similar_pairs"])
cols[3].metric("Inconsistências", summary["findings"])
cols[4].metric("Modo", summary["review_mode"])
cols[5].metric("F1 Detecção", f"{metrics['consistency_detection']['f1']:.2f}")

tab_docs, tab_findings, tab_metrics = st.tabs(["Documentos", "Revisão dos Agentes", "Métricas"])

with tab_docs:
    st.dataframe(clauses, use_container_width=True, hide_index=True)

with tab_findings:
    if not findings.empty:
        st.plotly_chart(
            px.bar(findings["issue_type"].value_counts().rename_axis("issue_type").reset_index(name="count"), x="issue_type", y="count", color="issue_type", title="Tipos de inconsistência"),
            use_container_width=True,
        )
        st.dataframe(findings, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma inconsistência foi encontrada.")

with tab_metrics:
    metrics_df = pd.DataFrame(
        [
            {"stage": "retrieval", **metrics["retrieval"]},
            {"stage": "consistency_detection", **metrics["consistency_detection"]},
        ]
    )
    st.dataframe(metrics_df, use_container_width=True, hide_index=True)
    st.caption(
        "As métricas usam um ground truth controlado com pares esperados de cláusulas comparáveis e inconsistências conhecidas."
    )
