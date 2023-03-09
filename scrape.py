import datetime
import json
import os
import pathlib
from urllib import request

# https://q-server.st-cdn.nzz.ch/tools/custom_code/endpoints/2484ed2804c37655aa53312284ef8f7f/getAreas?appendItemToPayload=c43940da317fdc578cf589dd9357512c&toolRuntimeConfig=%7B%22fileRequestBaseUrl%22%3A%22https%3A%2F%2Fq-server.st-cdn.nzz.ch%2Ffile%22%7D&to=2023-03-08
BASE_URL = 'https://q-server.st-cdn.nzz.ch/tools/custom_code/endpoints/2484ed2804c37655aa53312284ef8f7f/getAreas?appendItemToPayload=c43940da317fdc578cf589dd9357512c&toolRuntimeConfig=%7B%22fileRequestBaseUrl%22%3A%22https%3A%2F%2Fq-server.st-cdn.nzz.ch%2Ffile%22%7D&to='  # noqa

DATA_FOLDER = 'data'
USER_AGENT = 'nzz-scraper/0.0.1'
TIMEOUT = 60

DATE_FORMAT = '%Y-%m-%d'

start = datetime.datetime(2022, 2, 24)
end = datetime.datetime.today()
dates = [start + datetime.timedelta(days=x)
         for x in range(0, (end-start).days + 1)]
dates = [date.strftime(DATE_FORMAT) for date in dates]

def save_to_file(items, filename):
    with open(filename, 'w') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def scrape_json(url: str):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': USER_AGENT,
        'Origin': 'https://www.nzz.ch',
        'Accept-Language': 'en-US,en;q=0.7,de-DE;q=0.3',
    }
    req = request.Request(
        url=url,
        headers=headers,
        method='GET',
    )

    def fetch():
        return json.loads(
            request.urlopen(
                req,
                timeout=TIMEOUT,
            ).read().decode('utf-8')
        )

    return fetch()


# Ensure 'items' dir exists
pathlib.Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)

def scrape_items(items):

    def id_exists(id_):
        if os.path.isfile(DATA_FOLDER + '/' + id_ + '.json'):
            return True

    ids = list(filter(
        lambda x: not id_exists(x), [p for p in items]
    ))

    def scrape_content(id_):
        url = BASE_URL + id_
        entry = scrape_json(url)
        save_to_file(entry, DATA_FOLDER + '/' + id_ + '.json')
        entry['id'] = id_
        return entry

    if len(ids) == 0:
        print("No new items")
        return

    print(f"Scraping {len(ids)} new items...")

    return list(map(scrape_content, ids))

scrape_items(dates)
