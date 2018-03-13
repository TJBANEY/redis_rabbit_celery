import json
import redis
import datetime

from django.http import HttpResponse
from django.shortcuts import render

from wikipedia.models import Word

redis_server = redis.Redis("localhost")

def home(request):
    template = 'home.html'

    return render(request, template, {})

def get_word_results(request):
    import datetime
    # Using Redis to get the top ten most common words into JSON for javascript to consume on the frontend
    # Is more than 3000% faster than querying from Postgres  "142 milliseconds => 3 milliseconds"

    now = datetime.datetime.now()

    words = Word.objects.all().order_by('-occurrence')

    top_words_one = {
        'one': words[0].to_json(),
        'two': words[1].to_json(),
        'three': words[2].to_json(),
        'four': words[3].to_json(),
        'five': words[4].to_json(),
        'six': words[5].to_json(),
        'seven': words[6].to_json(),
        'eight': words[7].to_json(),
        'nine': words[8].to_json(),
        'ten': words[9].to_json(),
    }

    after = datetime.datetime.now()

    diff1 = (after - now).total_seconds() * 1000
    print(f'diff1 {diff1}')


    # =======================

    rnow = datetime.datetime.now()

    words_redis = redis_server.zrange(name='myzset', start=-10, end=-1, withscores=True)
    words_redis.reverse()

    total = 0
    for word in words_redis:
        total += int(word[1])

    top_words = {
        'one': {
            'name': words_redis[0][0].decode("utf-8"),
            'count': words_redis[0][1],
            'percent': "{0:.1f}".format(((words_redis[0][1] / total) * 100) * 3)
        },
        'two': {
            'name': words_redis[1][0].decode("utf-8"),
            'count': words_redis[1][1],
            'percent': "{0:.1f}".format(((words_redis[1][1] / total) * 100) * 3)
        },
        'three': {
            'name': words_redis[2][0].decode("utf-8"),
            'count': words_redis[2][1],
            'percent': "{0:.1f}".format(((words_redis[2][1] / total) * 100) * 3)
        },
        'four': {
            'name': words_redis[3][0].decode("utf-8"),
            'count': words_redis[3][1],
            'percent': "{0:.1f}".format(((words_redis[3][1] / total) * 100) * 3)
        },
        'five': {
            'name': words_redis[4][0].decode("utf-8"),
            'count': words_redis[4][1],
            'percent': "{0:.1f}".format(((words_redis[4][1] / total) * 100) * 3)
        },
        'six': {
            'name': words_redis[5][0].decode("utf-8"),
            'count': words_redis[5][1],
            'percent': "{0:.1f}".format(((words_redis[5][1] / total) * 100) * 3)
        },
        'seven': {
            'name': words_redis[6][0].decode("utf-8"),
            'count': words_redis[6][1],
            'percent': "{0:.1f}".format(((words_redis[6][1] / total) * 100) * 3)
        },
        'eight': {
            'name': words_redis[7][0].decode("utf-8"),
            'count': str(words_redis[7][1]),
            'percent': "{0:.1f}".format(((words_redis[7][1] / total) * 100) * 3)
        },
        'nine': {
            'name': words_redis[8][0].decode("utf-8"),
            'count': str(words_redis[8][1]),
            'percent': "{0:.1f}".format(((words_redis[8][1] / total) * 100) * 3)
        },
        'ten': {
            'name': words_redis[9][0].decode("utf-8"),
            'count': str(words_redis[9][1]),
            'percent': "{0:.1f}".format(((words_redis[9][1] / total) * 100) * 3)
        },
    }

    rlater = datetime.datetime.now()
    diff = (rlater - rnow).total_seconds() * 1000

    print(diff)

    return HttpResponse(json.dumps(top_words), content_type='application/json')

