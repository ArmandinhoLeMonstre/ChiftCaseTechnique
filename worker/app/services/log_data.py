import logging

def log_upsert_rows(rows):
    logger = logging.getLogger("odoo_worker")

    updated = 0
    inserted = 0

    for row in rows:
        if row[0] != '0':
            updated += 1
        else:
            inserted += 1

    logger.info("INSERTED : %d, UPDATED : %d", inserted, updated)

def log_deleted_rows(rows):
    logger = logging.getLogger("odoo_worker")
    logger.info("DELETED : %d", rows)