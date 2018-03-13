import redis
import os

import django
django.setup()

from wikipedia.models import Word

redis_server = redis.Redis("localhost")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_redis_rabbit_tut.settings')

keys = redis_server.keys(pattern='celery-task-meta*')

print(len(keys))