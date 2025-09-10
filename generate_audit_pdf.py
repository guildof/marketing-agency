import json
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Import Pydantic schema
from marketing_agency.schemas.audit import AuditOutput

TEMPLATES_DIR = "templates"
EXPORTS_DIR = "exports"
os.makedirs(EXPORTS_DIR, exist_ok=True)

def eur(v):
    try:
        return f"{float(v):,.0f} €".replace(",", " ").replace(".0", "")
    except Exception:
        return v

def generate_pdf_from_audit(audit_data: dict, client_name: str = "Client") -> str:
    # Valide la payload
    audit = AuditOutput(**audit_data)

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    env.filters["eur"] = eur
    template = env.get_template("audit_report.html")

    html_out = template.render(client=client_name, audit=audit, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_client = "".join(c if c.isalnum() or c in ('_','-') else '_' for c in client_name)[:40]
    out_name = f"audit_report_{safe_client}_{ts}.pdf"
    out_path = os.path.join(EXPORTS_DIR, out_name)

    HTML(string=html_out).write_pdf(out_path)
    print(f"✅ Rapport généré : {out_path}")
    return os.path.abspath(out_path)

if __name__ == "__main__":
    sample_path = "evals/sample_audit.json"
    with open(sample_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    generate_pdf_from_audit(data, client_name="Fleurs_de_Loire")
