from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import pyodbc
import urllib.parse
from sqlalchemy import inspect
import logging

# Log all tables in the database
logger = logging.getLogger("db_logger")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Load environment variables
load_dotenv('.env.local')


# DB connection settings
DB_USER = "sql_user"
DB_PASSWORD = urllib.parse.quote_plus("test@143")  # encodes @ to %40
DB_SERVER = r"MaheshBirajdar\SQLEXPRESS"           # use raw string for backslash
DB_NAME = "fastapi_dB"
DB_DRIVER = "ODBC Driver 17 for SQL Server"

# SQLite for simplicity, you can switch to PostgreSQL/MySQL
DATABASE_URL = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
    f"?driver={DB_DRIVER}&TrustServerCertificate=yes"
)
logger.info(f"---> Database URL: {DATABASE_URL}")

# Create the database engine
engine = create_engine(DATABASE_URL)


inspector = inspect(engine)
tables = inspector.get_table_names()
logger.info(f"---> Tables in the database: {tables}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auto-create tables
def create_tables():
    Base.metadata.create_all(bind=engine)