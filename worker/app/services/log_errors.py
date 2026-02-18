import logging
import app.services.db_operations as db_operations

def log_upsert_error(e):
    logger = logging.getLogger("odoo_worker")
    last_sync = db_operations.get_last_sync()
    logger.error(
        "Upsert failed. Next sync will start from last successful sync: %s",
        last_sync,
    )

def log_sync_error(e):
    logger = logging.getLogger("odoo_worker")
    last_sync = db_operations.get_last_sync()

    logger.error(
        "Failed to save last sync to database. Last valid sync: %s",
        last_sync,
    )