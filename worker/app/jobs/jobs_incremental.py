from app.services.db_operations import upsert_partner, update_last_sync, get_last_sync

def run_incremental_job(odoo, model, fields, limit, offset, order):
    domain = []
    last_sync = get_last_sync()

    if last_sync:
        domain = [('write_date','>=', last_sync)]

    while True:
        records = odoo.search_read(model, domain, fields, limit, offset, order)

        if not records:
            break

        write_date = upsert_partner(records)

        offset += limit
        update_last_sync(write_date)
    

