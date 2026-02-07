from app.database import engine, Base
from app.models.cve import CVE
Base.metadata.create_all(engine)
