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

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(37, 99, 235, 0.18), transparent 32%),
        radial-gradient(circle at top right, rgba(56, 189, 248, 0.12), transparent 30%),
        linear-gradient(180deg, #020617 0%, #0F172A 100%);
    color: var(--text);
}

.block-container {
    padding-top: 1.4rem;
    max-width: 1180px;
}

[data-testid="stHeader"] {
    background: rgba(2, 6, 23, 0);
}

h1, h2, h3 {
    font-family: 'Sora', sans-serif;
    color: var(--text);
    letter-spacing: -0.035em;
}

h1 {
    font-size: 3.35rem !important;
    line-height: 1.05 !important;
    margin-bottom: 1rem !important;
}

h2 {
    font-size: 1.9rem !important;
}

p, label, span, div {
    color: var(--muted);
}

.nav-pill {
    padding: 9px 16px;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(56, 189, 248, 0.28);
    color: #38BDF8;
    font-weight: 800;
    font-size: 0.84rem;
}

.hero {
    padding: 48px;
    border-radius: 30px;
    background:
        linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(2, 6, 23, 0.97)),
        radial-gradient(circle at 82% 18%, rgba(56, 189, 248, 0.20), transparent 34%);
    border: 1px solid rgba(56, 189, 248, 0.24);
    box-shadow: 0 26px 80px rgba(0,0,0,0.38);
    margin-bottom: 2rem;
}

.hero-kicker {
    color: #38BDF8;
    font-size: 0.84rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 1rem;
}

.hero-copy {
    font-size: 1.12rem;
    line-height: 1.75;
    color: #CBD5E1;
    max-width: 770px;
}

.step-card {
    background: rgba(15, 23, 42, 0.82);
    border: 1px solid rgba(56, 189, 248, 0.17);
    border-radius: 22px;
    padding: 22px;
    min-height: 145px;
    box-shadow: 0 14px 34px rgba(0,0,0,0.18);
}

.step-number {
    width: 32px;
    height: 32px;
    border-radius: 999px;
    background: rgba(37, 99, 235, 0.28);
    color: #38BDF8;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    margin-bottom: 12px;
}

/* Fix Streamlit expander */
[data-testid="stExpander"] {
    background: rgba(15, 23, 42, 0.78) !important;
    border: 1px solid rgba(56, 189, 248, 0.18) !important;
    border-radius: 18px !important;
    overflow: hidden !important;
}

[data-testid="stExpander"] details {
    background: rgba(15, 23, 42, 0.78) !important;
}

[data-testid="stExpander"] summary {
    background: rgba(15, 23, 42, 0.94) !important;
    color: #F8FAFC !important;
}

[data-testid="stExpander"] summary * {
    color: #F8FAFC !important;
}

/* Bordered Streamlit container used for Evaluate Content */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 23, 42, 0.78) !important;
    border: 1px solid rgba(56, 189, 248, 0.22) !important;
    border-radius: 26px !important;
    box-shadow: 0 18px 42px rgba(0,0,0,0.20) !important;
    padding: 10px !important;
}

/* Inputs */
[data-testid="stFileUploader"] {
    background: rgba(2, 6, 23, 0.50);
    border: 1px solid rgba(56, 189, 248, 0.22);
    border-radius: 16px;
    padding: 14px;
}

[data-testid="stFileUploader"] section {
    background: rgba(15, 23, 42, 0.86) !important;
    border: 1px dashed rgba(56, 189, 248, 0.35) !important;
    border-radius: 14px !important;
}

[data-testid="stFileUploader"] button {
    background: rgba(37, 99, 235, 0.22) !important;
    color: #E0F2FE !important;
    border: 1px solid rgba(56, 189, 248, 0.45) !important;
    border-radius: 12px !important;
}

textarea, input {
    border-radius: 14px !important;
    border: 1px solid rgba(56, 189, 248, 0.28) !important;
}

.stTextArea textarea, .stTextInput input {
    background-color: rgba(15, 23, 42, 0.92) !important;
    color: #F8FAFC !important;
}

.stTextArea textarea::placeholder, .stTextInput input::placeholder {
    color: #94A3B8 !important;
}

.stButton > button, .stDownloadButton > button {
    background: linear-gradient(90deg, #2563EB, #38BDF8) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.8rem 1.45rem !important;
    font-weight: 800 !important;
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.32) !important;
}

[data-testid="stMetric"] {
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(56, 189, 248, 0.24);
    border-radius: 20px;
    padding: 20px;
}

.decision-card {
    padding: 19px 21px;
    border-radius: 18px;
    font-weight: 800;
    border: 1px solid rgba(148, 163, 184, 0.18);
    box-shadow: 0 12px 28px rgba(0,0,0,0.16);
}

.pass-card {
    background: rgba(16, 185, 129, 0.13);
    color: #A7F3D0;
}

