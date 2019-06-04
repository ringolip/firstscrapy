# -*- coding: utf-8 -*-
import scrapy

from ..items import FirstscrapyItem

# 类必须继承自scrapy.Spider
class RingoquotesSpider(scrapy.Spider):
    # 项目唯一名称
    name = 'ringoquotes'
    # 允许爬去的域名范围
    allowed_domains = ['quotes.toscrape.com']
    # spider启动时爬取的域名列表
    start_urls = ['http://quotes.toscrape.com/']

    # 解析start_url返回的响应
    def parse(self, response):
        quotes = response.css(".quote")
        for quote in quotes:
            item = FirstscrapyItem()
            item['text'] = quote.css(".text::text").extract_first() 
            item['author'] = quote.css(".author::text").extract_first()
            # tag列表
            item['tags'] = quote.css(".tags .tag::text").extract()
            # 生成器返回item
            yield item
        # 下一页url
        next = response.css('.next a::attr("href")').extract_first()
        # 构造绝对url
        next_url = response.urljoin(next)
        # 构造请求
        yield scrapy.Request(url=next_url, callback=self.parse)