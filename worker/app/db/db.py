from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging
import os

db_url = os.environ["DATABASE_URL"]

engine = create_engine(
    db_url,
    pool_pre_ping=True
)

logger = logging.getLogger("odoo_worker")

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
except Exception as e:
    logger.exception("Database connection failed")
    sys.exit(1)

Session = sessionmaker(bind=engine, autoflush=False)
