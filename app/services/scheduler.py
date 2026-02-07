# app/services/scheduler.py
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.nvd_sync import sync_cves

scheduler = BackgroundScheduler(timezone="UTC")

def run_incremental_sync():
    print(f"[{datetime.utcnow()}] Running scheduled CVE sync...")
    try:
        sync_cves(limit=None)  
    except Exception as e:
        print("Scheduler error:", e)

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            run_incremental_sync,
            trigger="cron",
            hour=2,
            minute=0,
            id="daily_cve_sync",
            replace_existing=True
        )

        scheduler.start()
        print("CVE Scheduler started (daily at 02:00 UTC)")
