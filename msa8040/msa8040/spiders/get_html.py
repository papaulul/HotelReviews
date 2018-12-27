import scrapy


class QuotesSpider(scrapy.Spider):
    name = "html"

    def start_requests(self):
        urls = [
'https://www.tripadvisor.com/Hotel_Review-g60898-d114387-Reviews-The_Westin_Peachtree_Plaza_Atlanta-Atlanta_Georgia.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'tripadvisor-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
