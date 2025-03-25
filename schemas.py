from pydantic import BaseModel
from typing import Optional

class ComplianceRequest(BaseModel):
    control: str
    description: Optional[str] = None
    maturity_level: float

class ComplianceResponse(BaseModel):
    id: int
    assessment_date: str
    overall_score: float

    class Config:
        from_attributes = True

class AssessmentRequest(BaseModel):
    security_domain: str
    risk_level: int
    description: str
