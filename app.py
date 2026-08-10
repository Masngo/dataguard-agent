import streamlit as st
import subprocess

st.set_page_config(page_title="DataGuard: Autonomous PII Governance Agent", layout="wide")

st.markdown("""
    <style>
    [data-testid="stToolbar"] {
        opacity: 1 !important;
        visibility: visible !important;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("Agent Control Panel")
dataset_urn = st.sidebar.selectbox(
    "Target Dataset URN",
    ["urn:li:dataset:(urn:li:dataPlatform:postgres,public.users,PROD)"]
)

if st.sidebar.button("Trigger Agent Execution"):
    with st.spinner("Running DataGuard Agent pipeline..."):
        try:
            process = subprocess.Popen(
                ["python", "src/agent/runner.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            log_placeholder = st.empty()
            full_logs = ""
            
            for line in process.stdout:
                full_logs += line
                log_placeholder.code(full_logs, language="bash")
                
            process.wait()
            if process.returncode == 0:
                st.success("Pipeline execution completed successfully!")
            else:
                st.error("Pipeline execution failed. Check logs above.")
        except Exception as e:
            st.error(f"Failed to execute pipeline: {e}")

st.title("🛡️ DataGuard: Autonomous PII Governance Agent")
st.subheader("Metadata-Driven Compliance, dbt Code Generation, and Enterprise Graph Remediation")
