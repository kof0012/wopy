import requests
from requests.exceptions import RequestException
import re
import json
from hashlib import md5
import os

headers = headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'}


def get_page_index(offset, keyword):
    # payload={'offset':offset,'format':'json',
    # 'keyword':keyword,'autoload':'true','count':20,
    # 'cur_tab':1
    # }
    payload = dict(offset=offset, format='json', keyword=keyword,
                   autoload='true', count=20, cur_tab=3)
    try:
        rs = requests.get('http://www.toutiao.com/search_content/?',
                          params=payload, headers=headers).json()
        if 'data' in rs.keys():
            print('YES')
            return rs
        else:
            return None
    except RequestException:
        print('初始页面请求不成功')
        return None


def parse_page_index(response):
    detail_urls = (i.get('article_url', None) for i in response.get('data'))
    print(next(detail_urls))
    return detail_urls


def get_page_deatail(url):
    try:
        rs = requests.get(url, headers=headers)
        if rs.status_code == 200:
            return rs.text
        else:
            return None
    except RequestException:
        print('详情页面请求不成功')
        return None


def parse_page_detail(html, url):
    title = re.search(r'<title>(.*?)</title>', html, re.S).group(1)
    images_urls = re.findall(r'{"url":"(.*?)"', html, re.S)
    images_urls = (i.replace("\\", "")
                   for i in images_urls if "p3" in i and len(i) < 100)
    for single_image_url in images_urls:
        download_image(single_image_url)
    return {'title': title, 'url': url, 'images': images_urls}


def download_image(single_image_url):
    print('正在下载',single_image_url)
    try:
        rs = requests.get(single_image_url, headers=headers)
        if rs.status_code == 200:
            save_image(rs.content,single_image_url)
    
    except RequestException:
        print('图片未打开')
        return None


def save_image(content,single_image_url):
    file_name='%s/%s.jpg'%(os.getcwd(),md5(single_image_url.encode("ascii")).hexdigest())
    if not os.path.exists(file_name):
        with open(file_name,'wb') as f:
                f.write(content)



def main():
    response = get_page_index(0, '紧身')
    for url in parse_page_index(response):
        html = get_page_deatail(url)
        if html:
            result = parse_page_detail(html, url)
            print(result)

if __name__ == '__main__':
    main()
