import subprocess
import streamlit as st

st.title("DataGuard: Autonomous PII Governance Agent")

# Inside your sidebar or button handler:
if st.button("Trigger Agent Execution"):
    with st.spinner("Running DataGuard Agent pipeline..."):
        try:
            # Run your underlying python agent script and capture output
            process = subprocess.Popen(
                ["python", "agent.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Create an empty container for real-time logs
            log_placeholder = st.empty()
            full_logs = ""
            
            # Stream the output live to the UI
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
