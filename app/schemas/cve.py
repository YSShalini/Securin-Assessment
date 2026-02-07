from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class CVEBase(BaseModel):
    cve_id: str
    identifier: Optional[str]
    published: datetime
    last_modified: datetime
    status: Optional[str]

    class Config:
        orm_mode = True


class CVEListResponse(BaseModel):
    total: int
    data: list[CVEBase]


class CVEDetailResponse(CVEBase):
    description: Optional[str]
    cvss_v2: Optional[float]
    cvss_v3: Optional[float]
    raw_metrics: Optional[Any]
    cpe: Optional[Any]
