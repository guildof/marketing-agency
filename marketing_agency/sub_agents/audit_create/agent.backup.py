from google.adk.agents import LlmAgent
from .prompt import AUDIT_AGENT_PROMPT

MODEL = "gemini-2.5-pro"

audit_agent = LlmAgent(
    name="audit_agent",
    model=MODEL,
    description="Analyse la maturité digitale et propose 3 packs adaptés",
    instruction=AUDIT_AGENT_PROMPT,
)
