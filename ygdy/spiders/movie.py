# -*- coding: utf-8 -*-
import scrapy
from ygdy.items import YgdyItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['www.ygdy8.net']
    start_urls = ['http://www.ygdy8.net/html/gndy/dyzz/index.html']

    def parse(self, response):
        table_list = response.xpath('//table[@class="tbspan"]')
        for table in table_list:
            title = table.xpath('.//a[1]/text()').extract_first().strip()
            brief = table.xpath('.//tr[last()]/td/text()').extract_first().strip()
            link = "http://www.ygdy8.net" + table.xpath('.//a[1]/@href').extract_first()

            # 创建item对象
            item = YgdyItem()
            item['title'] = title
            item['brief'] = brief
            # 发起一个scrapy request请求.去访问link
            yield scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})

        # 爬其他页数据
        for i in range(2, 7):
            url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_%s.html' % i
            yield scrapy.Request(url=url, callback=self.parse)


    def parse_detail(self, response):
        # 取item
        item = response.meta['item']
        # 继续取item剩下的东西
        poster = response.xpath('//div[@id="Zoom"]//img[1]/@src').extract_first()
        download_url = response.xpath('//div[@id="Zoom"]//table//a/text()').extract_first()
        item['poster'] = poster
        item['download_url'] = download_url
        yield item


