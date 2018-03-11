from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

import requests
from bs4 import BeautifulSoup
from slugify import slugify

import django
django.setup()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_redis_rabbit_tut.settings')
app = Celery('tasks')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from wikipedia.models import WikipediaPage

@app.task()
def create_wiki_page():
    response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(response.text, 'html.parser')

    subject = soup.find("h1", {"id": "firstHeading"}).text
    url = f"https://en.wikipedia.org/wiki/{slugify(subject)}".replace('-', '_')

    WikipediaPage.objects.create(subject=subject, url=url)

    return 'Success'

@app.task()
def grab_idle_pages():
    pass

create_wiki_page.delay()