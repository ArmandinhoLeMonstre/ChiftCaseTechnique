from app.services.db_operations import upsert_partner, update_last_sync


def run_incremental_job(odoo, model, fields, limit, offset, order):
    while True:
        records = odoo.search_read(model, fields, limit, offset, order)

        if not records:
            break

        write_date = upsert_partner(records)

        offset += limit
    
    update_last_sync(write_date)

