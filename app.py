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
    --panel: #111827;
    --panel-soft: rgba(15, 23, 42, 0.82);
    --blue: #2563EB;
    --cyan: #38BDF8;
    --slate: #94A3B8;
    --text: #F8FAFC;
    --muted: #CBD5E1;
    --border: rgba(56, 189, 248, 0.22);
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
    width: min(94vw, 1480px) !important;
    max-width: 1480px !important;
    padding: 0.75rem 2rem 2rem !important;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    font-family: 'Sora', sans-serif;
    color: var(--text) !important;
    letter-spacing: -0.035em;
}

h1 {
    font-size: clamp(2.4rem, 3.6vw, 4.1rem) !important;
    line-height: 1.02 !important;
    max-width: 1080px;
    margin-bottom: 0.9rem !important;
}

h2 {
    font-size: 1.8rem !important;
}

p, label, span, div {
    color: var(--muted);
}

hr {
    margin: 1.45rem 0 !important;
    border-color: rgba(148, 163, 184, 0.14) !important;
}

.nav-pill {
    padding: 9px 16px;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.76);
    border: 1px solid rgba(56, 189, 248, 0.32);
    color: var(--cyan) !important;
    font-weight: 800;
    font-size: 0.84rem;
}

.hero {
    width: 100%;
    padding: clamp(28px, 3.5vw, 52px);
    border-radius: 32px;
    background:
        radial-gradient(circle at 86% 16%, rgba(56, 189, 248, 0.18), transparent 34%),
        linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(2, 6, 23, 0.98));
    border: 1px solid var(--border);
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.34);
    margin: 0.65rem 0 1rem;
}

.hero-kicker {
    color: var(--cyan);
    font-size: 0.78rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    margin-bottom: 0.85rem;
}

.hero-copy {
    font-size: clamp(0.94rem, 1vw, 1.08rem);
    line-height: 1.55;
    color: var(--muted);
    max-width: 1180px;
    margin: 0;
}

/* STEP CARDS */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    display: flex !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div {
    width: 100% !important;
}

.step-card {
    height: 175px !important;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background: var(--panel-soft);
    border: 1px solid rgba(56, 189, 248, 0.18);
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 14px 30px rgba(0, 0, 0, 0.18);
}

.step-card h3 {
    margin-top: 0.15rem;
    margin-bottom: 0.5rem;
}

.step-card p {
    margin: 0;
    line-height: 1.45;
}

.step-number {
    width: 28px;
    height: 28px;
    border-radius: 999px;
    background: rgba(37, 99, 235, 0.30);
    color: var(--cyan) !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    margin-bottom: 10px;
}

.after-steps-space {
    height: 0.75rem;
}

[data-testid="stExpander"] {
    background: rgba(15, 23, 42, 0.80) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    box-shadow: 0 12px 26px rgba(0, 0, 0, 0.16) !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    background: rgba(15, 23, 42, 0.94) !important;
    color: var(--text) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 23, 42, 0.84) !important;
    border: 1px solid rgba(56, 189, 248, 0.20) !important;
    border-radius: 28px !important;
    box-shadow: 0 18px 44px rgba(0, 0, 0, 0.22) !important;
    padding: 14px !important;
}

/* INPUTS */
div[data-baseweb="input"],
div[data-baseweb="textarea"] {
    background: #0B1220 !important;
    border: 1px solid rgba(56, 189, 248, 0.18) !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background: transparent !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="textarea"]:focus-within {
    border: 1px solid rgba(56, 189, 248, 0.35) !important;
    box-shadow: none !important;
    outline: none !important;
}

.stTextInput input,
.stTextArea textarea {
    background: #0B1220 !important;
    color: #F8FAFC !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    border-radius: 12px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #94A3B8 !important;
    opacity: 1 !important;
}

[data-testid="stFileUploader"] {
    border: none !important;
    padding: 0 !important;
}

[data-testid="stFileUploader"] section {
    background: #0B1220 !important;
    border: 1px dashed rgba(56, 189, 248, 0.35) !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] button {
    background: rgba(56, 189, 248, 0.10) !important;
    color: #38BDF8 !important;
    border: 1px solid rgba(56, 189, 248, 0.45) !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploader"] button *,
[data-testid="stFileUploader"] button svg {
    color: #38BDF8 !important;
    fill: #38BDF8 !important;
    stroke: #38BDF8 !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {
    color: #94A3B8 !important;
}

label {
    color: #E2E8F0 !important;
    font-weight: 600 !important;
}

/* TOOLTIP */
[data-testid="stTooltipIcon"] {
    color: #94A3B8 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stTooltipIcon"] svg,
[data-testid="stTooltipIcon"] svg *,
[data-testid="stTooltipIcon"] path {
    color: #94A3B8 !important;
    fill: none !important;
    stroke: #94A3B8 !important;
}

[data-testid="stTooltipContent"] {
    background: #0B1220 !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(56, 189, 248, 0.25) !important;
    border-radius: 10px !important;
    padding: 10px 12px !important;
    font-size: 0.85rem !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4) !important;
    overflow: hidden !important;
}

[data-testid="stTooltipContent"]::after {
    border-top-color: #0B1220 !important;
}

[data-testid="stTooltipContent"] * {
    color: #E2E8F0 !important;
}

/* BUTTONS */
.stButton {
    margin-top: 0.9rem !important;
}

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, var(--blue), var(--cyan)) !important;
    color: white !important;
    border: 0 !important;
    border-radius: 14px !important;
    padding: 0.75rem 1.35rem !important;
    font-weight: 800 !important;
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.30) !important;
}

