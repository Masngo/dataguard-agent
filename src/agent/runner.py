import json
from src.agent.pii_detector import PIIDetectorAgent
from src.datahub_client.mcp_emitter import DataHubGraphWriter

def run_dataguard_pipeline():
    print("=" * 60)
    print("🚀 Running DataGuard Autonomous Remediation Agent")
    print("=" * 60)

    target_dataset_urn = "urn:li:dataset:(urn:li:dataPlatform:postgres,analytics.users,PROD)"
    mock_schema_columns = [
        {"name": "user_id", "type": "INT"},
        {"name": "created_at", "type": "TIMESTAMP"},
        {"name": "user_email", "type": "VARCHAR"},
        {"name": "phone_number", "type": "VARCHAR"}
    ]

    print(f"[1/4] Reading context from DataHub URN:\n      {target_dataset_urn}\n")

    agent = PIIDetectorAgent()
    detected_pii, recommended_tags = agent.inspect_schema(mock_schema_columns)

    print(f"[2/4] Agent Analysis Complete:")
    print(f"      - Detected PII Fields: {detected_pii}")
    print(f"      - Recommended Tags:   {recommended_tags}\n")

    dbt_model_code = agent.generate_dbt_masking_model("users", detected_pii)
    
    with open("examples/generated_dbt_model.sql", "w") as f:
        f.write(dbt_model_code)
    print("[3/4] Generated dbt remediation code saved -> examples/generated_dbt_model.sql\n")

    # Generate mutation payload artifact for submission
    mutation_payload = {
        "entityType": "dataset",
        "entityUrn": target_dataset_urn,
        "changeType": "UPSERT",
        "aspectName": "globalTags",
        "aspect": {
            "tags": [{"tag": f"urn:li:tag:{t}"} for t in recommended_tags]
        }
    }
    with open("examples/datahub_mutation_payload.json", "w") as f:
        json.dump(mutation_payload, f, indent=2)

    print("[4/4] Writing metadata back to DataHub Context Graph...")
    writer = DataHubGraphWriter()
    writer.attach_pii_tags(target_dataset_urn, recommended_tags)
    writer.emit_pii_assertion(target_dataset_urn)

    print("\n" + "=" * 60)
    print(" DataGuard Agent pipeline execution complete!")
    print("=" * 60)

if __name__ == "__main__":
    run_dataguard_pipeline()
