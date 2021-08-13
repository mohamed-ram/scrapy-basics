import scrapy

class CigabuySearchSpider(scrapy.Spider):
    name = "cigabuy_search"
    
    def __init__(self, keyword=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            F"https://www.cigabuy.com/index.php?main_page=ws_search_result&keyword={keyword}&categories_id=&cat_change=true"
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