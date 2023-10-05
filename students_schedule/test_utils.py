import os
import random
import string

import requests


def random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


def random_number(length=7):
    return ''.join(random.choice(string.digits) for i in range(length))


words = None


def random_words(words_count=1):
    global words
    if words:
        return '_'.join((random.choice(words) for i in range(words_count)))
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    file_name = "test_words.txt"
    response = requests.get(word_site)
    words = response.content.splitlines()
    if not os.path.isfile(file_name):
        with open(file_name, 'w') as f:
            for word in words:
                f.write(word.decode("utf-8") + '\n')
    with open(file_name, 'r') as f:
        words = f.readlines()
        # remove '\n' from the end of each word
        words = [word[:-1] for word in words]
        return '_'.join((random.choice(words) for i in range(words_count)))
