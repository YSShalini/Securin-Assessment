import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
NVD_API_KEY = os.getenv("NVD_API_KEY")
