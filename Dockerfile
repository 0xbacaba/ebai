FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y cron

COPY ebai-cron /etc/cron.d/ebai-cron
RUN chmod 0644 /etc/cron.d/ebai-cron
RUN crontab /etc/cron.d/ebai-cron

CMD [ "cron", "-f" ]
