from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidElementStateException
import re,json
from scrapy.selector import Selector 

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)


def search():
    try:
        browser.get("https://www.taobao.com")

        in_put = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        in_put.send_keys('女超紧身裤性感')
        submit.click()
        total = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text

    except InvalidElementStateException:
        print('不知道咋了')
        return search()

def next_page(numbers):
    try:
        in_put = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        in_put.clear()
        in_put.send_keys(numbers)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(numbers)))
        get_products()

    except InvalidElementStateException:
        print('不知道咋了')
        return next_page(numbers)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist > div > div > div:nth-child(1) > div:nth-child(35)')))
    num=len(re.findall('<div class="item J_MouserOnverReq.*?data-index="(\d+)"',browser.page_source,re.S))
    html=Selector(text=browser.page_source)
    for i in range(int(num)+1):
        title=html.xpath('//div[@data-index="%d"]//a[contains(@class,"J_ClickStat")]//text()'%i).extract()
        title=re.sub(r'[\n\t\s ]','',''.join(title))
        if title:
            img=html.xpath('//div[@data-index="%d"]//img[@class="J_ItemPic img"]/@data-src'%i).extract_first()
            price=html.xpath('//div[@data-index="%d"]//strong/text()'%i).extract_first()
            print(i,title,img,price)
            content=dict(title=title,img=img,price=price)
            write_to_json(content)
        else:
            continue

def write_to_json(content):
    with open('taobao.fuck', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main():
    total = int(re.search('(\d+)', search()).group(1))
    print(total)
    for i in range(2,total+1):
        next_page(i)

if __name__ == '__main__':
    main()
