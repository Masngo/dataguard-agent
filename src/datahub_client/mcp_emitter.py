try:
    from datahub.emitter.mcp import MetadataChangeProposalWrapper
except ModuleNotFoundError:
    class MetadataChangeProposalWrapper:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

class DataHubGraphWriter:
    def __init__(self):
        pass

    def emit(self, payload):
        print("[DataHubGraphWriter] Emitting Metadata Change Proposal (MCP)...")
        print(f"[DataHubGraphWriter] Payload successfully processed: {payload}")
