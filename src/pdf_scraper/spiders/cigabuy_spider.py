import scrapy

class CigabuySpider(scrapy.Spider):
    name = "cigabuy"
    start_urls = [
        "https://www.cigabuy.com/products_all.html"
    ]
    
    def parse(self, response, **kwargs):
        for product in response.xpath("//div[@class='p_box_wrapper']"):
            title = product.xpath(".//a[@class='p_box_title']/text()").get()
            url = product.xpath(".//a[@class='p_box_title']/@href").get()
            price_box = product.xpath(".//div[@class='p_box_price cf']/text()").get()
            if price_box:
                price_before = price_box
                price_after = price_box
            else:
                price_before = product.xpath(".//span[@class='normalprice fl']/text()").get()
                price_after = product.xpath(".//span[@class='productSpecialPrice fl']/text()").get()

            yield {
                "title": title,
                "normal price": price_before,
                "sale price": price_after,
                "url": url
            }
            
            next_page = response.xpath("(//div[@class='digg'])[1]//a[@class='nextPage']/@href").get()
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)

