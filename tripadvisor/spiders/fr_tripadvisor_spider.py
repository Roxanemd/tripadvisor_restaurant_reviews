from tripadvisor.items import TripAdvisorItem
from scrapy import Spider, Request, Selector
import re
from selenium import webdriver
import time

class TripAdvisor(Spider):
    
    name='fr_trip_advisor'
    allowed_urls=['tripadvisor.fr']
    # url for restaurant, ten reviews per page, hierarchy in the form of or-%d
    start_urls=['https://www.tripadvisor.fr/Restaurant_Review-g187147-d719052-Reviews-Epicure-Paris_Ile_de_France.html']


    def __init__(self):
        self.driver = webdriver.Firefox()
    	self.nb_per_page = 10
    
    def parse(self, response):
	print response.url
	self.driver.get(response.url)
	# pour avoir le  commentaire en entier
	next = self.driver.find_element_by_xpath('//span[text()="Plus"]')
	next.click()
	sel = Selector(text=self.driver.page_source)
	reviews = sel.xpath('//div[@class="wrap"]')
	for rev in reviews :
		title=rev.xpath('.//div/a/span/text()').extract_first()
		discussion = rev.xpath('.//div[@class="prw_rup prw_reviews_text_summary_hsx"]//text()').extract()
		raw_txt = ' '.join(discussion)
		content = raw_txt.split('Afficher moins')[0].strip() # response of hotel could be added here
		rating=rev.xpath('.//div[@class="rating reviewItemInline"]/span/@class').extract_first()
		date_=rev.xpath('.//div[@class="rating reviewItemInline"]/span/text()').extract()
		if len(date_)==1:
		    if re.search('(ago)$', date_[0]) != None:
		        date=rev.xpath('.//div[@class="rating reviewItemInline"]/span/@title').extract_first()
		    else:
		            date=date_[0]
		else:
		        date=rev.xpath('.//div[@class="rating reviewItemInline"]/span/@title').extract_first()
		
		item=TripAdvisorItem()
		item['title']=title
		item['rating']=rating
		item['date']=date
		item['content']=content
		yield item 
	#on passe aux  10 avis suivants
	self.nb_per_page += 10
	next_p = 'https://www.tripadvisor.com/Restaurant_Review-g187147-d719052-Reviews-or%d-Epicure-Paris_Ile_de_France.html'%(self.nb_per_page)
	yield Request(next_p, callback=self.parse)



    """def closed(self,reason):
        self.driver.close()"""
                
                
                
