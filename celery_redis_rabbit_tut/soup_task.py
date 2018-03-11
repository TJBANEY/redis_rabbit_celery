import random
import time

import django
django.setup()

from bs4 import BeautifulSoup
from bs4.element import Comment

import requests

from wikipedia.models import Word

forbidden_words = [
    '', 'the', 'and', 'as', 'for', 'a', 'by', '&', 'of', 'on', 'at',
    ',', '.', 'in', 'to', 'are', '', 'is', '^', '[', ']', 'from',
    'an', 'this', 'that', 'then', 'there', 'but', 'was', 'with',
    'which', ':', ';', 'also', 'were', 'has', 'its', '-', '_', 'or',
    'it', '=', '"', '\'', 'such', '–', '(', ')', ').', 'be'
]

def hit_page():
    count = 0

    while count < 20:
        print('Scanning page')

        get_fifty_most_common_words("https://en.wikipedia.org/wiki/Special:Random")

        time.sleep(3)
        count += 1


def get_fifty_most_common_words(url):
    body = requests.get(url)

    text = text_from_html(body.text)

    # Get 1000 most common words from the page.
    words_dict = get_sorted_list_of_words(text)[:1000]

    # Start saving words to database
    for item in words_dict:
        word = item[0].lower()

        count = int(item[1])

        word_obj, _ = Word.objects.get_or_create(name=word)

        word_obj.occurrence += count
        word_obj.save()

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


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

hit_page()
