from fastapi import APIRouter, Query
from app.dependencies import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.contact_schemas import ContactsResponse
from fastapi import HTTPException
from typing import List
import app.services.retrieve_from_db as retrieve_from_db

router = APIRouter(prefix="/contacts")

@router.get("/", response_model=List[ContactsResponse])
def get_contacts(
    limit: int = Query(5, gt=0, le=100),
    offset: int = Query(0, ge=0),
    db : Session = Depends(get_db)
):
    response = retrieve_from_db.fetch_multiple_contacts(limit, offset, db)

    return (response)

@router.get("/{contact_id}", response_model=ContactsResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    res = retrieve_from_db.fetch_one_contact(contact_id, db)

    if not res:
        raise HTTPException(404, detail=f'{contact_id} not found', headers=None)

    return res