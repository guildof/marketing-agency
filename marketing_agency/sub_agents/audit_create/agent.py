import os
from pydantic import ValidationError
from google.adk.agents import LlmAgent
from .prompt import AUDIT_AGENT_PROMPT
from .postprocess import postprocess_agent_output

MODEL = os.getenv("ROOT_MODEL", "gemini-2.5-pro")

def _make_agent():
    base = dict(
        name="audit_agent",
        model=MODEL,
        description="Analyse la maturité digitale et propose 3 packs adaptés",
        instruction=AUDIT_AGENT_PROMPT,
    )
    # Essaye d'abord 'postprocess', sinon 'response_adapter' (selon version ADK)
    try:
        return LlmAgent(**base, postprocess=postprocess_agent_output)
    except Exception:
        return LlmAgent(**base, response_adapter=postprocess_agent_output)

audit_agent = _make_agent()
