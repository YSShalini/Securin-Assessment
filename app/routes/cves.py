from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models.cve import CVE

router = APIRouter(prefix="/cves", tags=["CVEs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/list")
def list_cves(
    year: int | None = Query(None),
    score: float | None = Query(None),
    last_days: int | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sortField: str = Query("published"),
    sortOrder: str = Query("asc"),
    db: Session = Depends(get_db)
):
    """
    List CVEs with filtering, pagination and sorting
    """
    q = db.query(CVE)

    # 🔹 Filter by year
    if year:
        q = q.filter(
            CVE.published.between(
                datetime(year, 1, 1),
                datetime(year, 12, 31)
            )
        )

    # 🔹 Filter by CVSS score
    if score is not None:
        q = q.filter(
            (CVE.cvss_v2 >= score) | (CVE.cvss_v3 >= score)
        )

    # 🔹 Filter by last modified days
    if last_days:
        cutoff = datetime.utcnow() - timedelta(days=last_days)
        q = q.filter(CVE.last_modified >= cutoff)

    total = q.count()

    # 🔹 Sorting
    sort_map = {
        "published": CVE.published,
        "last_modified": CVE.last_modified,
        "cve_id": CVE.cve_id
    }

    sort_column = sort_map.get(sortField, CVE.published)

    if sortOrder.lower() == "asc":
        q = q.order_by(sort_column.asc())
    else:
        q = q.order_by(sort_column.desc())

    records = q.offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": records
    }


@router.get("/{cve_id}")
def get_cve(cve_id: str, db: Session = Depends(get_db)):
    cve = db.query(CVE).filter(CVE.cve_id == cve_id).first()

    if not cve:
        raise HTTPException(status_code=404, detail="CVE not found")

    return cve


