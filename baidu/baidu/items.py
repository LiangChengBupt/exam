import scrapy

class BaiduSpiderItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()

class UrlContentItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()