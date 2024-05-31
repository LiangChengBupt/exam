import scrapy
from bs4 import BeautifulSoup
import json
from ..items import UrlContentItem

class BaiduContentSpider(scrapy.Spider):
    name = "baidu_content"

    def __init__(self, input_file='data/medic3.json', *args, **kwargs):
        super(BaiduContentSpider, self).__init__(*args, **kwargs)
        self.input_file = input_file

    def start_requests(self):
        with open(self.input_file, 'r', encoding='utf-8') as f:
            search_results = json.load(f)
            for result in search_results:
                title = result['title']
                link = result['link']
                yield scrapy.Request(url=link, callback=self.parse_url_content, meta={'title': title, 'link': link})

    def parse_url_content(self, response):
        title = response.meta['title']
        link = response.meta['link']

        content = response.text
        soup = BeautifulSoup(content, "html.parser")

        # 过滤掉 <script> 和 <style> 标签
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()  # 删除这些标签及其内容

        # 提取纯文本内容
        text = soup.get_text(separator="\n").replace('\n','')
        
        # 清理多余的空白符
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # 创建并返回一个包含所有信息的Item
        item = UrlContentItem()
        item['title'] = title
        item['link'] = link
        item['content'] = text
        
        yield item
