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
    now = datetime.datetime.now()
    words = Word.objects.all().order_by('-occurrence')
    after = datetime.datetime.now()

    diff = (after - now).total_seconds() * 1000

    print(diff)

    rnow = datetime.datetime.now()
    words_redis = redis_server.zrange(name='myzset', start=0, end=-1, withscores=True)
    rafter = datetime.datetime.now()

    diff2 = (rafter - rnow).total_seconds() * 1000

    print(diff2)

    top_words = {
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

    return HttpResponse(json.dumps(top_words), content_type='application/json')

