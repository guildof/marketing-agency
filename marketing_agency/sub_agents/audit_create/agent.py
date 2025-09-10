from google.adk.agents import LlmAgent
from pydantic import ValidationError

from marketing_agency.schemas import AuditOutput
from marketing_agency.utils.json_first import extract_first_json
from .prompt import AUDIT_AGENT_PROMPT

MODEL = "gemini-2.5-pro"

def _validate_and_format_audit_output(response_text: str) -> str:
    """Extrait le 1er JSON, valide via Pydantic, renvoie le JSON propre."""
    json_str = extract_first_json(response_text or "")
    if not json_str:
        raise ValueError("Audit agent: aucun JSON détecté en tête de réponse.")
    try:
        AuditOutput.model_validate_json(json_str)
    except ValidationError as e:
        raise ValueError(f"Audit agent: JSON invalide vs schéma. Détails: {e}") from e
    return response_text

audit_agent = LlmAgent(
    name="audit_agent",
    model=MODEL,
    description="Analyse la maturité digitale et propose 3 packs adaptés"
)
