from typing import List, Optional
from pydantic import BaseModel

class Direction(BaseModel):
    name: str
    palette: List[str]  # hex
    typos: List[str]
    do: List[str]
    dont: List[str]

class LogoOutput(BaseModel):
    directions: List[Direction]
    claims: Optional[List[str]] = None
    assumptions: Optional[List[str]] = None
