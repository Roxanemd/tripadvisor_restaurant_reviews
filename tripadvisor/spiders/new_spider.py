from tripadvisor.items import TripAdvisorItem
from scrapy import Spider, Request, Selector
import re
import time


# TODO use loaders


class TripadvisorSpider(Spider):
    name = "fr_test_tripadvisor"
    start_urls = [
        'https://www.tripadvisor.fr/Restaurant_Review-g187147-d719052-Reviews-Epicure-Paris_Ile_de_France.html'
    ]

    def parse(self, response):
	yield Request(response.url, callback=self.parse_restaurant)



    def parse_restaurant(self, response):
        for href in response.xpath('//div[starts-with(@class,"quote")]/a/@href'):
            url = response.urljoin(href.extract())
            yield Request(url, callback=self.parse_review)

        url = response.url
        if not re.findall(r'or\d', url):
            next_page = re.sub(r'(-Reviews-)', r'\g<1>or10-', url)
        else:
            pagenum = int(re.findall(r'or(\d+)-', url)[0])
            pagenum_next = pagenum + 10
            next_page = url.replace('or' + str(pagenum), 'or' + str(pagenum_next))
        yield Request(
            next_page,
            meta={'dont_redirect': True},
            callback=self.parse_restaurant
        )

    def parse_review(self, response):
        item=TripAdvisorItem()
	item['title']= response.xpath('.//div/a/span/text()').extract_first()

        item['content'] = response.xpath('//div[@class="entry"]/p/text()').extract_first()
        item['rating'] = response.xpath('.//div[@class="rating reviewItemInline"]/span/@class').extract_first()
	date_=response.xpath('.//div[@class="rating reviewItemInline"]/span/text()').extract()
	if len(date_)==1:
	    if re.search('(ago)$', date_[0]) != None:
		date=response.xpath('.//div[@class="rating reviewItemInline"]/span/@title').extract_first()
	    else:
		date=date_[0]
	else:
		date=response.xpath('.//div[@class="rating reviewItemInline"]/span/@title').extract_first()
	item['date'] = date
		
        return item

