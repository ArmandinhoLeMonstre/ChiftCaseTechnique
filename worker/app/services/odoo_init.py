from app.services.odoo_client import OdooClient
import os

def get_odoo_client():
    url = os.getenv("ODOO_URL", default=None)
    db = os.getenv("ODOO_DATABASE", default=None)
    username = os.getenv("ODOO_USERNAME", default=None)
    password = os.getenv("ODOO_API_KEY", default=None)

    if not all([url, db, username, password]):
        raise RuntimeError("Missing Odoo environment variables")

    odoo = OdooClient(url, db, username, password)

    return (odoo)