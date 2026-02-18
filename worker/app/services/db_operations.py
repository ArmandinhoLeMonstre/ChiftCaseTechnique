from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update, delete, literal_column
from app.db.db import Session
from app.db.models import Partner, SyncState

def get_last_sync():
    with Session() as session:
        stmt = select(SyncState.write_date).where(SyncState.model == "res.partner")
        last_sync = session.execute(stmt).scalar_one_or_none()

        return (last_sync)

def update_last_sync(write_date):
    with Session() as session:
        stmt = select(SyncState).where(SyncState.model == "res.partner")
        sync_state = session.execute(stmt).scalar_one_or_none()
        sync_state.write_date = write_date
        try:
            session.add(sync_state)
            session.commit()
        except Exception as e:
            session.rollback()
            raise

def upsert_partner(records):
    with Session() as session:

        stmt = insert(Partner).values(records)

        stmt = stmt.on_conflict_do_update(
            index_elements=[Partner.odoo_id],
            set_={
                "name": stmt.excluded.name,
                "email": stmt.excluded.email,
                "website": stmt.excluded.website,
                "write_date": stmt.excluded.write_date,
                "active": stmt.excluded.active,
            }
        )
        stmt = stmt.returning(literal_column("xmax"))

        try:
            result = session.execute(stmt)
            rows = result.fetchall()
            session.commit()
            return rows
        except Exception:
            session.rollback()
            raise

def update_reconciliation_to_false():
    with Session() as session:
        stmt = (
            update(Partner).values(reconciliation_flag=False)
        )
        session.execute(stmt)
        session.commit()

def update_reconciliation_to_true(odoo_ids):
    with Session() as session:
        stmt = (
            update(Partner)
            .where(Partner.odoo_id.in_(odoo_ids))
            .values(reconciliation_flag=True)
        )
        session.execute(stmt)
        session.commit()

def delete_partners():
    with Session() as session:
        stmt = delete(Partner).where(Partner.reconciliation_flag==False)
        result = session.execute(stmt)
        deleted = result.rowcount or 0
        session.commit()

        return (deleted)