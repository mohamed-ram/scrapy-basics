import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SeedcollectionSpider(CrawlSpider):
    name = "seedcollection"
    allowed_domains = ["theseedcollection.com.au"]
    
    def __init__(self, tag=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            F"https://www.theseedcollection.com.au/{tag}"
        ]
    
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class, 'wrapper-thumbnail')]"), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='pagination']/li/a/i[@class='fa fa-angle-right']/parent::a")),
    )
    
    def parse_item(self, response):
        images = response.xpath("//div[@class='thumb-image']/div/a/img")
        yield {
            "title": response.xpath("normalize-space(//h1[@aria-label='Product Name']/text())").get(),
            "price": response.xpath("normalize-space(//div[@class='productprice productpricetext']/text())").get(),
            "images": [
                response.urljoin(response.xpath("//div[@class='zoom']/img[@id='main-image']/@src").get()),
                *[response.urljoin(img.xpath("./@src").get()) for img in images]
            ],
        }