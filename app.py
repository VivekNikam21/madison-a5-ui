import base64
import requests
import streamlit as st

st.set_page_config(
    page_title="Aligna Brand Voice Evaluator",
    page_icon="🧭",
    layout="wide"
)

# -----------------------------
# BRAND CSS (UPDATED MINIMALLY)
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

/* CLEAN INPUT STYLING */

.stTextInput input,
.stTextArea textarea {
    background: #0B1220 !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(56, 189, 248, 0.25) !important;
    border-radius: 12px !important;
}

/* remove white glow */
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

/* remove outer uploader border */
[data-testid="stFileUploader"] {
    border: none !important;
    padding: 0 !important;
}

/* labels */
label {
    color: #E2E8F0 !important;
    font-weight: 600 !important;
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
    <h1>Turn brand voice review into a clear decision.</h1>
    <p>
        Aligna evaluates copy against a learned brand voice and returns structured PASS, FLAG, or REVIEW outcomes with explanations your team can act on before anything goes live.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# INPUTS (FIXED LAYOUT)
# -----------------------------
with st.container(border=True):
    st.header("Evaluate Content")

    col1, col2 = st.columns([1, 1.2], gap="large")

    # LEFT → upload + email
    with col1:
        brand_pdf = st.file_uploader(
            "Upload Brand Guidelines PDF — optional",
            type=["pdf"],
            help="Optional. Uploading guidelines can support richer future evaluation."
        )

        email = st.text_input(
            "Email — optional",
            placeholder="name@example.com"
        )

    # RIGHT → textarea
    with col2:
        copy_text = st.text_area(
            "Copy to evaluate — optional for testing",
            height=220,
            placeholder="Example: Introducing our latest feature to help marketers move faster with confidence..."
        )

    errors = []

    if not N8N_WEBHOOK_URL:
        errors.append("Missing webhook URL in secrets.")

    if email and ("@" not in email or "." not in email.split("@")[-1]):
        errors.append("Invalid email format.")

    if errors:
        for e in errors:
            st.error(e)

    run = st.button("Run Evaluation", disabled=bool(errors))

# -----------------------------
# OUTPUT (UNCHANGED CORE LOGIC)
# -----------------------------
if run:
    payload = {
        "email": email,
        "user_copy": copy_text,
        "uploaded_pdf": bool(brand_pdf),
    }

    with st.spinner("Running Aligna evaluation…"):
        try:
            resp = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=300)
            data = resp.json()
        except Exception as e:
            st.error("Webhook failed")
            st.code(str(e))
            st.stop()

    st.success("Evaluation complete")

    st.json(data)
