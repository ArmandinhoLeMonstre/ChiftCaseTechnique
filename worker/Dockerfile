FROM python:3.12

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app

RUN apt update && apt install -y cron
COPY crontab /etc/cron.d/my-cron
COPY cron.log /var/log/cron.log
RUN chmod 644 /etc/cron.d/my-cron
COPY bootstrap.sh /code/bootstrap.sh
COPY ./scripts /code/scripts
RUN chmod 755 /code/scripts/run_incremental.sh
RUN chmod 755 /code/scripts/run_reconciliation.sh
RUN chmod 755 /code/bootstrap.sh

ENTRYPOINT cron -f