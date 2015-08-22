import sys
from datetime import datetime

import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from urlparse import urlparse
from bs4 import BeautifulSoup

DB_NAME = 'web_crawler'
DB_URL = ('mongodb://%s/%s' % ('localhost', DB_NAME))
NUMBER_LINKS_VISITED = 0


def connect_db():
    try:
        return MongoClient(DB_URL)
    except ConnectionFailure:
        raise ConnectionFailure


def valid_url(url):
    return bool(urlparse(url)[0] and urlparse(url)[1])


def get_html_doc(url):
    response = requests.get(url)
    return response.content


def find_links(url):
    soup = BeautifulSoup(get_html_doc(url), 'html.parser')
    return [{'url': link.get('href')} for link in soup.find_all('a')]


def store_website_cache(db, url):
    try:
        visits = db.websitecache.find_one({'url': url}).get('visits')
    except AttributeError:
        visits = 0

    db.websitecache.update({
        'url': url
    }, {
        '$set': {
            'doc': get_html_doc(url),
            'url': url,
            'visits': visits + 1,
            'last_visit': datetime.now()
        }
    }, upsert=True)


def crawl(db, url, depth=0, max_depth=2):
    global NUMBER_LINKS_VISITED
    import pdb; pdb.set_trace()
    try:
        if valid_url(url):
            store_website_cache(db, url)
            NUMBER_LINKS_VISITED += 1
            print url

            if depth == max_depth:
                return

            links_discovered = find_links(url)

            for frontier in links_discovered:
                crawl(db, frontier['url'], depth+1, max_depth)
    except Exception:
        return


def run(seed_url, max_depth=2):
    client = connect_db()
    db = client[DB_NAME]

    crawl(db, seed_url, max_depth=max_depth)

    print '\n====================================================================='
    print 'Number of sites crawled: %d' % NUMBER_LINKS_VISITED


if __name__ == '__main__':
    seed_url = sys.argv[1]

    max_depth = None
    try:
        max_depth = int(sys.argv[2])
    except IndexError:
        pass

    if valid_url(seed_url):
        if max_depth:
            run(seed_url, max_depth)
        else:
            run(seed_url)

    print 'Bye!'
