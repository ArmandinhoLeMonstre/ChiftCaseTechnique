from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from app.db.db import Session
from app.db.models import Partner, SyncState

def get_last_sync():
    with Session() as session:
        stmt = select(SyncState.write_date).where(SyncState.model == "res.partner")
        last_sync = session.execute(stmt).scalar_one_or_none()

        return (last_sync)

def set_last_sync(records):
    size = len(records)
    write_date = records[size - 1]["write_date"]

    return write_date

def update_last_sync(write_date):
    with Session() as session:
        stmt = select(SyncState).where(SyncState.model == "res.partner")
        sync_state = session.execute(stmt).scalar_one_or_none()
        sync_state.write_date = write_date
        try:
            session.add(sync_state)
            session.commit()
        except Exception as e:
            print(f'Sync state update failure: {e}')
            session.rollback()
            raise

def upsert_partner(records):
    with Session() as session:

        stmt = insert(Partner).values(records)

        stmt = stmt.on_conflict_do_update(
            index_elements=[Partner.id],
            set_={
                "name": stmt.excluded.name,
                "email": stmt.excluded.email,
                "website": stmt.excluded.website,
                "write_date": stmt.excluded.write_date,
                "active": stmt.excluded.active,
            }
        )

        try:
            session.execute(stmt)
            session.commit()
            latest_write_date = set_last_sync(records)
            return latest_write_date
        except Exception:
            session.rollback()
            raise

