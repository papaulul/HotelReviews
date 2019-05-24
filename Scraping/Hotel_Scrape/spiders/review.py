import scrapy
from selenium import webdriver
import time
from Hotel_Scrape.items import StackItem
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
# Main Class
class ReviewSpider(scrapy.Spider):
    name = 'review'
    allowed_domains=["tripadvisor.com"]
    start_urls =['https://www.tripadvisor.com/Hotels-g60898-Atlanta_Georgia-Hotels.html' ]
    count = 0
    def parse(self,response):
        """
        This main parse will go through the webpage with all hotels within
        """
        # Collecting all of the links for the spider to enter and extract reviews
        href = response.xpath('//a[@data-clicksource="HotelName"]/@href').extract()
        for hot in href:
            # For each hotel on the page, it will go onto the title link
            yield scrapy.Request(response.urljoin(hot), self.parse_page)
        # This is making sure that we don't go too far with our scrape
        # Recursively calls upon parse to click on the next button on the bottomabs
        # of the page
        
        try: 
            yield response.follow(response.xpath('//link[@rel="next"]/@href').extract_first(),self.parse)
        except: 
            print("No Page?")
        print(self.count)
        
    def parse_page(self, response):
        reviews = response.xpath('//a[contains(@class,"ReviewTitle__reviewTitle")]/@href').extract()
        for review in reviews:
            try:
                yield scrapy.Request(response.urljoin(review), self.parse_review)
            except:
                print("No Reviews?")
        
        try: 
            yield response.follow(response.xpath('//a[contains(@class,"nav next")]/@href').extract_first(),self.parse_page)
        except: 
            print("No Page?")
        
    def parse_review(self, response):
        print("Parsing Review: \n")
        text = response.xpath('//p/span/text()').extract()
        bubbles = str(response.xpath('//span[contains(@class,"bubble_rating")]/@class').extract_first())
        hotel= response.xpath('//a[@class="ui_header h2"]/text()').extract()
        type_label = str(response.xpath('//div[@class="recommend-titleInline noRatings"]/text()').extract_first())
        item = StackItem()
        item['review'] = text
        item['hotel_name'] = hotel
        item['travel_type'] = type_label
        item['bubble'] = bubbles
        item['url'] = response.request.url
        yield item
        print(item)
        self.count+=1
