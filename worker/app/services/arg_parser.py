import argparse

def limit_type(value):
    try:
        v = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Limit must be an integer")

    MIN = 1
    MAX = 500

    if v < MIN or v > MAX:
        raise argparse.ArgumentTypeError(f"Limit must be between {MIN} and {MAX}")
    
    return v


def handle_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        help="Odoo synchronization service. Runs either as an incremental or reconciliation cron job.",
        choices=["incremental", "reconciliation"],
    )

    parser.add_argument(
        "--model",
        help="Choose which model you would like to synchronise",
        choices=["res.partner"],
    )

    parser.add_argument(
        "--limit",
        type=limit_type,
        default=5,
        help="Pagination limit (between 1 and 500)"
    )

    args = parser.parse_args()

    return (args)
