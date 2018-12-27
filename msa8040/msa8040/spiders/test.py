import scrapy
from selenium import webdriver
import time
from msa8040.items import StackItem
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains=["tripadvisor.com"]
    start_urls =[
'https://www.tripadvisor.com/Hotel_Review-g60898-d89380-Reviews-La_Quinta_Inn_Suites_Atlanta_Ballpark_Galleria-Atlanta_Georgia.html']
    custom_settings={
        'DEPTH_LIMIT':'3'
    }
    def __init__(self):
        self.driver = webdriver.Chrome('/Users/Work/Downloads/chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(5) # seconds
        WebDriverWait(self.driver,15).until(EC.element_to_be_clickable((By.XPATH,'//p[@class="partial_entry"]/span[contains(@onclick,"clickExpand")]')))
        next = self.driver.find_element_by_xpath('//p[@class="partial_entry"]/span[contains(@onclick,"clickExpand")]')
        self.driver.implicitly_wait(5) # seconds

        self.driver.execute_script("arguments[0].click();", next)
        #next.click()
        self.driver.implicitly_wait(5) # seconds
        #Grabs Tags
        tags = self.driver.find_elements_by_xpath('//div[contains(@class ,"recommend-titleInline")]')
        x = [y.text for y in tags]
        #Grab Reviews
        reviews = []
        for i in self.driver.find_elements_by_xpath('//div[@class="ui_column is-9"]/div[@class="prw_rup prw_reviews_text_summary_hsx"]//p'):
            reviews.append(i.text)
        #Grab titles
        titles = []
        for i in self.driver.find_elements_by_xpath('//span[@class="noQuotes"]'):
            titles.append(i.text)
        #Grabs Hotel name
        h = self.driver.find_element_by_xpath('//h1[@class="header heading masthead masthead_h1 "]')
        hotel=[]
        for i in range(0,len(titles)):
            hotel.append(h.text)
        #Grabs Rating
        bubbles = []
        for i in self.driver.find_elements_by_xpath('//div[@class="ui_column is-9"]/span[contains(@class,"rating bubble")]'):
            bubbles.append(i.get_attribute("class"))
        #Puts out the items towards the pipeline
        # for i in list(zip(x,reviews,titles,hotel,bubbles)):
        #     item = StackItem()
        #     item['tag'] = i[0]
        #     item['review'] = i[1]
        #     item['title'] = i[2]
        #     item['hotel_name'] = i[3]
        #     item['bubble'] = i[4]
        #     yield item
        #Clicks next page for reviews
        #page_turn = self.driver.find_element_by_xpath('//a[@class="nav next taLnk ui_button primary"]')
        #self.driver.implicitly_wait(5) # seconds
        #self.driver.execute_script("arguments[0].click();", page_turn)
        #self.driver.implicitly_wait(5) # seconds
        next_page = response.xpath('/html/head/link[@rel="next"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        #yield scrapy.Request(self.driver.current_url,callback=self.parse)
        #self.driver.close()
