import scrapy

class ReviewSpider(scrapy.Spider):
    name = 'review'
    start_urls =[
'https://www.tripadvisor.com/Hotel_Review-g60898-d114387-Reviews-The_Westin_Peachtree_Plaza_Atlanta-Atlanta_Georgia.html'
 ]
    count = 1
    def parse(self,response):
        reviews = []
        for i in response.xpath('//p[contains(@class, "partial_entry")][not(contains(text(),"Dear"))]'):
            reviews.append(i.xpath('text()').extract_first())
            reviews.append("|")
        yield {
        'Title': response.xpath('//a[contains(@class, "title")]/span/text()').extract(),
        'Review':  reviews,
        'Rating': response.xpath('//*[contains(@id,"review")]//span[contains(@class,"bubble")]/@class').extract(),
        'Date': response.xpath('//*[contains(@id,"review")]//span[contains(@class,"Date")][not(contains(text(),"Responded"))]/@title').extract(),
        }
        next_page = response.xpath('/html/head/link[@rel="next"]/@href').extract_first()
        if next_page is not None:
            yield response.follow( callback=self.parse)
