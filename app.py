import base64
import requests
import streamlit as st

st.set_page_config(page_title="Madison Brand Voice Checker", layout="wide")

# -----------------------------
# CONFIG
# -----------------------------
# Streamlit Cloud will store this in Secrets (Settings → Secrets)
# Example value later: https://<your-public-tunnel-domain>/webhook/madison/run
N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", "")

# -----------------------------
# BASIC INFO (6 pts)
# -----------------------------
st.title("Madison Brand Voice Checker (Prototype)")
st.caption("Evaluates marketing copy against a learned brand voice and returns PASS / FLAG / REVIEW with a downloadable HTML report.")

with st.expander("About", expanded=False):
    st.markdown("""
**What it does**
- Triggers my existing Assignment 4 n8n workflow via a webhook
- Outputs **PASS / FLAG / REVIEW** counts + report
- Provides a downloadable HTML report

**Who it’s for**
Marketing teams, social media managers, and brand managers.

**Tech stack**
Streamlit (Cloud UI) → n8n (local workflow) → Ollama (local LLM) → HTML report

**Built by**
Vivek Nikam  
Portfolio/Contact: *(paste your link here)*
""")

st.divider()

# -----------------------------
# INPUTS (7 pts)
# -----------------------------
st.header("Inputs")

col1, col2 = st.columns(2)

with col1:
    brand_pdf = st.file_uploader(
        "Upload Brand Guidelines (PDF) — optional",
        type=["pdf"],
        help="Optional for user testing. Current A4 workflow runs its built-in sources.",
    )

with col2:
    copy_text = st.text_area(
        "Copy to evaluate (optional for testing)",
        height=160,
        placeholder="Example: Introducing our latest feature to help marketers move faster with confidence...",
    )

email = st.text_input(
    "Email (optional)",
    placeholder="name@example.com",
    help="Optional. The workflow may email results; UI also provides download.",
)

# Validation
errors = []
if not N8N_WEBHOOK_URL:
    errors.append("Missing N8N_WEBHOOK_URL secret. Add it in Streamlit Cloud → App → Settings → Secrets.")

if email and ("@" not in email or "." not in email.split("@")[-1]):
    errors.append("Email looks invalid. Enter a valid email or leave blank.")

if errors:
    for e in errors:
        st.error(e)

run = st.button("Run Evaluation", disabled=bool(errors))

st.divider()

# -----------------------------
# OUTPUTS (7 pts)
# -----------------------------
st.header("Outputs")

def decode_report(report_b64: str) -> str:
    if not report_b64:
        return ""
    return base64.b64decode(report_b64).decode("utf-8", errors="replace")

if run:
    # We are NOT changing A4 workflow.
    # We send optional fields for UI testing / logging purposes.
    payload = {
        "email": email,
        "user_copy": copy_text,
        "uploaded_pdf": bool(brand_pdf),
    }

    with st.spinner("Running workflow… (can take up to 1–2 minutes)"):
        try:
            resp = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=300)
            resp.raise_for_status()
            data = resp.json()
        except Exception as ex:
            st.error("Failed to call the n8n webhook. Ensure your tunnel is running and n8n is running locally.")
            st.code(str(ex))
            st.stop()

    if not data.get("ok"):
        st.error("Workflow returned ok=false or missing fields.")
        st.json(data)
        st.stop()

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Items", data.get("total_items", "—"))
    c2.metric("PASS", data.get("passed", "—"))
    c3.metric("FLAG", data.get("flagged", "—"))
    c4.metric("REVIEW", data.get("review", "—"))

    st.markdown("### Key Insights")
    st.markdown("""
- **PASS** = aligns with brand voice  
- **FLAG** = misaligned → rewrite suggested  
- **REVIEW** = model output couldn’t be parsed → safe fallback  
""")

    st.caption(f"Generated at: {data.get('generated_at', '—')}")

    # Report
    report_name = data.get("report_file_name", "brand_voice_report.html")
    report_b64 = data.get("report_base64", "")
    html = decode_report(report_b64)

    st.markdown("### HTML Report Preview")
    if html:
        st.components.v1.html(html, height=650, scrolling=True)

        st.download_button(
            "Download HTML Report",
            data=html.encode("utf-8"),
            file_name=report_name,
            mime="text/html",
        )
    else:
        st.warning("No report returned (report_base64 missing/empty).")
