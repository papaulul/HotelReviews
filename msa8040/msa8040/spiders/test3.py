import scrapy
from selenium import webdriver
import time
from msa8040.items import StackItem
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException


class TestSpider(scrapy.Spider):
    name = 'test3'
    allowed_domains=["tripadvisor.com"]
    #start_urls =['https://www.tripadvisor.com/Hotels-g60898-Atlanta_Georgia-Hotels.html' ]
    start_urls=['https://www.tripadvisor.com/Hotels-g60898-oa60-Atlanta_Georgia-Hotels.html']
    """
    custom_settings={
        'DEPTH_LIMIT':'5'
    }
    """
    def __init__(self):
        self.driver = webdriver.Chrome('/Users/Work/Downloads/chromedriver')

    def parse(self,response):
        #for href in response.xpath('//a[@data-clicksource="HotelName"]/@href'):
        #    yield response.follow(href, self.parse_page)

        href = response.xpath('//a[@data-clicksource="HotelName"]/@href').extract()
        #href = ['/Hotel_Review-g60898-d86197-Reviews-Holiday_Inn_Suites_Atlanta_Airport_North-Atlanta_Georgia.html']
        #href = ['/Hotel_Review-g60898-d114387-Reviews-The_Westin_Peachtree_Plaza_Atlanta-Atlanta_Georgia.html','/Hotel_Review-g60898-d86197-Reviews-Holiday_Inn_Suites_Atlanta_Airport_North-Atlanta_Georgia.html','/Hotel_Review-g60898-d86179-Reviews-Grand_Hyatt_Atlanta_in_Buckhead-Atlanta_Georgia.html','/Hotel_Review-g60898-d223001-Reviews-Wingate_by_Wyndham_Atlanta_Buckhead-Atlanta_Georgia.html','/Hotel_Review-g60898-d224838-Reviews-La_Quinta_Inn_Suites_Atlanta_Airport_North-Atlanta_Georgia.html']

        for hot in href:
            yield scrapy.Request(response.urljoin(hot), self.parse_page)

    def parse_page(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(30) # seconds
        try:
            WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.XPATH,'//p[@class="partial_entry"]/span[contains(@onclick,"clickExpand")]')))
        except TimeoutException:
            print("ERROR1")
            self.driver.implicitly_wait(200) # seconds


        next = self.driver.find_element_by_xpath('//p[@class="partial_entry"]/span[contains(@onclick,"clickExpand")]')
        try:
            WebDriverWait(self.driver,25).until(EC.element_to_be_clickable((By.XPATH,'//span[contains(@onclick,"clickExpand")]')))
        except TimeoutException:
            print("ERROR2")

        self.driver.implicitly_wait(5) # seconds
        try:
            next.click()
        except WebDriverException:
            print("ERROR3")
            self.driver.execute_script("arguments[0].click();", next)
        self.driver.implicitly_wait(5) # seconds
        try:
            WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="review-container"]')))
        except TimeoutException:
            print("ERROR4")
        """
        #Grab titles
        print("TITLESTALE?")
        titles = []
        for i in self.driver.find_elements_by_xpath('//a[@class="title "]/span[@class="noQuotes"]'):
            titles.append(i.text)
        """
        #Grabs Hotel name
        print("HOTELSTALE?")
        h = self.driver.find_element_by_xpath('//h1[@class="header heading masthead masthead_h1 "]')
        hotel=[]
        for i in range(0,5):
            hotel.append(h.text)
        #Grabs Rating
        print("BUBBLESTALE??")
        bubbles = []
        for i in self.driver.find_elements_by_xpath('//div[@class="ui_column is-9"]/span[contains(@class,"rating bubble")]'):
            try:
                bubbles.append(i.get_attribute("class"))
            except StaleElementReferenceException:
                bubbles.append("ERROR")
            #bubbles.append(i.text)
        print("-------------{}".format(len(bubbles)))

        #Grabs Tags
        """print("WTF")
        tags = self.driver.find_elements_by_xpath('//div[contains(@class ,"recommend-titleInline")]')
        print("THIS?????")
        x = [str(y.text) for y in tags]"""

        #Grab Reviews
        print("REVIEWSTALE?")
        reviews = []
        for i in self.driver.find_elements_by_xpath('//div[@class="ui_column is-9"]/div[@class="prw_rup prw_reviews_text_summary_hsx"]//p'):
            try:
                reviews.append(i.text)
            except StaleElementReferenceException:
                reviews.append("ERROR")
                print("I GUESSASKDF")

        #for i in list(zip(reviews,titles,hotel,bubbles)):
        for i in list(zip(reviews,hotel,bubbles)):

            item = StackItem()
            #item['tag'] = i[0]
            item['review'] = i[0]
            #item['title'] = i[1]
            item['hotel_name'] = i[1]
            item['bubble'] = i[2]
            item['url'] = self.driver.current_url
            yield item
            print(item)
        #Clicks next page for reviews
        #

        try:
            WebDriverWait(self.driver,25).until(EC.element_to_be_clickable((By.XPATH,'//a[@class="nav next taLnk ui_button primary"]')))
        except TimeoutException:
            print("----------------------Butwhy")

        print("FUCK")
        try:
            WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.XPATH,'//a[@class="nav next taLnk ui_button primary"]')))
        except TimeoutException:
            print("ERROR6")

        page_turn = self.driver.find_element_by_xpath('//a[@class="nav next taLnk ui_button primary"]')
        print("-------------------ifounditifoundit")
        self.driver.implicitly_wait(5) # seconds
        self.driver.implicitly_wait(5) # seconds
        #

        try:
            page_turn.click()
        except WebDriverException:
            print("ERROR7")
            self.driver.execute_script("arguments[0].click();", page_turn)

        #page_turn.click()
        """
        try:
            WebDriverWait(self.driver,25).until(EC.url_changes(response.urljoin(next_page)))
        except TimeoutException:
            print("Ouchies")
            self.driver.execute_script("arguments[0].click();", page_turn)
            try:
                WebDriverWait(self.driver,25).until(EC.url_changes(response.urljoin(next_page)))
            except TimeoutException:
                print("--------DoubleOuchies---------- it didn't change")
        """
        self.driver.implicitly_wait(30) # seconds
        next_page = response.xpath('/html/head/link[@rel="next"]/@href').extract_first()
        #if 'or30' not in next_page:
        page_numbers =response.xpath('//a[@class ="nav next taLnk ui_button primary"]/@data-page-number').extract_first()
        if int(page_numbers) < 6:
            if "or30" not in next_page:
                print("THIS IS THE PAGE NUMBER: \n\n\n\n\n ",page_numbers," fuck\n\n\n\n\n\n\n\n\n\n\ ",next_page,"\n ",self.driver.current_url,"\n ")
                yield response.follow(next_page, callback=self.parse_page)
                #yield scrapy.Request(self.driver.current_url,callback=self.parse_page)
        else:
            print("\n ",hotel, "IS DONE \n")
            self.driver.implicitly_wait(100000000) # seconds

            #yield scrapy.Request(response.urljoin(next_page),callback=self.parse_page)


        #self.driver.close()
