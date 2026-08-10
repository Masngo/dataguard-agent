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
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### 🤖 Agent Control Panel")
dataset_urn = st.sidebar.text_input(
    "Target Dataset URN",
    value="urn:li:dataset:(urn:li:dataPlatform:postgres,public.users,PROD)"
)

log_container = st.sidebar.empty()

if st.sidebar.button("🚀 Trigger Agent Execution"):
    with st.sidebar.spinner("Executing pipeline..."):
        try:
            # Pass current environment with PYTHONPATH set to the root folder
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
            
            full_logs = ""
            for line in process.stdout:
                full_logs += line
                log_container.code(full_logs, language="bash")
                
            process.wait()
            if process.returncode == 0:
                st.sidebar.success("Pipeline executed successfully!")
            else:
                st.sidebar.error("Execution failed.")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.info("**Agent Status:** Online\n\n**Mode:** Offline Fallback Active")

# Main Page Header
st.title("🛡️ DataGuard: Autonomous PII Governance Agent")
st.subheader("Metadata-Driven Compliance, dbt Code Generation, and Enterprise Graph Remediation")

st.markdown("<br>", unsafe_allow_html=True)

# Metric Cards Layout
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(label="Target Dataset", value="analytics.users")
with c2:
    st.metric(label="Detected PII Fields", value="2 (High Risk)")
with c3:
    st.metric(label="Compliance Status", value="GDPR Enforced")

st.markdown("<br>", unsafe_allow_html=True)

# Tabs Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Generated dbt SQL Model", 
    "🔄 DataHub Metadata Change Proposal", 
    "📊 PII Scan Audit Report", 
    "⚙️ Pipeline Execution Logs"
])

with tab1:
    st.markdown("#### Generated dbt SQL Model")
    st.code("""
SELECT 
    MD5(user_id) AS user_id,
    REGEXP_REPLACE(email, '(?i)(?<=^.).*?(?=@)', '***') AS email,
    REGEXP_REPLACE(phone_number, '^.*(.{4})$', '\\\\1') AS phone_number,
    created_at
FROM {{ source('production', 'users') }}
    """, language="sql")

with tab2:
    st.markdown("#### Serialized Metadata Change Proposal (MCP)")
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
    st.markdown("#### PII Scan Audit Report")
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
    st.markdown("#### Pipeline Execution Logs")
    st.info("Trigger the agent execution from the sidebar to view dynamic logs.")
