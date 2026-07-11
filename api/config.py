import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DUCKDB_PATH = BASE_DIR / "data" / "ylff.duckdb"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DUCKDB_PATH = os.getenv("DUCKDB_PATH", str(DEFAULT_DUCKDB_PATH))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"duckdb:///{DUCKDB_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
