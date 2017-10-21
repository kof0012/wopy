import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0'}


def get_one_page(url):
    try:
        rs = requests.get(url, headers=headers)
        if rs.status_code == 200:
            return (rs.text, rs.url)
        else:
            print('no,200')
            return None
    except RequestException:
        raise RequestException
        return None


def parse_item(html):
    pattern = re.compile(
        r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name.*?title="(\w+).*?star">(.*?)</p>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for i, u, n, s in items:
        yield{'index': i, 'img': u, 'name': re.sub(r'[\r\n\t主演： ]', '', s)}


def write_to_json(content):
    with open('maoyan.fuck', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html, baseurl = get_one_page(url)
    print(baseurl)

    for content in parse_item(html):
        write_to_json(content)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
