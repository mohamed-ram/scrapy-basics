import scrapy


class QuoteAuthorSpider(scrapy.Spider):
    name = "quotes_author"
    start_urls = [
        "http://quotes.toscrape.com"
    ]
    
    def parse(self, response, **kwargs):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            text = quote.xpath("./span[@class='text']/text()").get()
            author_link = quote.xpath(".//a[contains(text(), 'about')]/@href").get()
            tags = quote.xpath(".//a[@class='tag']/text()").getall()
            
            yield response.follow(url=author_link, callback=self.parse_author, meta={
                "text": text,
                "tags": tags
            })
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


    def parse_author(self, response, **kwargs):
        quote = response.request.meta
        author_name = response.xpath("//h3[@class='author-title']/text()").get()
        author_birthday = response.xpath("//span[@class='author-born-date']/text()").get()
        author_birth_place = response.xpath("//span[@class='author-born-location']/text()").get()
        author_description = response.xpath("//div[@class='author-description']/text()").get()
        
        yield {
            "quote": quote["text"].strip(u'\u201c\u201d'),
            "tags": quote["tags"],
            "author": author_name,
            "author_birth": {
                "date": author_birthday,
                "place": author_birth_place
            },
            "about": author_description
        }