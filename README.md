# DataGuard Agent: Autonomous PII Governance & dbt Pipeline Engine

DataGuard Agent is an autonomous data governance tool built for modern data stacks. It analyzes database schemas, detects untagged Personally Identifiable Information (PII), generates masked dbt transformation models, and emits Metadata Change Proposals (MCPs) to sync compliance schemas directly back to the DataHub catalog.

## Features

* **Autonomous PII Discovery:** Inspects target database schemas (PostgreSQL, Snowflake, BigQuery) to locate sensitive columns and untagged PII.
* **Metadata-Aware Code Generation:** Automatically compiles production-ready, obfuscated dbt SQL models with built-in data masking.
* **DataHub Graph Integration:** Serializes metadata mutation payloads and synchronizes governance tags and assertions with the DataHub catalog.
* **Interactive Streamlit Dashboard:** Provides a real-time web interface to review audit reports, examine generated dbt code, and monitor pipeline executions.

## Repository Structure

```text
dataguard-agent/
├── app.py                      # Interactive Streamlit dashboard interface
├── requirements.txt            # Project dependencies
├── LICENSE                     # Apache 2.0 License
├── README.md                   # Project documentation
├── src/
│   ├── agent/                  # Core PII detection and runner scripts
│   └── datahub_client/         # MCP emitter and catalog sync modules
└── examples/
    ├── generated_dbt_model.sql # Sample anonymized dbt model output
    └── datahub_mutation_payload.json # Sample metadata mutation payload

```

## Setup & Installation

* **Clone the Repository:**
```bash
git clone [https://github.com/Masngo/dataguard-agent.git](https://github.com/Masngo/dataguard-agent.git)
cd dataguard-agent

```


* **Create and Activate a Virtual Environment:**
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows (Git Bash)
# source venv/bin/activate    # On macOS/Linux

```


* **Install Dependencies:**
```bash
pip install -r requirements.txt

```



## Running the Application Locally

## Live Demo
Check out the live application here: [DataGuard Autonomous Agent](https://dataguard-agent.streamlit.app) 

Launch the interactive Streamlit dashboard to test functionality, view generated artifacts, and inspect governance reports:

```bash
streamlit run app.py

```

This will start the local server, typically accessible at `http://localhost:8501`.

## Artifacts & Examples

Review pre-compiled examples of agent outputs inside the `examples/` directory:

* `examples/generated_dbt_model.sql`: Production-ready anonymized dbt model code.
* `examples/datahub_mutation_payload.json`: Serialized metadata mutation payload emitted to the DataHub graph.

## License

This project is licensed under the terms of the Apache License 2.0. See the LICENSE file for details.

```

```
