🛡️ NVD CVE Management System

A full-stack application to ingest, store, filter, and visualize CVE (Common Vulnerabilities and Exposures) data from the NVD (National Vulnerability Database) using the official NVD CVE API.

This project demonstrates API consumption, batch synchronization, data cleansing, backend filtering, pagination, sorting, frontend visualization, and unit testing.

📌 Features
      🔹 Backend
      
      Consume CVE data from NVD CVE API v2.0
      Chunked data ingestion using startIndex & resultsPerPage
      Data cleansing & de-duplication     
      Store CVE data in PostgreSQL    
      REST APIs built using FastAPI  
      
      Server-side:    
          Pagination      
          Sorting (published / last modified dates)      
          Filtering by:      
          CVE ID      
          CVE Year  
          CVSS Score (v2 / v3)   
          Last modified in N days
          
      Periodic batch synchronization using APScheduler      
      Auto-generated API documentation using Swagger (OpenAPI)      
      Unit tests using pytest

      🔹 Frontend
      
      Built using HTML, CSS, JavaScript   
      
      CVE List page:     
          Total record count     
          Paginated table      
          Results per page (10 / 50 / 100)      
          Sorting support      
      CVE Detail page:     
          CVE description     
          CVSS v2 metrics     
          Scores breakdown      
          CPE details in tabular format

🏗️ Tech Stack
      Layer	Technology
      Backend	FastAPI
      Database	PostgreSQL
      ORM	SQLAlchemy
      Scheduler	APScheduler
      Frontend	HTML, CSS, JavaScript
      Testing	Pytest
      API Source	NVD CVE API v2.0

⚙️ Setup & Installation
1️⃣ Clone the repository
git clone https://github.com/<your-username>/nvd-cve-ingestion.git
cd nvd-cve-ingestion

2️⃣ Create virtual environment
python -m venv myenv
source myenv/bin/activate   # Linux / Mac
myenv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file:

DATABASE_URL=postgresql://username:password@localhost:5432/cvedb
NVD_API_KEY=your_nvd_api_key_here


🔑 NVD API key can be generated at
https://nvd.nist.gov/developers/request-an-api-key

🗄️ Database Setup

Create tables:

python create_tables.py

🔄 CVE Data Synchronization
Initial Sync
python sync_cves.py


Uses chunked API calls

Respects NVD rate limits

Deduplicates CVE entries

▶️ Run Backend Server
uvicorn app.main:app --reload


Backend available at:

API: http://127.0.0.1:8000

Swagger Docs: http://127.0.0.1:8000/docs

🧪 Run Unit Tests
pytest -v

🌐 Run Frontend

From project root:

cd ui
python -m http.server 5500


Open browser:

http://localhost:5500/index.html

🔁 Scheduler (Periodic Sync)
Configured using APScheduler
Runs automatically on FastAPI startup
Supports incremental CVE updates based on last modified date

📑 API Endpoints
Method	Endpoint	Description
GET	/cves/list	List CVEs with filters
GET	/cves/{cve_id}	Get CVE details
GET	/docs	Swagger API Docs

