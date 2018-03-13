import redis
import os

import django
django.setup()

from wikipedia.models import Word

redis_server = redis.Redis("localhost")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_redis_rabbit_tut.settings')

for word in Word.objects.all().order_by('-occurrence'):

    # Since 'name' is a reserved parameter name
    if word.name == 'name':
        word.name = '.name'

    kw = {
        word.name: word.occurrence,
    }

    try:
        redis_server.zadd(name='myzset', **kw)
    except Exception:
        print(word.name)

print(redis_server.zrange(name='myzset', start=0, end=-1, withscores=True))