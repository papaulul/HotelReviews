import scrapy
from selenium import webdriver
import time
from Hotel_Scrape.items import hotelItem
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
class hotel_info(scrapy.Spider):
    name = 'hotel'
    allowed_domains=["tripadvisor.com"]
    start_urls =['https://www.tripadvisor.com/Hotels-g60898-Atlanta_Georgia-Hotels.html' ]
    """
    def __init__(self):
        #Mac
        self.driver = webdriver.Chrome('/Users/Work/Dropbox/Misc/chromedriver')

        #Windows
        #self.driver = webdriver.Chrome('C:\\Users\\Paul\\Desktop\\chromedriver')
    """
    def parse(self, response):
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

    def parse_page(self, response):
        out = hotelItem()
        hotel_name = response.xpath('//h1[@id="HEADING"]/text()').extract()
        hotel_url = response.url
        rating = response.xpath('//div[@class="prw_rup prw_common_bubble_rating rating"]/span/@alt').extract_first()
        num_amenities = len(response.xpath('//div[contains(@class,"2tkPV")]').extract())
        amenities = response.xpath('//span[contains(@class,"2IUMR")]/text()').extract()
        if 'PRICE RANGE' in response.xpath('//div[contains(@class, "2QuyD")]/text()').extract():
            price_range = response.xpath('//div[contains(@class, "iVts5")]/text()').extract()[0:3]
        else:
            price_range = ["NAN"]
        if 'NUMBER OF ROOMS' in response.xpath('//div[contains(@class, "2QuyD")]/text()').extract():
            num_rooms = response.xpath('//div[contains(@class, "iVts5")]/text()').extract()[-1]
        else:
            num_rooms = ["NAN"]
        
        out['hotelname'] = hotel_name
        out['hotel_rating'] = rating
        out['url'] = hotel_url
        out['num_amenities'] = num_amenities
        out['amenities'] = amenities
        out['price_range'] =price_range
        out['num_rooms'] = num_rooms
        yield out