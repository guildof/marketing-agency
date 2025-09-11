from typing import List, Dict, Optional
from pydantic import BaseModel

class WebsiteCode(BaseModel):
    zip_base64: str  # archive du site

class WebsiteOutput(BaseModel):
    code_site: WebsiteCode
    arbo: List[str]
    seo_onpage: Optional[Dict[str, str]] = None
    tracking_plan: Optional[List[str]] = None
    instructions_deploiement: List[str]
    assumptions: Optional[List[str]] = None
