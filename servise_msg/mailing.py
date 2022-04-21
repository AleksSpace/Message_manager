import datetime
import os

import pytz
import requests
from dotenv import load_dotenv

from massage_manager.celery import app

from .models import Client, Mailing, Message

load_dotenv()
URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")


@app.task(bind=True, retry_backoff=True)
def send_message(self, data, client_id, mailing_id, url=URL, token=TOKEN):
    mailing = Mailing.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)
    timezone = pytz.timezone(client.timezone)
    now = datetime.datetime.now(timezone)
    if mailing.time_start <= now.time() <= mailing.time_end:
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
        try:
            requests.post(url=url + str(data['id']), headers=header, json=data)
        except requests.exceptions.RequestException as exc:
            raise self.retry(exc=exc)
        else:
            Message.objects.filter(pk=data['id']).update(status='Sent')
    else:
        time = 24 - (int(now.time().strftime('%H:%M:%S')[:2]) - int(
            mailing.time_start.strftime('%H:%M:%S')[:2])
        )
        return self.retry(countdown=60 * 60 * time)
