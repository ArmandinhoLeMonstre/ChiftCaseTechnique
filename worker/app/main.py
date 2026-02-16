from app.jobs.jobs_incremental import run_incremental_job
from app.services.odoo_init import get_odoo_client
from app.services.arg_parser import handle_args
import sys

def main():
    args = handle_args()

    if not args.mode:
        raise ValueError("--mode is required")

    if not args.model:
        raise ValueError("--model is required when running a sync job")

    try:
        odoo = get_odoo_client()
    except Exception as e:
        print(f'CRON Exception : {e}')
        sys.exit(1)

    if args.mode == "incremental":
        fields =  ['id', 'name', 'email', 'write_date', 'active']
        model = args.model
        limit = args.limit or 5
        offset = 0
        order = 'write_date asc'
        run_incremental_job(odoo, model, fields, limit, offset, order)
    elif args.mode == "reconciliation":
        print("not implemented yet")