import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CourseSpider(CrawlSpider):
    name = "courses"
    allowed_domains = ['freetutsdownload.com']
    start_urls = ['https://freetutsdownload.com/category/udemy']
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//article[@class='jeg_post jeg_pl_md_4 format-standard']/div[@class='jeg_thumb']/a"),
             callback='parse_item', follow=True),
    )
    
    def parse_item(self, response):
        yield {
            "title": response.xpath("//h1[@class='jeg_post_title']/text()").get(),
            "description": response.xpath("(//div[@class='content-inner ']/p)[1]/text()").get()
        }
