# from celery_redis_rabbit_tut.celery import app
from celery import Celery
import time
import bs4

from wikipedia.models import WikipediaPage

app = Celery('tasks', broker='redis://localhost')

app.conf.beat_schedule = {
    'publication-heartbeat': {
        'task': 'inspect_page',
        'schedule': 60.0,
    }
}

@app.task()
def grab_idle_pages():
    # Grabs Idle Pages, and throw them in Queue to be scanned
    pages = WikipediaPage.objects.filter(scanned='I')

    print('This Works')

def scan_page(idle_pages):
    for page in idle_pages:
        pass


count = 1
while count < 10:
    grab_idle_pages.delay()
    time.sleep(2)
    count += 1