import app.services.db_operations as db_operations
from app.services.log_data import log_deleted_rows

def run_reconciliation_job(odoo, model, limit, offset, order):
    domain = []
    db_operations.update_reconciliation_to_false()

    while True:
        records = odoo.search(model, domain, limit, offset, order)

        if not records:
            break

        db_operations.update_reconciliation_to_true(records)

        offset += limit

    rows = db_operations.delete_partners()
    log_deleted_rows(rows)