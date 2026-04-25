import base64
import requests
import streamlit as st

st.set_page_config(
    page_title="Aligna Brand Voice Evaluator",
    page_icon="🧭",
    layout="wide"
)

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
        linear-gradient(rgba(56,189,248,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,189,248,0.035) 1px, transparent 1px),
        radial-gradient(circle at 70% 25%, rgba(37,99,235,0.22), transparent 32%),
        linear-gradient(180deg, #020617 0%, #0F172A 100%);
    background-size: 32px 32px, 32px 32px, auto, auto;
    color: var(--text);
}

.block-container {
    max-width: 1320px;
    padding-top: 1.2rem;
    padding-left: 4rem;
    padding-right: 4rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    font-family: 'Sora', sans-serif;
    color: var(--text);
    letter-spacing: -0.035em;
}

p, label, span, div {
    color: var(--muted);
}

section {
    margin-bottom: 3.5rem;
}

.top-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6rem;
}

.nav-links {
    display: flex;
    gap: 34px;
    align-items: center;
    color: #94A3B8;
    font-weight: 700;
}

.nav-cta {
    background: #2563EB;
    color: white;
    padding: 13px 24px;
    border-radius: 10px;
    font-weight: 800;
}

.hero-grid {
    display: grid;
    grid-template-columns: 1fr 0.95fr;
    gap: 72px;
    align-items: center;
    margin-bottom: 6rem;
}

.kicker {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(37,99,235,0.18);
    border: 1px solid rgba(56,189,248,0.28);
    color: #38BDF8;
    font-weight: 800;
    margin-bottom: 24px;
}

.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 4.4rem;
    line-height: 1.08;
    font-weight: 800;
    color: #F8FAFC;
    margin-bottom: 24px;
}

.hero-subtitle {
    font-size: 1.18rem;
    line-height: 1.75;
    max-width: 620px;
    color: #94A3B8;
}

.hero-actions {
    display: flex;
    gap: 14px;
    margin-top: 32px;
}

