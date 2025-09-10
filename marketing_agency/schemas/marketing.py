from typing import List, Optional
from pydantic import BaseModel, Field

class AdsKeyword(BaseModel):
    keyword: str
    match_type: Optional[str] = None  # broad|phrase|exact

class AdsGroup(BaseModel):
    nom: str
    mots_cles: List[AdsKeyword]

class AdsCampaign(BaseModel):
    nom: str
    budget_journalier_eur: float = Field(ge=0)
    groupes: List[AdsGroup]

class SocialPost(BaseModel):
    semaine: int = Field(ge=1, le=13)
    plateforme: str
    idee: str

class CRMMinimal(BaseModel):
    outil: Optional[str] = None
    actions: List[str] = []

class KPI(BaseModel):
    nom: str
    cible: float

class MarketingOutput(BaseModel):
    plan_90j: List[str]  # résumé des 13 semaines ou 3 phases
    ads_google: List[AdsCampaign]
    social_organique: List[SocialPost]
    crm_minimal: CRMMinimal
    kpis: List[KPI]
    assumptions: Optional[List[str]] = None
