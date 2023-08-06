import json
import os
from subprocess import call

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from cdm.ftypes import allowed_types


def get_db_path():
    if os.getenv("CDM_PATH", None):
        dir = os.getenv("CDM_PATH")
    else:
        dir = os.path.expanduser('~/.cdm')
    if not os.path.exists(dir):
        call(['mkdir', '-p', dir])
    return os.path.join(dir, 'db')


def remove_empty(x):
    return filter(lambda a: a != '', x)


def get_extention(x):
    if not x:
        return None
    if x[-1] == '.':
        return None
    lis = x.split('.')
    return lis[-1].upper()


def validate_url(url, all=False):
    if not urlparse(url).hostname:
        return False
    if not all:
        return get_extention(urlparse(url).path) in allowed_types
    return True


def read_queue(db):
    db.setdefault('queue', [])
    return db['queue']


def read_db():
    if not os.path.exists(get_db_path()):
        return {}
    with open(get_db_path(), 'r') as file:
        db = json.load(file)
    return db

def write_db(db):
    with open(get_db_path(), 'w') as file:
        json.dump(db, file)


def write_queue(db, queue):
    db['queue'] = queue
    write_db(db)


def add_to_queue(url):
    print((url if isinstance(url, str) else url['url']) + " added to queue")
    db = read_db()
    queue = read_queue(db)
    if url not in queue:
        queue.append(url)
    write_queue(db, queue)


def shift_queue():
    print("queue shifted")
    db = read_db()
    queue = read_queue(db)
    if len(queue) > 0:
        element = queue.pop(0)
        queue.append(element)
    write_queue(db, queue)


def pop_queue():
    print("queue popped")
    db = read_db()
    queue = read_queue(db)
    if len(queue) > 0:
        queue.pop(0)
    write_queue(db, queue)


def parse_urls(db, text, all):
    inv = "\'\""
    l = text.split()
    for c in inv:
        cpy = []
        for a in l:
            cpy += a.split(c)
        l = cpy
    l = remove_empty(l)
    for s in l:
        if validate_url(s, all):
            add_to_queue(s)


def file_name_index(name, idx):
    if idx == 0:
        return name
    if name[-1] == '.':
        return name + "({})".format(idx)
    lis = name.split('.')
    ext = lis[-1].lower()
    return ext[:len(name) - len(ext) - 1] + "({}).".format(idx) + ext


def get_file_name(url):
    name = url[url.find('/') + 1]
    for c in "`~!@#$%^&*()+=[]{}\\|<>,/?":
        name = name.replace(c, '')
    name = name.replace('_', '-')
    return file_name_index(name, 0)

