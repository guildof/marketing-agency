from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class Pack(BaseModel):
    name: str
    description: str
    price_eur: Optional[float] = None

class RoadmapItem(BaseModel):
    semaine: int = Field(ge=1, description="Semaine #1..#13")
    objectifs: List[str]

class AuditOutput(BaseModel):
    score_maturite: int = Field(ge=0, le=100)
    sous_scores: Dict[str, int] = {}
    quick_wins: List[str]
    packs: List[Pack]
    roadmap_90j: List[RoadmapItem]
    assumptions: Optional[List[str]] = None
