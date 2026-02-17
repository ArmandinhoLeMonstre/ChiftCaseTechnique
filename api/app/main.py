from fastapi import FastAPI
from app.db.conn_test import db_conn_test
from contextlib import asynccontextmanager
from app.routers.contacts_router import router as contacts_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_conn_test()

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(contacts_router)