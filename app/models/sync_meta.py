# app/models/sync_meta.py

from sqlalchemy import Column, Integer, DateTime
from app.database import Base

class SyncMeta(Base):
    __tablename__ = "sync_meta"

    id = Column(Integer, primary_key=True)
    last_sync = Column(DateTime)
