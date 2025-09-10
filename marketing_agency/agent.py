# marketing_agency/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.logo_create import logo_create_agent
from .sub_agents.marketing_create import marketing_create_agent
from .sub_agents.website_create import website_create_agent
from .sub_agents.audit_create.agent import audit_agent
from .sub_agents.web_audit.agent import run_web_audit

def handle_request(payload: dict):
    task = payload.get("task")

    if task == "web_audit":
        return run_web_audit(payload)


MODEL = "gemini-2.5-pro"

marketing_coordinator = LlmAgent(
    name="marketing_coordinator",
    model=MODEL,
    description=(
        "Establish a powerful online presence and connect with your audience "
        "effectively. Guide you through defining your digital identity, from "
        "choosing the perfect domain name and crafting a professional "
        "website, to strategizing online marketing campaigns, "
        "designing a memorable logo, and creating engaging short videos. "
        "It can also perform a digital audit to evaluate the maturity of a "
        "business and recommend adapted offers."
    ),
    instruction=prompt.MARKETING_COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=website_create_agent),
        AgentTool(agent=marketing_create_agent),
        AgentTool(agent=logo_create_agent),
        AgentTool(agent=audit_agent),  # <- ajout ici
    ],
)

root_agent = marketing_coordinator
