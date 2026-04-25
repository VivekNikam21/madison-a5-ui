import base64
import requests
import streamlit as st

st.set_page_config(
    page_title="Aligna Brand Voice Evaluator",
    page_icon="🧭",
    layout="wide"
)

# -----------------------------
# BRAND CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --midnight: #020617;
    --navy: #0F172A;
    --blue: #2563EB;
    --cyan: #38BDF8;
    --slate: #94A3B8;
    --text: #F8FAFC;
    --muted: #CBD5E1;
}

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(37, 99, 235, 0.22), transparent 32%),
        radial-gradient(circle at 90% 8%, rgba(56, 189, 248, 0.13), transparent 30%),
        linear-gradient(180deg, var(--midnight) 0%, var(--navy) 100%);
    color: var(--text);
}

.block-container {
    width: min(94vw, 1400px);
}

/* Typography */
h1, h2, h3 {
    font-family: 'Sora', sans-serif;
    color: var(--text);
}

p, span, label {
    color: var(--muted);
}

/* Hero */
.hero {
    padding: 56px;
    border-radius: 28px;
    background: linear-gradient(135deg, #0F172A, #020617);
    border: 1px solid rgba(56,189,248,0.2);
    margin-bottom: 2rem;
}

.hero-kicker {
    color: var(--cyan);
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    margin-bottom: 1rem;
}

.hero-copy {
    max-width: 900px;
}

/* Step cards */
.step-card {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 18px;
    padding: 20px;
}

/* CLEAN INPUT STYLING */

.stTextInput input,
.stTextArea textarea {
    background: #0B1220 !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(56, 189, 248, 0.25) !important;
    border-radius: 12px !important;
}

/* remove ugly white glow */
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #38BDF8 !important;
    box-shadow: none !important;
    outline: none !important;
}

/* uploader */
[data-testid="stFileUploader"] section {
    background: #0B1220 !important;
    border: 1px dashed rgba(56, 189, 248, 0.35) !important;
    border-radius: 12px !important;
}

/* remove extra borders */
[data-testid="stFileUploader"] {
    border: none !important;
    padding: 0 !important;
}

/* labels */
label {
    color: #E2E8F0 !important;
    font-weight: 600 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2563EB, #38BDF8);
    border-radius: 12px;
    border: none;
    color: white;
    padding: 0.8rem 1.4rem;
    font-weight: 700;
}

/* Decision cards */
.decision-card {
    padding: 20px;
    border-radius: 16px;
    font-weight: 700;
}

.pass-card { background: rgba(16,185,129,0.2); }
.flag-card { background: rgba(245,158,11,0.2); }
.review-card { background: rgba(56,189,248,0.2); }

.footer {
    margin-top: 3rem;
    border-top: 1px solid rgba(148,163,184,0.2);
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# CONFIG
# -----------------------------
N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", "").strip()

# -----------------------------
# HERO
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-kicker">AI-powered brand voice evaluation</div>
    <h1>Turn brand voice review into a clear decision.</h1>
    <p class="hero-copy">
        Aligna evaluates copy against a learned brand voice and returns structured PASS, FLAG, or REVIEW outcomes with explanations your team can act on before anything goes live.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# INPUTS
# -----------------------------
with st.container():
    st.header("Evaluate Content")

    col1, col2 = st.columns([1, 1.2], gap="large")

    # LEFT
    with col1:
        brand_pdf = st.file_uploader(
            "Upload Brand Guidelines PDF — optional",
            type=["pdf"]
        )

        email = st.text_input(
            "Email — optional",
            placeholder="name@example.com"
        )

    # RIGHT
    with col2:
        copy_text = st.text_area(
            "Copy to evaluate — optional",
            height=220,
            placeholder="Example: Introducing our latest feature to help marketers move faster with confidence..."
        )

    run = st.button("Run Evaluation")

# -----------------------------
# OUTPUT (simplified)
# -----------------------------
st.header("Decision System")

d1, d2, d3 = st.columns(3)

with d1:
    st.markdown('<div class="decision-card pass-card">PASS<br>On-brand</div>', unsafe_allow_html=True)

with d2:
    st.markdown('<div class="decision-card flag-card">FLAG<br>Needs rewrite</div>', unsafe_allow_html=True)

with d3:
    st.markdown('<div class="decision-card review-card">REVIEW<br>Needs human</div>', unsafe_allow_html=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<div class="footer">
Aligna · AI-powered brand voice evaluation
</div>
""", unsafe_allow_html=True)
