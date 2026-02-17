# Odoo Contacts Sync

Odoo Contacts Sync is a Python-based synchronization system that fetches
contacts from Odoo, stores them in PostgreSQL, and exposes them through
a FastAPI REST API. It includes an incremental sync strategy, a daily
reconciliation process, and cron-based automation.

## Installation

Rename the environment file:

mv .env.exemple .env

Update the `.env` file with your configuration:

DATABASE_URL=postgresql+psycopg://user:password@db:5432/database

ODOO_URL=https://your-odoo-instance.com 
ODOO_DB=your_db
ODOO_USERNAME=your_user 
ODOO_PASSWORD=your_password

Rename the bootstrap script:

mv bootstrap_exemple.sh bootstrap.sh

Make sure the values inside `bootstrap.sh` match those in `.env`.

Run the project with Docker:

docker compose up --build

## Usage

### Migrations

Alembic is used for schema management.

On startup:

-   Database container starts
-   Migration container runs alembic upgrade head
-   Default seed data is inserted if required


### API

Fetch paginated contacts ordered by `id ASC`:

GET /contacts?limit=50&offset=0

Fetch a single contact by id:

GET /contacts/12

Returns:

-   200 → Contact data
-   404 → Not found

### Worker

The worker contains two jobs.

Incremental job:

-   Fetches updated contacts from Odoo using search_read
-   Uses active_test=False to include archived contacts
-   Performs upsert (insert or update)
-   Stores latest write_date
-   Does not delete records
-   Runs every X minutes

Reconciliation job:

-   Fetches all contact IDs from Odoo
-   Flags existing IDs in database
-   Deletes records not present in Odoo
-   Runs once per day

### Cron

Example cron configuration:

SHELL=/bin/bash

*/5 * \* \* \* cd /code && source bootstrap.sh && bash scripts/run_incremental.sh \>\> /var/log/cron.log 2\>&1 
0 23 \* \* \* cd /code && source bootstrap.sh && bash scripts/run_reconciliation.sh \>\> /var/log/cron.log 2\>&1

Logs are written to:

/var/log/cron.log

The log file is mounted as a Docker volume and accessible from the host.
