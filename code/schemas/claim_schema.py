from pydantic import BaseModel


class ClaimExtraction(BaseModel):
    issue: str
    affected_part: str
    summary: str
    severity: str