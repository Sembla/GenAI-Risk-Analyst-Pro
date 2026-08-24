from __future__ import annotations

from pathlib import Path

import streamlit as st

from explanations import local_explanation
from llm_service import explain_decision
from retrieval import load_documents, retrieve
from risk_engine import DemoCase, evaluate_case, load_policy


ROOT = Path(__file__).parent

st.set_page_config(page_title="GenAI Risk Analyst Pro", layout="wide")
st.title("GenAI Risk Analyst Pro")
st.caption("Educational prototype: deterministic rules, document retrieval and optional LLM explanation")

st.warning(
    "This application uses synthetic data and demonstration policies. It must not be used "
    "for real credit, financial, compliance or eligibility decisions."
)

policy = load_policy(ROOT / "data" / "demo_policy.json")
documents = load_documents(ROOT / "data" / "knowledge")

with st.sidebar:
    st.header("Synthetic case")
    score = st.slider("Demo score", 0, 1000, 580)
    late_payments = st.number_input("Recent late payments", min_value=0, max_value=12, value=1)
    income_verified = st.checkbox("Income verified", value=False)
    use_llm = st.toggle("Use optional OpenAI explanation", value=False)

case = DemoCase(
    case_id="DEMO-001",
    score=score,
    recent_late_payments=int(late_payments),
    income_verified=income_verified,
)
decision = evaluate_case(case, policy)

classification_col, review_col, policy_col = st.columns(3)
classification_col.metric("Classification", decision.classification.upper())
review_col.metric("Manual review", "YES" if decision.manual_review else "NO")
policy_col.metric("Policy", decision.policy_version)

st.subheader("Transparent rule reasons")
for reason in decision.reasons:
    st.write(f"- {reason}")

st.subheader("Ask about the demonstration policy")
question = st.text_input(
    "Question",
    value="Quando uma revisão manual é necessária?",
)

if question:
    retrieved = retrieve(question, documents, top_k=2)
    if use_llm:
        try:
            answer = explain_decision(decision, retrieved, question)
            mode = "OpenAI explanation of deterministic decision"
        except Exception as error:
            answer = local_explanation(case, decision)
            mode = f"Local fallback ({type(error).__name__})"
    else:
        answer = local_explanation(case, decision)
        mode = "Local deterministic explanation"

    st.write(answer)
    st.caption(f"Mode: {mode}")
    with st.expander("Retrieved sources"):
        for document in retrieved:
            st.markdown(f"**{document.source}** — similarity `{document.score:.3f}`")
            st.write(document.content)
