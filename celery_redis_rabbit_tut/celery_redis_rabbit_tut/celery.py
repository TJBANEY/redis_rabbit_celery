from celery import Celery

app = Celery('celery_redis_rabbit_tut', broker='redis://localhost')

app.conf.beat_schedule = {
    'publication-heartbeat': {
        'task': 'celery_redis_rabbit_tut.wikipedia.tasks.inspect_page',
        'schedule': 60.0,
    }
}