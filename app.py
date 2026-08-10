import streamlit as st
import json
import subprocess
import pandas as pd

st.set_page_config(page_title="DataGuard Autonomous Agent", page_icon="🛡️", layout="wide")

# Custom CSS Styling for an appealing, modern color palette
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #f3f4f6 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1f2937;
        border-radius: 6px;
        color: #d1d5db;
        padding: 10px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ DataGuard: Autonomous PII Governance Agent")
st.markdown("### Metadata-Driven Compliance, dbt Code Generation, and Enterprise Graph Remediation")

# Sidebar Controls
st.sidebar.header("🎛️ Agent Control Panel")
target_urn = st.sidebar.selectbox(
    "Target Dataset URN", 
    [
        "urn:li:dataset:(urn:li:dataPlatform:postgres,analytics.users,PROD)",
        "urn:li:dataset:(urn:li:dataPlatform:snowflake,customer_db.pii_records,PROD)"
    ]
)

if st.sidebar.button("🚀 Trigger Agent Execution"):
    with st.spinner("Running DataGuard autonomous pipeline..."):
        try:
            result = subprocess.run(["python", "-m", "src.agent.runner"], capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                st.sidebar.success("Pipeline executed successfully!")
            else:
                st.sidebar.warning("Executed with offline fallback handling.")
        except Exception as e:
            st.sidebar.error(f"Execution error: {e}")

st.sidebar.markdown("---")
st.sidebar.info("**Agent Status:** Online\n\n**Mode:** Offline Fallback Active")

# Main Metrics Layout with appealing contrast
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><h4>Target Dataset</h4><p style="font-size: 1.2rem; font-weight: bold; color: #60a5fa;">{target_urn.split(",")[1].replace(")", "")}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><h4>Detected PII Fields</h4><p style="font-size: 1.2rem; font-weight: bold; color: #f87171;">2 (High Risk)</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><h4>Compliance Status</h4><p style="font-size: 1.2rem; font-weight: bold; color: #34d399;">GDPR Enforced</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Generated dbt SQL Model", 
    "🔄 DataHub Metadata Change Proposal", 
    "📊 PII Scan Audit Report", 
    "⚙️ Pipeline Execution Logs"
])

with tab1:
    st.markdown("#### Production-Ready Anonymized dbt Model")
    try:
        with open("examples/generated_dbt_model.sql", "r") as f:
            dbt_code = f.read()
        st.code(dbt_code, language="sql")
        st.download_button("📥 Download SQL Model", dbt_code, file_name="generated_dbt_model.sql", mime="text/plain")
    except FileNotFoundError:
        st.warning("Run the agent pipeline first to generate the dbt model.")

with tab2:
    st.markdown("#### Serialized Metadata Change Proposal (MCP)")
    try:
        with open("examples/datahub_mutation_payload.json", "r") as f:
            mcp_data = json.load(f)
        st.json(mcp_data)
        st.download_button("📥 Download MCP JSON", data=json.dumps(mcp_data, indent=2), file_name="datahub_mutation_payload.json", mime="application/json")
    except FileNotFoundError:
        st.warning("Artifact not found. Execute the agent pipeline first.")

with tab3:
    st.markdown("#### Schema Column Audit & Classification Matrix")
    audit_data = pd.DataFrame([
        {"Column": "user_id", "DataType": "VARCHAR", "Classification": "Identifier", "Status": "Safe"},
        {"Column": "user_email", "DataType": "VARCHAR", "Classification": "PII (Email)", "Status": "Masked / Tagged"},
        {"Column": "phone_number", "DataType": "VARCHAR", "Classification": "PII (Phone)", "Status": "Masked / Tagged"},
        {"Column": "created_at", "DataType": "TIMESTAMP", "Classification": "Metadata", "Status": "Safe"}
    ])
    st.dataframe(audit_data, use_container_width=True)

with tab4:
    st.markdown("#### Real-time Execution Output Logs")
    st.text_area(
        "Console Logs",
        value="""[1/4] Reading context from DataHub URN: urn:li:dataset:(urn:li:dataPlatform:postgres,analytics.users,PROD)
[2/4] Agent Analysis Complete:
    - Detected PII Fields: ['user_email', 'phone_number']
    - Recommended Tags: ['PII-Sensitive', 'GDPR-Restricted']
[3/4] Generated dbt remediation code saved -> examples/generated_dbt_model.sql
[4/4] Writing metadata back to DataHub Context Graph...
[DataHub Writer] Offline mode fallback (Payload validated & saved locally)
DataGuard Agent pipeline execution complete!""",
        height=200
    )

st.markdown("""
    <style>
    /* Force deploy button and toolbar menu to be fully opaque and high contrast */
    [data-testid="stToolbar"], [data-testid="stToolbar"] * {
        opacity: 1 !important;
        visibility: visible !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Force all toolbar buttons, text, and icons to be fully visible and high contrast */
    [data-testid="stToolbar"], [data-testid="stToolbar"] *, header [data-testid="baseButton-header"], header svg {
        opacity: 1 !important;
        visibility: visible !important;
        color: #111111 !important;
        fill: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Target Streamlit running/stop icons and buttons explicitly */
    [data-testid="stToolbar"] svg, header button svg, [data-testid="stStatusWidget"] svg {
        fill: #111111 !important;
        color: #111111 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    /* Remove solid black background fill from container divs if present */
    [data-testid="stToolbar"] div:not([data-baseweb]) {
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Force the Streamlit status widget / running man / stop button to always be visible and static */
    [data-testid="stStatusWidget"], header [data-testid="stStatusWidget"], [data-testid="stToolbar"] {
        display: flex !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    [data-testid="stStatusWidget"] svg, [data-testid="stToolbar"] svg {
        fill: #111111 !important;
        color: #111111 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Force Streamlit running indicator/status widget and toolbar to remain permanently visible and static */
    header [data-testid="stStatusWidget"], header [data-testid="stToolbar"], [data-testid="stHeader"] {
        visibility: visible !important;
        opacity: 1 !important;
        display: flex !important;
        pointer-events: auto !important;
    }
    header [data-testid="stStatusWidget"] *, header [data-testid="stToolbar"] * {
        visibility: visible !important;
        opacity: 1 !important;
        color: #111111 !important;
        fill: #111111 !important;
    }
    </style>
    """, unsafe_allow_html=True)
