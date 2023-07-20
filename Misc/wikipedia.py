import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from SENIOR_PROJECT.items import SeniorProjectItem



class WikipediaSpider(CrawlSpider):
    name = "wikipedia"
    allowed_domains = ['en.wikipedia.org']
    handle_httpstatus_list =[404]
    start_urls = ['https://en.wikipedia.org/wiki/keke_palmer']

    rules= [Rule(LinkExtractor(allow=r'wiki/((?!:).)*'), callback= 'parse_info', follow =True)]
    def parse_info(self, response):
        if response.status == 404:
            self.logger.info("Page not found: %s", response.url)
        else:
            return{
                'title': response.xpath('//h1/text()').get() or response.xpath('//h1/i/text()').get(),
                'url': response.url,
                'last_edited': response.xpath('//li[@id="footer-info-lastmod"]/text()').get()
              
        }