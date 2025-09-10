import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from marketing_agency.schemas.audit import AuditOutput

# Exemple : réponse JSON de l'agent
with open("evals/sample_audit.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Validation stricte
audit = AuditOutput(**data)

# Prépare template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("audit_report.html")

# Rendu HTML
html_out = template.render(client="Fleurs de Loire", audit=audit)

# Génère PDF
HTML(string=html_out).write_pdf("exports/audit_report.pdf")

print("✅ Rapport généré : exports/audit_report.pdf")
