import app.services.db_operations as db_operations

def run_incremental_job(odoo, model, fields, limit, offset, order):
    domain = []
    last_sync = db_operations.get_last_sync()

    if last_sync:
        domain = [('write_date','>=', last_sync)]

    while True:
        records = odoo.search_read(model, domain, fields, limit, offset, order)

        if not records:
            break

        write_date = db_operations.upsert_partner(records)

        offset += limit
        db_operations.update_last_sync(write_date)
    

