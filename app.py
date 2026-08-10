import streamlit as st
import subprocess
import os

st.set_page_config(page_title="DataGuard: Autonomous PII Governance Agent", layout="wide")

st.markdown("""
    <style>
    [data-testid="stToolbar"] {
        opacity: 1 !important;
        visibility: visible !important;
    }
    .metric-card {
        background-color: var(--secondary-background-color);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        text-align: left;
    }
    .metric-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .metric-value-blue {
        font-size: 1.5rem;
        font-weight: bold;
        color: #4a90e2;
    }
    .metric-value-red {
        font-size: 1.5rem;
        font-weight: bold;
        color: #e74c3c;
    }
    .metric-value-green {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2ecc71;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar with Dropdown Selector matching original design
st.sidebar.markdown("### 🎛️ Agent Control Panel")

target_urn = st.sidebar.selectbox(
    "Target Dataset URN",
    [
        "urn:li:dataset:(urn:li:dataPlatform:postgres,analytics.users,PROD)",
        "urn:li:dataset:(urn:li:dataPlatform:snowflake,finance.payments,PROD)",
        "urn:li:dataset:(urn:li:dataPlatform:bigquery,customer_data.profiles,PROD)"
    ]
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

if st.sidebar.button("🚀 Trigger Agent Execution", use_container_width=True):
    with st.sidebar.spinner("Running agent..."):
        try:
            env = os.environ.copy()
            env["PYTHONPATH"] = "."

            process = subprocess.Popen(
                ["python", "src/agent/runner.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=env
            )
            
            log_box = st.sidebar.empty()
            full_logs = ""
            
            for line in process.stdout:
                full_logs += line
                log_box.code(full_logs, language="bash")
                
            process.wait()
            if process.returncode == 0:
                st.sidebar.success("Pipeline executed successfully!")
            else:
                st.sidebar.error("Execution failed. Check log output.")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.info("**Agent Status:** Online\n\n**Mode:** Offline Fallback Active")

# Main Dashboard Interface
st.title("🛡️ DataGuard: Autonomous PII Governance Agent")
st.subheader("Metadata-Driven Compliance, dbt Code Generation, and Enterprise Graph Remediation")

st.markdown("<br>", unsafe_allow_html=True)

# 3 Metric Cards Block
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Target Dataset</div>
            <div class="metric-value-blue">analytics.users</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Detected PII Fields</div>
            <div class="metric-value-red">2 (High Risk)</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Compliance Status</div>
            <div class="metric-value-green">GDPR Enforced</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Generated dbt SQL Model", 
    "🔄 DataHub Metadata Change Proposal", 
    "📊 PII Scan Audit Report", 
    "⚙️ Pipeline Execution Logs"
])

with tab1:
    st.markdown("### Generated dbt SQL Model")
    st.code("""
SELECT 
    MD5(user_id) AS user_id,
    REGEXP_REPLACE(email, '(?i)(?<=^.).*?(?=@)', '***') AS email,
    REGEXP_REPLACE(phone_number, '^.*(.{4})$', '\\\\1') AS phone_number,
    created_at
FROM {{ source('production', 'users') }}
    """, language="sql")

with tab2:
    st.markdown("### Serialized Metadata Change Proposal (MCP)")
    st.json({
        "entityType": "dataset",
        "changeType": "UPSERT",
        "aspect": {
            "name": "datasetProperties",
            "value": {
                "customProperties": {
                    "pii_governance": "compliant",
                    "masked_fields": "email, phone_number"
                }
            }
        }
    })

with tab3:
    st.markdown("### PII Scan Audit Report")
    st.dataframe(
        {
            "Column": ["user_id", "email", "phone_number", "created_at"],
            "Detected Type": ["Identifier", "Email", "Phone", "Timestamp"],
            "Risk Level": ["Medium", "High", "High", "Low"],
            "Action Taken": ["Hashed", "Masked", "Truncated", "None"]
        },
        use_container_width=True
    )

with tab4:
    st.markdown("### Pipeline Execution Logs")
    st.info("Trigger agent execution from the sidebar to view logs.")