.flag-card {
    background: rgba(245, 158, 11, 0.14);
    color: #FDE68A;
}

.review-card {
    background: rgba(56, 189, 248, 0.13);
    color: #BAE6FD;
}

.footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(148, 163, 184, 0.16);
    color: #94A3B8;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# CONFIG
# -----------------------------
N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", "").strip()

# -----------------------------
# LOGO + NAV
# -----------------------------
nav_left, nav_right = st.columns([0.75, 0.25])

with nav_left:
    st.image("aligna-logo.png", width=230)

with nav_right:
    st.markdown(
        """
        <div style="display:flex; justify-content:flex-end; align-items:center; height:64px;">
            <div class="nav-pill">Brand Voice QA</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# HERO
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-kicker">AI-powered brand voice evaluation</div>
    <h1>Turn brand voice review into a clear decision.</h1>
    <p class="hero-copy">
        Aligna evaluates copy against a learned brand voice and returns structured
        PASS, FLAG, or REVIEW outcomes with explanations your team can act on before anything goes live.
    </p>
</div>
""", unsafe_allow_html=True)

step1, step2, step3 = st.columns(3)

with step1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">1</div>
        <h3>Upload or paste</h3>
        <p>Add brand guidelines or paste copy you want to evaluate.</p>
    </div>
    """, unsafe_allow_html=True)

with step2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">2</div>
        <h3>Evaluate</h3>
        <p>Aligna checks tone, clarity, and alignment against the brand voice.</p>
    </div>
    """, unsafe_allow_html=True)

with step3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">3</div>
        <h3>Act with confidence</h3>
        <p>Review PASS, FLAG, or REVIEW decisions with a shareable HTML report.</p>
    </div>
    """, unsafe_allow_html=True)

with st.expander("About Aligna", expanded=False):
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
with st.container(border=True):
    st.header("Evaluate Content")
    st.caption("Brand guideline upload is optional. The tool can still run using built-in brand voice examples.")

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
            height=170,
            placeholder="Example: Introducing our latest feature to help marketers move faster with confidence...",
            help="Paste copy you want Aligna to evaluate."
        )

    email = st.text_input(
        "Email — optional",
        placeholder="name@example.com",
        help="Optional. Used only if your workflow supports logging or email delivery."
    )

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
st.header("Decision System")

d1, d2, d3 = st.columns(3)

with d1:
    st.markdown('<div class="decision-card pass-card">PASS<br><span>On-brand and ready to use</span></div>', unsafe_allow_html=True)

with d2:
    st.markdown('<div class="decision-card flag-card">FLAG<br><span>Off-brand or rewrite suggested</span></div>', unsafe_allow_html=True)

with d3:
    st.markdown('<div class="decision-card review-card">REVIEW<br><span>Needs human judgment</span></div>', unsafe_allow_html=True)


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

    st.markdown("## Evaluation Summary")

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

    if html:
        aligna_report_css = """
<style>
    html, body {
        background: #020617 !important;
        color: #E5E7EB !important;
        font-family: Inter, Arial, sans-serif !important;
        padding: 24px !important;
    }

    body * {
        color: #E5E7EB !important;
    }

    h1, h2, h3 {
        color: #F8FAFC !important;
        letter-spacing: -0.02em !important;
    }

    table {
        width: 100% !important;
        border-collapse: collapse !important;
        background: #0F172A !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
    }

    th {
        background: #1E293B !important;
        color: #F8FAFC !important;
        font-weight: 800 !important;
        padding: 14px !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
    }

    td {
        background: #0F172A !important;
        color: #E5E7EB !important;
        padding: 14px !important;
        border: 1px solid rgba(148, 163, 184, 0.22) !important;
        vertical-align: top !important;
    }

    tr:nth-child(even) td {
        background: #111C33 !important;
    }

    td:nth-child(2) {
        color: #38BDF8 !important;
        font-weight: 900 !important;
    }

    code, pre {
        background: #020617 !important;
        color: #38BDF8 !important;
        border-radius: 10px !important;
    }
</style>
"""
        if "<head>" in html:
            html = html.replace("<head>", "<head>" + aligna_report_css)
        else:
            html = aligna_report_css + html

        html = html.replace("PASS:", "<span style='color:#A7F3D0!important;font-weight:900;'>PASS:</span>")
        html = html.replace("FLAG:", "<span style='color:#FCA5A5!important;font-weight:900;'>FLAG:</span>")
        html = html.replace("REVIEW:", "<span style='color:#FDE68A!important;font-weight:900;'>REVIEW:</span>")

    st.markdown("### HTML Report Preview")
    st.caption("A branded report preview designed for brand managers and non-technical stakeholders.")

    if html:
        st.components.v1.html(html, height=720, scrolling=True)
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

st.markdown("""
<div class="footer">
    Aligna · AI-powered brand voice evaluation · Built with Streamlit, n8n, and Ollama
</div>
""", unsafe_allow_html=True)
