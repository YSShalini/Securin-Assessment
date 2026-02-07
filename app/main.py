from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.cves import router as cve_router
from app.services.scheduler import start_scheduler

app = FastAPI(
    title="NVD CVE API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cve_router)

@app.get("/")
def health_check():
    return {"status": "OK"}


@app.on_event("startup")
def startup_event():
    start_scheduler()


