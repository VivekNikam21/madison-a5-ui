import base64
import requests
import streamlit as st

st.set_page_config(
    page_title="Aligna Brand Voice Evaluator",
    page_icon="🧭",
    layout="wide"
)

# -----------------------------
# BRAND STYLING
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #020617 0%, #0F172A 100%);
    color: #E5E7EB;
}

h1, h2, h3 {
    font-family: 'Sora', sans-serif;
    color: #F8FAFC;
}

p, label, span, div {
    color: #CBD5E1;
}

[data-testid="stHeader"] {
    background: rgba(2, 6, 23, 0);
}

[data-testid="stMetric"] {
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(56, 189, 248, 0.28);
    border-radius: 18px;
    padding: 18px;
}

.stButton > button {
    background: linear-gradient(90deg, #2563EB, #38BDF8);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.25rem;
    font-weight: 700;
}

.stButton > button:hover {
    opacity: 0.92;
    transform: translateY(-1px);
}

[data-testid="stFileUploader"] {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 16px;
    padding: 14px;
}

textarea, input {
    border-radius: 12px !important;
}

.block-container {
    padding-top: 3rem;
}

.aligna-card {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.22);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 20px;
}

.aligna-pill {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(37, 99, 235, 0.18);
    color: #38BDF8;
    border: 1px solid rgba(56, 189, 248, 0.35);
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 10px;
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
st.markdown('<div class="aligna-pill">AI Brand QA Layer</div>', unsafe_allow_html=True)

col1, col2 = st.columns([0.72, 0.28])

with col1:
    st.title("Aligna Brand Voice Evaluator")
    st.caption("Where brand voice stops being subjective and becomes a decision.")
    st.write(
        "Evaluate content against your brand voice and receive clear PASS, FLAG, or REVIEW outcomes with explainable feedback."
    )

with col2:
    st.markdown("""
<div class="aligna-card">
<h3>Built for</h3>
<p>Marketing teams, brand managers, social media managers, and content creators who need a fast quality check before publishing.</p>
</div>
""", unsafe_allow_html=True)

with st.expander("About", expanded=False):
    st.markdown(
        """
**What it does**
- Evaluates content against a learned brand voice
- Returns **PASS / FLAG / REVIEW** decisions
- Provides explainable feedback and a human-readable HTML report

**Who it’s for**
Marketing teams, social media managers, content creators, and brand managers.

**Tech stack**
Streamlit UI → n8n workflow → Ollama local LLM → HTML report

**Built by**
Vivek Nikam  
Portfolio: https://vivek-nikam-portfolio.framer.website/
"""
    )

st.divider()

# -----------------------------
# INPUTS
# -----------------------------
st.header("Evaluate Content")
st.caption(
    "Upload brand guidelines if available. The system can still run using built-in brand voice examples."
)

col1, col2 = st.columns(2)

with col1:
    brand_pdf = st.file_uploader(
        "Upload Brand Guidelines PDF — optional",
        type=["pdf"],
        help="Optional. Uploading guidelines can support richer future evaluation."
    )

with col2:
    copy_text = st.text_area(
        "Copy to evaluate — optional for testing",
        height=160,
        placeholder="Example: Introducing our latest feature to help marketers move faster with confidence...",
        help="Paste copy you want Aligna to evaluate."
    )

email = st.text_input(
    "Email — optional",
    placeholder="name@example.com",
    help="Optional. Used only if your workflow supports logging or email delivery."
)

# -----------------------------
# VALIDATION
# -----------------------------
errors = []

if not N8N_WEBHOOK_URL:
    errors.append(
        "Missing N8N_WEBHOOK_URL. Add it in Streamlit Cloud → App → Settings → Secrets."
    )
elif not N8N_WEBHOOK_URL.startswith("http"):
    errors.append("N8N_WEBHOOK_URL must start with http:// or https://")

if email and ("@" not in email or "." not in email.split("@")[-1]):
    errors.append("Email looks invalid. Enter a valid email or leave blank.")

if errors:
    for e in errors:
        st.error(e)

run = st.button("Run Evaluation", disabled=bool(errors))

st.divider()

# -----------------------------
# OUTPUTS
# -----------------------------
st.header("Outputs")

decision_cols = st.columns(3)
decision_cols[0].success("PASS: On-brand and ready to use")
decision_cols[1].warning("FLAG: Off-brand or rewrite suggested")
decision_cols[2].info("REVIEW: Needs human judgment")


def decode_report(report_b64: str) -> str:
    if not report_b64:
        return ""
    try:
        return base64.b64decode(report_b64).decode("utf-8", errors="replace")
    except Exception:
        return ""


if run:
    payload = {
        "email": email,
        "user_copy": copy_text,
        "uploaded_pdf": bool(brand_pdf),
    }

    with st.spinner("Running Aligna evaluation… this can take up to 1–2 minutes."):
        try:
            resp = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=300)
        except requests.exceptions.RequestException as ex:
            st.error(
                "Couldn’t reach the n8n webhook. Check that ngrok is running, n8n is running, and the webhook URL is correct."
            )
            st.code(str(ex))
            st.stop()

        if not resp.ok:
            st.error(f"n8n returned an error ({resp.status_code}).")
            st.code(resp.text[:2000])
            st.download_button(
                "Download Raw Response",
                data=resp.text.encode("utf-8"),
                file_name="n8n_error_response.txt",
                mime="text/plain",
            )
            st.stop()

        try:
            data = resp.json()
        except Exception:
            st.error("Webhook responded, but it wasn’t valid JSON.")
            st.code(resp.text[:2000])
            st.download_button(
                "Download Raw Response",
                data=resp.text.encode("utf-8"),
                file_name="n8n_non_json_response.txt",
                mime="text/plain",
            )
            st.stop()

    if not data.get("ok"):
        st.error("Workflow returned ok=false or missing ok.")
        st.json(data)
        st.download_button(
            "Download Raw JSON",
            data=resp.text.encode("utf-8"),
            file_name="n8n_response.json",
            mime="application/json",
        )
        st.stop()

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Items", data.get("total_items", "—"))
    c2.metric("PASS", data.get("passed", "—"))
    c3.metric("FLAG", data.get("flagged", "—"))
    c4.metric("REVIEW", data.get("review", "—"))

    st.markdown("### Key Insights")
    st.markdown(
        """
- **PASS** = content aligns with the brand voice  
- **FLAG** = content appears misaligned and needs a rewrite  
- **REVIEW** = output needs human verification before action  
"""
    )

    st.caption(f"Generated at: {data.get('generated_at', '—')}")

    report_name = data.get("report_file_name", "aligna_brand_voice_report.html")
    report_b64 = data.get("report_base64", "")
    html = decode_report(report_b64)

    st.markdown("### HTML Report Preview")
    st.caption("A shareable report designed for brand managers and non-technical stakeholders.")

    if html:
        st.components.v1.html(html, height=650, scrolling=True)
        st.download_button(
            "Download HTML Report",
            data=html.encode("utf-8"),
            file_name=report_name,
            mime="text/html",
        )
    else:
        st.warning("No report returned.")
        st.download_button(
            "Download Raw JSON",
            data=resp.text.encode("utf-8"),
            file_name="n8n_response.json",
            mime="application/json",
        )

st.divider()
st.caption("Aligna · AI-powered brand voice evaluation · Built with Streamlit, n8n, and Ollama")
