import app.services.db_operations as db_operations

def convert_id_to_odoo_id(records):
    for record in records:
        if "id" in record:
            record["odoo_id"] = record.pop("id")
    
    return(records)

def run_incremental_job(odoo, model, fields, limit, offset, order):
    domain = []
    last_sync = db_operations.get_last_sync()

    if last_sync:
        domain = [('write_date','>=', last_sync)]

    while True:
        records = odoo.search_read(model, domain, fields, limit, offset, order)

        if not records:
            break
        records_converted = convert_id_to_odoo_id(records)

        write_date = db_operations.upsert_partner(records_converted)

        offset += limit
        db_operations.update_last_sync(write_date)
    

