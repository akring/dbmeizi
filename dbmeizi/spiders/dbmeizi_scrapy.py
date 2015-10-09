from scrapy import Spider
from scrapy.selector import Selector
from dbmeizi.items import MeiziItem
import os
import urllib


class dbmeiziSpider(Spider):
    name = "dbmeiziSpider"
    allowed_domin = ["akringblog.com"]
    start_urls = [
        # "http://www.akringblog.com",
        # "http://akringblog.com/2015/06/03/iOS8-Today-Extension%E5%BC%80%E5%8F%91%E6%94%BB%E7%95%A5%EF%BC%88%E4%B8%80%EF%BC%89/"
        "http://ui4app.com/"
    ]

    def parse(self, response):

        itemBlock = Selector(response).xpath('//div[@class="uiimg"]')

        for image in itemBlock.xpath('//img'):
            # self.writeToDisk(image)
            item = MeiziItem()
            item['title'] = image.xpath('@alt').extract()
            item['dataid'] = image.xpath('@data-id').extract()
            item['datasrc'] = image.xpath('@src').extract()
            item['startcount'] = 0
            yield item
        """
        liResults = Selector(response).xpath('//div[@class="post-body"]')
        for li in liResults:
            for img in li.xpath('.//img'):
                item = MeiziItem()
                item['title'] = img.xpath('@alt').extract()
                item['dataid'] = img.xpath('@data-id').extract()
                item['datasrc'] = img.xpath('@src').extract()
                item['startcount'] = 0
                yield item
        """
