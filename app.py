import base64
import requests
import streamlit as st

st.set_page_config(page_title="Madison Brand Voice Checker", layout="wide")

# -----------------------------
# CONFIG
# -----------------------------
# Streamlit Cloud → App → Settings → Secrets
# Example value:
# N8N_WEBHOOK_URL = "https://<YOUR_NGROK_DOMAIN>/webhook/madison/run"
N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", "").strip()

# -----------------------------
# BASIC INFO (6 pts)
# -----------------------------
st.title("Madison Brand Voice Checker (Prototype)")
st.caption(
    "Evaluates content against a learned brand voice and returns PASS / FLAG / REVIEW with a downloadable HTML report."
)

with st.expander("About", expanded=False):
    st.markdown(
        """
**What it does**
- Triggers my Assignment 4 n8n workflow via a webhook
- Returns **PASS / FLAG / REVIEW** counts + a human-readable report
- Lets a non-technical user preview + download the HTML report

**Who it’s for**
Marketing teams, social media managers, and brand managers.

**Tech stack**
Streamlit (Cloud UI) → n8n (workflow) → Ollama (local LLM) → HTML report

**Built by**
Vivek Nikam  
Portfolio/Contact: *(paste your link here)*
"""
    )

st.divider()

# -----------------------------
# INPUTS (7 pts)
# -----------------------------
st.header("Inputs")

st.caption(
    "Note: In Assignment 4, the workflow evaluates built-in sources. PDF upload is included for user testing and A6 expansion."
)

col1, col2 = st.columns(2)

with col1:
    brand_pdf = st.file_uploader(
        "Upload Brand Guidelines (PDF) — optional",
        type=["pdf"],
        help="A4 workflow uses built-in sources. This input is for UX completeness + future expansion.",
    )

with col2:
    copy_text = st.text_area(
        "Copy to evaluate (optional for testing)",
        height=160,
        placeholder="Example: Introducing our latest feature to help marketers move faster with confidence...",
        help="Optional input to pass into the workflow (for logging/testing).",
    )

email = st.text_input(
    "Email (optional)",
    placeholder="name@example.com",
    help="Optional. Used for workflow logging or emailing if your workflow supports it.",
)

# Validation
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
# OUTPUTS (7 pts)
# -----------------------------
st.header("Outputs")


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

    with st.spinner("Running workflow… (can take up to 1–2 minutes)"):
        # 1) Network / connectivity errors
        try:
            resp = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=300)
        except requests.exceptions.RequestException as ex:
            st.error(
                "Couldn’t reach the n8n webhook. Check: ngrok running + n8n running + correct webhook URL."
            )
            st.code(str(ex))
            st.stop()

        # 2) HTTP errors
        if not resp.ok:
            st.error(f"n8n returned an error ({resp.status_code}).")
            st.code(resp.text[:2000])
            st.download_button(
                "Download Raw Response (debug)",
                data=resp.text.encode("utf-8"),
                file_name="n8n_error_response.txt",
                mime="text/plain",
            )
            st.stop()

        # 3) JSON parse errors (very common)
        try:
            data = resp.json()
        except Exception:
            st.error("Webhook responded, but it wasn’t valid JSON.")
            st.code(resp.text[:2000])
            st.download_button(
                "Download Raw Response (debug)",
                data=resp.text.encode("utf-8"),
                file_name="n8n_non_json_response.txt",
                mime="text/plain",
            )
            st.stop()

    # Must contain ok=true per your workflow response
    if not data.get("ok"):
        st.error("Workflow returned ok=false (or missing ok).")
        st.json(data)
        st.download_button(
            "Download Raw JSON (debug)",
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
- **PASS** = aligns with brand voice  
- **FLAG** = misaligned → rewrite suggested  
- **REVIEW** = model output couldn’t be parsed → safe fallback + re-run recommended  
"""
    )

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
        st.download_button(
            "Download Raw JSON (debug)",
            data=resp.text.encode("utf-8"),
            file_name="n8n_response.json",
            mime="application/json",
        )
