# marketing_agency/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.logo_create import logo_create_agent
from .sub_agents.marketing_create import marketing_create_agent
from .sub_agents.website_create import website_create_agent
from .sub_agents.audit_create.agent import audit_agent
from .sub_agents.web_audit.agent import run_web_audit

from .utils.json_first import extract_first_json


def format_for_client(response_text: str) -> str:
    if not response_text:
        return ""
    json_str = extract_first_json(response_text)
    if not json_str:
        return response_text
    end_idx = response_text.find(json_str) + len(json_str)
    markdown_part = response_text[end_idx:].strip()
    return markdown_part if markdown_part else response_text


MODEL = "gemini-2.5-pro"

# Ici on reste sur un agent valide
marketing_coordinator = LlmAgent(
    name="marketing_coordinator",
    model=MODEL,
    description=(
        "Coordinateur marketing : site web, plan marketing, logo, audit."
    ),
    instruction=prompt.MARKETING_COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=website_create_agent),
        AgentTool(agent=marketing_create_agent),
        AgentTool(agent=logo_create_agent),
        AgentTool(agent=audit_agent),
    ],
)

# On expose bien un agent, pas une fonction
root_agent = marketing_coordinator
