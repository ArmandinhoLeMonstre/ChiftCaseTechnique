from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

db_url = os.environ["DATABASE_URL"]

engine = create_engine(
    db_url,
    pool_pre_ping=True
)

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
except Exception as e:
    raise RuntimeError(f"Database connection failed: {e}")

Session = sessionmaker(bind=engine, autoflush=False)
