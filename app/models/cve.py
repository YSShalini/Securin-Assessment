from sqlalchemy import Column, String, Float, DateTime, JSON
from app.database import Base

class CVE(Base):
    __tablename__ = "cves"

    cve_id = Column(String, primary_key=True, index=True)
    identifier = Column(String)
    description = Column(String)
    published = Column(DateTime)
    last_modified = Column(DateTime)
    status = Column(String)
    cvss_v2 = Column(Float, nullable=True)
    cvss_v3 = Column(Float, nullable=True)
    raw_metrics = Column(JSON)
    cpe = Column(JSON)