.stButton > button {
    min-width: 154px !important;
    height: 50px !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    filter: brightness(1.08);
    transform: translateY(-1px);
}

[data-testid="stMetric"] {
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(56, 189, 248, 0.24);
    border-radius: 20px;
    padding: 18px;
}

.decision-card {
    padding: 20px 22px;
    border-radius: 20px;
    font-weight: 800;
    border: 1px solid rgba(148, 163, 184, 0.18);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.16);
}

.decision-card span {
    color: var(--text) !important;
    font-weight: 700;
}

.pass-card {
    background: rgba(16, 185, 129, 0.14);
    color: #A7F3D0 !important;
}

.flag-card {
    background: rgba(245, 158, 11, 0.15);
    color: #FDE68A !important;
}

.review-card {
    background: rgba(56, 189, 248, 0.14);
    color: #BAE6FD !important;
}

.footer {
    margin-top: 2rem;
    padding-top: 1.1rem;
    border-top: 1px solid rgba(148, 163, 184, 0.16);
    color: var(--slate);
    font-size: 0.9rem;
}

@media (max-width: 900px) {
    .block-container {
        width: 94vw !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .hero {
        padding: 28px 22px;
    }

    .step-card {
        height: auto !important;
        min-height: 150px;
    }
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
    <p class="hero-copy">Aligna evaluates copy against a learned brand voice and returns structured PASS, FLAG, or REVIEW outcomes with explanations your team can act on before anything goes live.</p>
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

st.markdown('<div class="after-steps-space"></div>', unsafe_allow_html=True)

with st.expander("About Aligna", expanded=False):
    st.markdown(
        """
**What it does**  
Aligna evaluates content against a learned brand voice and turns subjective review into clear decisions.

**Decision system**
- **PASS** = content aligns with the brand voice
- **FLAG** = content conflicts with the brand voice or needs rewriting
- **REVIEW** = human judgment is needed before action

**Who it’s for**  
Marketing teams, social media managers, content creators, product marketers, and brand managers.

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
    st.caption("Upload is optional. Aligna can still run using built-in brand voice examples when no brand guideline PDF is added.")

    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        brand_pdf = st.file_uploader(
            "Upload Brand Guidelines PDF — optional",
            type=["pdf"],
            help="Optional. Uploading guidelines can support richer future evaluation."
        )

        email = st.text_input(
            "Email — optional",
            placeholder="name@example.com",
            help="Optional. Used only if your workflow supports logging or email delivery."
        )

    with col2:
        copy_text = st.text_area(
            "Copy to evaluate — optional for testing",
            height=182,
            placeholder="Example: Introducing our latest feature to help marketers move faster with confidence...",
            help="Paste copy you want Aligna to evaluate."
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
    st.markdown(
        '<div class="decision-card pass-card">PASS<br><span>On-brand and ready to use</span></div>',
        unsafe_allow_html=True
    )

with d2:
    st.markdown(
        '<div class="decision-card flag-card">FLAG<br><span>Off-brand or rewrite suggested</span></div>',
        unsafe_allow_html=True
    )

with d3:
    st.markdown(
        '<div class="decision-card review-card">REVIEW<br><span>Needs human judgment</span></div>',
        unsafe_allow_html=True
    )


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

    /* Report badge readability */
.badge,
span[class*="pass"],
span[class*="flag"],
span[class*="review"] {
    color: #020617 !important;
    font-weight: 900 !important;
}

/* Report explanation block readability */
.report-legend,
.legend,
.summary-box,
.info-box {
    background: #0F172A !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(56, 189, 248, 0.22) !important;
    border-radius: 14px !important;
}

/* Make text inside explanation blocks readable */
.report-legend *,
.legend *,
.summary-box *,
.info-box * {
    color: #E2E8F0 !important;
}

/* Keep labels visually distinct */
.report-legend strong,
.legend strong,
.summary-box strong,
.info-box strong {
    color: #F8FAFC !important;
    font-weight: 900 !important;
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
        html = html.replace("background:#fff", "background:#0F172A")
        html = html.replace("background: #fff", "background:#0F172A")
        html = html.replace("color:#111", "color:#E2E8F0")
        html = html.replace("color: #111", "color:#E2E8F0")

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
