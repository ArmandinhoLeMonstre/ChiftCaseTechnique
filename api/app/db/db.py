from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db_url = os.environ["DATABASE_URL"]

engine = create_engine(
    db_url,
    pool_pre_ping=True
)

Session = sessionmaker(bind=engine, autoflush=False)