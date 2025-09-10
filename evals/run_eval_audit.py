import json
from marketing_agency.schemas.audit import AuditOutput

with open("evals/sample_audit.json", "r", encoding="utf-8") as f:
    data = json.load(f)

audit = AuditOutput(**data)
print("✅ JSON valide")
print(audit)
