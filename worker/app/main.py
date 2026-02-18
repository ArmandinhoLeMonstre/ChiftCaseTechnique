from app.jobs.jobs_incremental import run_incremental_job
from app.jobs.jobs_reconciliation import run_reconciliation_job
from app.services.odoo_init import get_odoo_client
from app.services.arg_parser import handle_args
import sys
import logging

def main():

    args = handle_args()

    if not args.mode:
        raise ValueError("--mode is required")

    if not args.model:
        raise ValueError("--model is required when running a sync job")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    logger = logging.getLogger("odoo_worker")
    
    try:
        odoo = get_odoo_client()
    except Exception:
        logger.exception("Odoo init problem")
        sys.exit(1)
    

    if args.mode == "incremental":
        logger.info("Starting incremental sync")
        fields =  ['id', 'name', 'email', 'website', 'write_date', 'active']
        model = args.model
        limit = args.limit or 5
        offset = 0
        order = 'write_date asc, id asc'
        run_incremental_job(odoo, model, fields, limit, offset, order)
        logger.info("Incremental sync completed")
    elif args.mode == "reconciliation":
        logger.info("Starting reconciliation sync")
        model = args.model
        limit = args.limit or 5
        offset = 0
        order = 'write_date asc, id asc'
        run_reconciliation_job(odoo, model, limit, offset, order)
        logger.info("Reconciliation sync completed")

if __name__ == "__main__":
    main()