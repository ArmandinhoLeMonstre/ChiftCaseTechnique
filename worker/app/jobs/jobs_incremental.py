import app.services.db_operations as db_operations
from app.services.log_data import log_upsert_rows
from app.services.log_errors import log_upsert_error, log_sync_error


def convert_id_to_odoo_id(records):
    for record in records:
        if "id" in record:
            record["odoo_id"] = record.pop("id")
    
    return(records)

def set_last_sync(records):
    size = len(records)
    write_date = records[size - 1]["write_date"]

    return write_date

def run_incremental_job(odoo, model, fields, limit, offset, order):
    domain = []
    last_sync = db_operations.get_last_sync()

    if last_sync:
        domain = [('write_date','>', last_sync)]

    rows = []

    while True:
        records = odoo.search_read(model, domain, fields, limit, offset, order)

        if not records:
            log_upsert_rows(rows)
            break

        records_converted = convert_id_to_odoo_id(records)

        try:
            rows_tmp = db_operations.upsert_partner(records_converted)
        except Exception as e:
            log_upsert_error(e)
            raise

        rows.extend(rows_tmp)

        offset += limit

        last_sync = set_last_sync(records)

        try:
            db_operations.update_last_sync(last_sync)
        except Exception as e:
            log_sync_error(e)
            raise
    

