import scrapy
from urllib.parse import quote
import random
from bs4 import BeautifulSoup
from ..items import BaiduSpiderItem

class BaiduSpider(scrapy.Spider):
    name = "baidu"

    def __init__(self, query='骨折并发症', pages=20, *args, **kwargs):
        super(BaiduSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.pages = int(pages)

    def start_requests(self):
        for page in range(1, self.pages + 1):
            text = quote(self.query, "utf-8")
            url = f"https://www.baidu.com/s?wd={text}&pn={(page - 1) * 10}&inputT={random.randint(500, 4000)}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        if not soup.find("div", id="content_left"):
            return []

        result_list = []
        link_list = []

        element_list = soup.findAll('div', class_='result')
        for element in element_list:
            result_list.append(element)

        for i in range(len(result_list)):
            title = result_list[i].text.replace('\n', '')
            link = result_list[i].find('a').get('href')
            link_list.append({'title': title, 'link': link})
            
            item = BaiduSpiderItem()
            item['title'] = title
            item['link'] = link
            yield item
