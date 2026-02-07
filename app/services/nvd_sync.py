import time
import requests
from sqlalchemy.exc import SQLAlchemyError

from app.config import NVD_API_KEY
from app.database import SessionLocal
from app.models.cve import CVE

BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

HEADERS = {"apiKey": NVD_API_KEY} if NVD_API_KEY else {}

RESULTS_PER_PAGE = 50
MAX_RETRIES = 5
SLEEP_BETWEEN_CALLS = 10  


def sync_cves(limit=None):
    db = SessionLocal()
    start_index = 0
    fetched = 0
    total_results = None
    try:
        while True:
            params = {
                "startIndex": start_index,
                "resultsPerPage": RESULTS_PER_PAGE
            }
            print(f"Requesting CVEs | startIndex={start_index}")
            response = None
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    response = requests.get(
                        BASE_URL,
                        headers=HEADERS,
                        params=params,
                        timeout=(10, 60)
                    )
                    response.raise_for_status()
                    break 
                except requests.exceptions.RequestException as e:
                    wait_time = 20 * attempt
                    print(f"API error (attempt {attempt}/{MAX_RETRIES}): {e}")
                    print(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)

            if response is None:
                print("Skipping this batch after max retries")
                start_index += RESULTS_PER_PAGE
                continue

            data = response.json()

            if total_results is None:
                total_results = data.get("totalResults", 0)
                print(f"Total CVEs available: {total_results}")

            vulnerabilities = data.get("vulnerabilities", [])

            if not vulnerabilities:
                print("No more CVEs returned")
                break

            for item in vulnerabilities:
                cve = item.get("cve", {})
                cve_id = cve.get("id")
                if not cve_id:
                    continue
                if db.query(CVE).filter(CVE.cve_id == cve_id).first():
                    continue
                descriptions = cve.get("descriptions", [])
                description = descriptions[0]["value"] if descriptions else ""
                new_cve = CVE(
                    cve_id=cve_id,
                    identifier=cve_id,
                    description=description,
                    published=cve.get("published"),
                    last_modified=cve.get("lastModified"),
                    status=cve.get("vulnStatus"),
                    raw_metrics=cve.get("metrics", {}),
                    cpe=cve.get("configurations")
                )
                db.add(new_cve)
                fetched += 1

                if limit and fetched >= limit:
                    break

            db.commit()
            print(f"Stored {fetched} CVEs so far")
            start_index += RESULTS_PER_PAGE
            time.sleep(SLEEP_BETWEEN_CALLS)

            if limit and fetched >= limit:
                print("Limit reached")
                break

            if start_index >= total_results:
                print("Completed full NVD sync")
                break

    except SQLAlchemyError as db_err:
        db.rollback()
        print("Database error:", db_err)

    except Exception as e:
        db.rollback()
        print("Unexpected error:", e)
        
    finally:
        db.close()
        print(f"Sync complete. Total CVEs stored: {fetched}")
