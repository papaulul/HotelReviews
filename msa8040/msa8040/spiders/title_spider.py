import scrapy

class HotelSpider(scrapy.Spider):
    name = 'hotel'
    start_urls =[
'https://www.tripadvisor.com/Hotels-g60898-Atlanta_Georgia-Hotels.html'
    ]
    def parse(self,response):
        yield {
        'Hotel Name': response.xpath('//a[contains(@id,"property")]/text()').extract(),
        'Ranks': response.xpath('//div[@class="popindex"]/text()').extract(),
        #'Star': response.xpath('//div//span//@alt').extract()
        }

        for href in response.xpath('//a[contains(@id,"property")]/@href'):
            yield response.follow(href, self.parse_links)

        # href = response.xpath('//a[contains(@id,"property")]/@href').extract_first()
        # yield response.follow(href, self.parse_links)


        # next_page = response.xpath('/html/head/link[@rel="next"]/@href').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
    def parse_links(self,response):
        yield{
        'Name': response.xpath('//h1[@id="HEADING"]/text()').extract(),
        'star': response.xpath('//*[@id="taplc_resp_hr_atf_hotel_info_0"]/div/div[1]/div/a/div/span/@alt').extract_first(),
        'Ranks' : response.xpath('//b[@class ="rank"]/text()').extract(),
        'Amenities': response.xpath('//*[@id="ABOUT_TAB"]//div[@class="textitem"]/text()').extract(),
        'UnavaliableAmenities': response.xpath('//*[@id="ABOUT_TAB"]//div[@class = "textitem unavailable"]/text()').extract()
        }
