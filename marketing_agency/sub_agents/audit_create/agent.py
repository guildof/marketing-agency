import os
from google.adk.agents import LlmAgent
# Utilise imports absolus pour éviter les erreurs en REPL si lancé isolément
from marketing_agency.sub_agents.audit_create.prompt import AUDIT_AGENT_PROMPT
from marketing_agency.sub_agents.audit_create.postprocess import postprocess_agent_output

MODEL = os.getenv("ROOT_MODEL", "gemini-2.5-pro")

# Instancie l'agent SANS fournir de callable en kwargs (évite pydantic extra_forbidden)
audit_agent = LlmAgent(
    name="audit_agent",
    model=MODEL,
    description="Analyse la maturité digitale et propose 3 packs adaptés",
    instruction=AUDIT_AGENT_PROMPT,
)

# Attache la fonction de post-process après instanciation.
# ADK/runner peut ensuite trouver l'attribut 'postprocess' ou 'response_adapter' à l'exécution.
try:
    setattr(audit_agent, "postprocess", postprocess_agent_output)
except Exception:
    try:
        setattr(audit_agent, "response_adapter", postprocess_agent_output)
    except Exception:
        def _pp_wrapper(text, *args, **kwargs):
            return postprocess_agent_output(text)
        setattr(audit_agent, "postprocess", _pp_wrapper)
