# from celery_redis_rabbit_tut.celery import app
from celery import Celery
import time

from wikipedia.models import WikipediaPage

app = Celery('tasks', broker='redis://localhost')

app.conf.beat_schedule = {
    'publication-heartbeat': {
        'task': 'inspect_page',
        'schedule': 60.0,
    }
}

@app.task()
def inspect_page():
    # Grabs all wiki pages that haven't been scanned by Beautiful Soup
    pages = WikipediaPage.objects.filter(scanned=False)

    print('This Works')

count = 1
while count < 10:
    inspect_page.delay()
    time.sleep(2)
    count += 1