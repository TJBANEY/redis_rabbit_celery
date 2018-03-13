# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from slugify import slugify
import redis

import time

import django
django.setup()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_redis_rabbit_tut.settings')
app = Celery('tasks')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

redis_server = redis.Redis("localhost")

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(1.0, create_wiki_page.s(), name='add every 10')

from wikipedia.models import WikipediaPage, Word

forbidden_words = [
    '', 'the', 'and', 'as', 'for', 'a', 'by', '&', 'of', 'on', 'at',
    ',', '.', 'in', 'to', 'are', '', 'is', '^', '[', ']', 'from',
    'an', 'this', 'that', 'then', 'there', 'but', 'was', 'with',
    'which', ':', ';', 'also', 'were', 'has', 'its', '-', '_', 'or',
    'it', '=', '"', '\'', 'such', '–', '(', ')', ').', 'be', 'wikipedia', 'page',
    'edit', 'retrieved', 'articles', '[1]', 'in', 'his', 'her', 'he', 'she', 'name'
]

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# def purge_rare_words():
#     rare_words = Word.objects.filter(occurrence__lte=10)
#     rare_words.delete()

def get_sorted_list_of_words(text):
    word_count = {}
    for index, item in enumerate(text.split(' ')):

        # Ensure word is not a letter of the alphabet, or a common word like a preposition, or conjunction
        if len(list(item)) > 1 and item.lower() not in forbidden_words:

            # Ensure word is not a number
            try:
                int(item)
            except Exception:
                if not word_count.get(item):
                    word_count[item] = 1
                else:
                    word_count[item] += 1

    sorted_dict = [(item, word_count[item]) for item in sorted(word_count, key=word_count.get, reverse=True)]

    # Only return top 1000 most common words
    return sorted_dict

@app.task()
def create_wiki_page():
    response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(response.text, 'html.parser')

    subject = soup.find("h1", {"id": "firstHeading"}).text
    url = f"https://en.wikipedia.org/wiki/{slugify(subject)}".replace('-', '_')

    WikipediaPage.objects.create(subject=subject, url=url)

    content = soup.find("div", {"id": "content"})

    texts = content.findAll(text=True)

    visible_texts = filter(tag_visible, texts)
    text = u" ".join(t.strip() for t in visible_texts)

    # Get 1000 most common words from the page.
    words_dict = get_sorted_list_of_words(text)[:1000]

    # purge_rare_words()

    # Start saving words to Redis
    for item in words_dict:
        word = item[0].lower()
        for ch in ['(', '{', '}', ')', ',', '[', ']', '"', '\'', '=']:
            word = word.replace(ch, '')

        count = int(item[1])

        redis_server.zincrby(name='myzset', value=word, amount=count)

    return 'Success'

@app.task()
def grab_idle_pages():
    pass

# create_wiki_page.apply_async(countdown=60)



