import scrapy

class AuthorSpider(scrapy.Spider):
    name = "authors"
    start_urls = [
        "http://quotes.toscrape.com/"
    ]
    
    def parse(self, response, **kwargs):
        author_links = response.css("small.author + a")
        yield from response.follow_all(author_links, callback=self.parse_author)
        
        pagination_links = response.css("li.next a")
        yield from response.follow_all(pagination_links, self.parse)
        
    def parse_author(self, response, **kwargs):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }

