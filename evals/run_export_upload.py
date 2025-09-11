import os, json
from marketing_agency.utils.pdf_export import export_audit_to_pdf_and_upload
from marketing_agency.schemas.audit import AuditOutput

with open("evals/sample_audit.json","r",encoding="utf-8") as f:
    data = json.load(f)

# validation pydantic
AuditOutput(**data)

pdf, url = export_audit_to_pdf_and_upload(data, client_name=os.getenv("CLIENT_NAME","Client"))
print("PDF local :", pdf)
print("Signed URL (7j) :", url or "(pas d'upload — variable AGENT_PDF_BUCKET non définie)")