.primary-btn {
    background: linear-gradient(90deg, #2563EB, #38BDF8);
    color: white;
    padding: 15px 24px;
    border-radius: 12px;
    font-weight: 800;
    display: inline-block;
}

.secondary-btn {
    border: 1px solid rgba(148,163,184,0.22);
    color: #F8FAFC;
    padding: 15px 24px;
    border-radius: 12px;
    font-weight: 800;
    display: inline-block;
    background: rgba(15,23,42,0.42);
}

.mockup {
    background: rgba(15,23,42,0.86);
    border: 1px solid rgba(56,189,248,0.18);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 30px 80px rgba(0,0,0,0.42);
}

.mockup-top {
    display: flex;
    gap: 10px;
    margin-bottom: 18px;
}

.dot {
    width: 11px;
    height: 11px;
    border-radius: 99px;
}

.mock-card {
    background: #020617;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 16px;
    border: 1px solid rgba(148,163,184,0.10);
}

.progress {
    height: 6px;
    border-radius: 99px;
    background: rgba(148,163,184,0.16);
    overflow: hidden;
    margin: 18px 0;
}

.progress > div {
    height: 100%;
    width: 76%;
    background: linear-gradient(90deg, #2563EB, #38BDF8);
}

.process-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 22px;
    margin-bottom: 4rem;
}

.step-soft {
    border-left: 2px solid rgba(56,189,248,0.45);
    padding-left: 22px;
}

.step-num {
    color: #38BDF8;
    font-weight: 900;
    margin-bottom: 12px;
}

.evaluate-panel {
    background: rgba(15,23,42,0.68);
    border: 1px solid rgba(56,189,248,0.18);
    border-radius: 26px;
    padding: 34px;
    box-shadow: 0 22px 60px rgba(0,0,0,0.24);
    margin-bottom: 4rem;
}

.section-title {
    font-family: 'Sora', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #F8FAFC;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #94A3B8;
    margin-bottom: 28px;
}

[data-testid="stFileUploader"] {
    background: rgba(2,6,23,0.62) !important;
    border: 1px solid rgba(56,189,248,0.35) !important;
    border-radius: 16px !important;
    padding: 16px !important;
}

[data-testid="stFileUploader"] section {
    background: rgba(15,23,42,0.78) !important;
    border: 1px dashed rgba(56,189,248,0.35) !important;
    border-radius: 14px !important;
}

[data-testid="stFileUploader"] button {
    background: rgba(37,99,235,0.25) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(56,189,248,0.45) !important;
    border-radius: 12px !important;
}

.stTextArea textarea, .stTextInput input {
    background: rgba(2,6,23,0.70) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(56,189,248,0.42) !important;
    border-radius: 16px !important;
    box-shadow: none !important;
}

.stTextArea textarea::placeholder, .stTextInput input::placeholder {
    color: #94A3B8 !important;
}

.stButton > button, .stDownloadButton > button {
    background: linear-gradient(90deg, #2563EB, #38BDF8) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 1.55rem !important;
    font-weight: 800 !important;
    box-shadow: 0 12px 30px rgba(37,99,235,0.32) !important;
}

[data-testid="stMetric"] {
    background: rgba(15,23,42,0.84);
    border: 1px solid rgba(56,189,248,0.24);
    border-radius: 20px;
    padding: 20px;
}

.decision-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin: 20px 0 36px;
}

.decision-card {
    padding: 18px 20px;
    border-radius: 18px;
    font-weight: 800;
    border: 1px solid rgba(148,163,184,0.18);
}

.pass-card { background: rgba(16,185,129,0.12); color: #A7F3D0; }
.flag-card { background: rgba(245,158,11,0.13); color: #FDE68A; }
.review-card { background: rgba(56,189,248,0.12); color: #BAE6FD; }

.about-strip {
    background: rgba(15,23,42,0.54);
    border-top: 1px solid rgba(56,189,248,0.18);
    border-bottom: 1px solid rgba(56,189,248,0.18);
    padding: 26px 0;
    margin-bottom: 4rem;
}

.footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(148,163,184,0.16);
    color: #94A3B8;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", "").strip()

# NAV
st.markdown("""
<div class="top-nav">
    <img src="aligna-logo.png" style="width:145px;" />
    <div class="nav-links">
        <span>Product</span>
        <span>About</span>
        <span>Team</span>
        <span>Contact</span>
    </div>
    <div class="nav-cta">Try Aligna</div>
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<section class="hero-grid">
    <div>
        <div class="kicker">AI-Powered Brand Voice Platform</div>
        <div class="hero-title">Ensure Every Message Matches Your Brand Voice</div>
        <div class="hero-subtitle">
            Aligna evaluates your content against your brand voice and provides clear PASS, FLAG, or REVIEW decisions before it goes live.
        </div>
        <div class="hero-actions">
            <div class="primary-btn">Try Aligna →</div>
            <div class="secondary-btn">▷ See How It Works</div>
        </div>
    </div>

    <div class="mockup">
        <div class="mockup-top">
            <div class="dot" style="background:#EF4444;"></div>
            <div class="dot" style="background:#F59E0B;"></div>
            <div class="dot" style="background:#22C55E;"></div>
            <span style="margin-left:16px;font-weight:800;color:#94A3B8;">Brand Voice Evaluation</span>
        </div>
        <div class="mock-card">
            <div style="color:#94A3B8;font-weight:800;margin-bottom:10px;">Content Input</div>
            <div style="color:#F8FAFC;font-weight:700;">
                “Unlock your potential with our revolutionary solution that transforms how you work...”
            </div>
        </div>
        <div class="progress"><div></div></div>
        <div class="mock-card">
            <div style="color:#94A3B8;font-weight:800;margin-bottom:10px;">Evaluation Result</div>
            <div style="display:flex;justify-content:space-between;gap:16px;">
                <div style="color:#F8FAFC;font-weight:700;">
                    Tone mismatch detected. Language is more promotional than the brand's supportive, educational voice.
                </div>
                <div style="color:#FDE68A;font-weight:900;">FLAG</div>
            </div>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# PROCESS — cleaner, less boxy
st.markdown("""
<section class="process-row">
    <div class="step-soft">
        <div class="step-num">01</div>
        <h3>Upload or paste</h3>
        <p>Add brand guidelines or paste copy you want to evaluate.</p>
    </div>
    <div class="step-soft">
        <div class="step-num">02</div>
        <h3>Evaluate</h3>
        <p>Aligna checks tone, clarity, and alignment against your brand voice.</p>
    </div>
    <div class="step-soft">
        <div class="step-num">03</div>
        <h3>Act with confidence</h3>
        <p>Review PASS, FLAG, or REVIEW decisions with a shareable report.</p>
    </div>
</section>
""", unsafe_allow_html=True)

# ABOUT — no expander, no white bar
st.markdown("""
<section class="about-strip">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:34px;">
        <div>
            <h3>What it does</h3>
            <p>Evaluates content against a learned brand voice and returns structured PASS, FLAG, or REVIEW decisions.</p>
        </div>
        <div>
            <h3>Who it’s for</h3>
            <p>Marketing teams, social media managers, content creators, and brand managers.</p>
        </div>
        <div>
            <h3>Tech stack</h3>
            <p>Streamlit UI → n8n workflow → Ollama local LLM → HTML report.</p>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# INPUTS
st.markdown('<section class="evaluate-panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Evaluate Content</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Upload brand guidelines or paste copy below. Brand guideline upload is optional.</div>', unsafe_allow_html=True)

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
    errors.append("Missing N8N_WEBHOOK_URL. Add it in Streamlit Cloud → App → Settings → Secrets.")
elif not N8N_WEBHOOK_URL.startswith("http"):
    errors.append("N8N_WEBHOOK_URL must start with http:// or https://")

if email and ("@" not in email or "." not in email.split("@")[-1]):
    errors.append("Email looks invalid. Enter a valid email or leave blank.")

if errors:
    for e in errors:
        st.error(e)

run = st.button("Run Evaluation", disabled=bool(errors))
st.markdown('</section>', unsafe_allow_html=True)

# DECISION SYSTEM
st.markdown('<div class="section-title">Decision System</div>', unsafe_allow_html=True)
st.markdown("""
<div class="decision-row">
    <div class="decision-card pass-card">PASS<br><span>On-brand and ready to use</span></div>
    <div class="decision-card flag-card">FLAG<br><span>Off-brand or rewrite suggested</span></div>
    <div class="decision-card review-card">REVIEW<br><span>Needs human judgment</span></div>
</div>
""", unsafe_allow_html=True)


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
            st.error("Couldn’t reach the n8n webhook. Check ngrok, n8n, and the webhook URL.")
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
    st.markdown("""
- **PASS** = content aligns with the brand voice  
- **FLAG** = content appears misaligned and needs a rewrite  
- **REVIEW** = output needs human verification before action  
""")

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
    body * { color: #E5E7EB !important; }
    h1, h2, h3 { color: #F8FAFC !important; }
    table {
        width: 100% !important;
        border-collapse: collapse !important;
        background: #0F172A !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(56,189,248,0.25) !important;
    }
    th {
        background: #1E293B !important;
        color: #F8FAFC !important;
        font-weight: 800 !important;
        padding: 14px !important;
        border: 1px solid rgba(148,163,184,0.25) !important;
    }
    td {
        background: #0F172A !important;
        color: #E5E7EB !important;
        padding: 14px !important;
        border: 1px solid rgba(148,163,184,0.22) !important;
        vertical-align: top !important;
    }
    tr:nth-child(even) td { background: #111C33 !important; }
    td:nth-child(2) { color: #38BDF8 !important; font-weight: 900 !important; }
</style>
"""
        if "<head>" in html:
            html = html.replace("<head>", "<head>" + aligna_report_css)
        else:
            html = aligna_report_css + html

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
