from sqlalchemy import select
from app.models.models import Partner

def fetch_multiple_contacts(limit, offset, db):
    stmt = (
        select(
            Partner.id,
            Partner.name,
            Partner.email,
            Partner.website,
            Partner.write_date,
            Partner.active
        )
        .order_by(Partner.id.asc()).limit(limit).offset(offset)
    )

    rows = db.execute(stmt).mappings().all()

    return (rows)

def fetch_one_contact(contact_id, db):
    stmt = select(Partner).where(Partner.id == contact_id)
    res = db.execute(stmt).scalar_one_or_none()
    
    return (res)