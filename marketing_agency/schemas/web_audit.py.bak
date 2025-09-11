from pydantic import BaseModel
from typing import Optional, List, Dict

class DiscoverCite(BaseModel):
    url: str
    snippet: Optional[str] = None
    date: Optional[str] = None  # "YYYY-MM-DD"

class DiscoverURLs(BaseModel):
    website: Optional[str] = None
    gbp: Optional[str] = None
    instagram: Optional[str] = None

class GBP(BaseModel):
    rating: Optional[float] = None
    reviews: Optional[int] = None
    score: int = 0

class Instagram(BaseModel):
    followers: Optional[int] = None
    posts_30d: Optional[int] = None
    score: int = 0

class Website(BaseModel):
    seo_onpage_score: int = 0
    cwv_mobile_score: Optional[int] = None
    score: int = 0

class Audit(BaseModel):
    gbp: GBP
    instagram: Instagram
    website: Website

class Output(BaseModel):
    input: Dict
    discover: Dict
    audit: Audit
    scores: Dict
    actions_90j: List[Dict]
