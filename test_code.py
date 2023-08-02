from mimetypes import guess_extension
from urllib.parse import urlparse
from os.path import splitext
import requests
import pathlib
import pickle
# https://platform.virdocs.com/rscontent/epub/2321706/2486865/OEBPS/xhtml/page-1.xhtml

# 6-digit ID from book URL (/api/v1/book/<BOOK_ID>)
BOOK_ID = REDACTED
# Cookies from request header
COOKIES = 'csrftoken=REDACTED; session_id=REDACTED'

ENDPOINT = 'https://platform.virdocs.com'
HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cookie': COOKIES,
    'Referer': f'https://platform.virdocs.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'X-NewRelic-ID': 'REDACTED',
    'X-Requested-With': 'XMLHttpRequest'
}

def download_and_save(url, path):
    r = requests.get(url)

    if not r.ok:
        raise Exception('Failed to download resource')
    
    #ext = guess_extension(r.headers['Content-Type'].split()[0].rstrip(";"))
    ext = splitext(urlparse(url).path)[1]
    
    with path.with_suffix(ext).open('wb') as f:
        f.write(r.content)

r = requests.get(f'{ENDPOINT}/api/v1/book/{BOOK_ID}/', headers=HEADERS)

if not r.ok:
    raise Exception('Failed to get book')

j = r.json()

title = j['title'].lower().replace(' ', '-')
book_path = pathlib.Path(f'book-{BOOK_ID}-{title}')
book_path.mkdir(parents=True, exist_ok=True)

pickle.dump(j, (book_path / 'book.pickle').open('wb'))

cover_url = j['cover_image']
download_and_save(cover_url, book_path / 'cover')

page_paths = j['pages']

page_data = {}

for i, page_path in enumerate(page_paths):
    print(i)
    
    r = requests.get(ENDPOINT + page_path, headers=HEADERS)

    if not r.ok:
        print(f'Stopped with status code {r.status_code}: {r.text}')
        break
    
    j = r.json()
    page_data[i] = j

    num, label = j['page_number'], j['page_label'].lower().replace(' ', '-')

    for resource in ['image', 'svg_image']:
        if resource in j and j[resource]:
            download_and_save(j[resource], book_path / f'page-{num}-{label}')
    
pickle.dump(page_data, (book_path / 'pages.pickle').open('wb'))