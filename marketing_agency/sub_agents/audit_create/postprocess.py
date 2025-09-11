import os, json
from typing import Optional
from marketing_agency.utils.json_first import extract_first_json
from marketing_agency.schemas.audit import AuditOutput
from marketing_agency.utils.pdf_export import export_audit_to_pdf_and_upload

def postprocess_agent_output(response_text: str, client_name: Optional[str] = None) -> str:
    json_str = extract_first_json(response_text or "")
    if not json_str:
        return response_text

    data = json.loads(json_str)
    audit = AuditOutput(**data)

    client_name = client_name or os.getenv("CLIENT_NAME", "Client")
    _, url = export_audit_to_pdf_and_upload(audit.model_dump(), client_name=client_name)

    lines = []
    lines.append("### Audit digital – synthèse")
    lines.append(f"- **Score de maturité** : {audit.score_maturite}/100")

    # Quick wins
    if audit.quick_wins:
        # accept list[str] ou list[objects] (robuste)
        def _to_text(x):
            try:
                return x if isinstance(x, str) else (x.get("action") or str(x))
            except Exception:
                return str(x)
        qws = ", ".join(_to_text(x) for x in audit.quick_wins)
        lines.append("- **Quick wins** : " + qws)

    # Packs
    if audit.packs:
        def _price(p):
            try:
                v = getattr(p, "price_eur", None)
                return f"{int(v)}€" if v is not None else "sur devis"
            except Exception:
                return "sur devis"
        def _name(p):
            return getattr(p, "name", getattr(p, "nom", "Pack"))
        packs = " · ".join([f"**{_name(p)}** ({_price(p)})" for p in audit.packs])
        lines.append(f"- **Packs recommandés** : {packs}")

    if url:
        lines.append(f"📄 **Rapport PDF (7 jours)** : {url}")

    lines.append("\nSouhaites-tu qu’on valide un pack et qu’on enclenche la roadmap 90 jours ?")
    return "\n".join(lines)
