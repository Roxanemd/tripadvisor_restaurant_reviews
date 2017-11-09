# tripadvisor_restaurant_reviews

Python spider and scraper for Tripadvisor restaurant reviews

## Getting Started

These instructions will get you an introduction of the program and running it for further development, testing and improvements.

### Prerequisites

Python 2.7 
Scrapy
Selenium

Tested on Ubuntu 14.04

### How to start program

Launch this command in the scrapy_tripadvisor_reviews/tripadvisor subdirectory : 

$ scrapy crawl fr_tripadvisor -o result_fr.json

We are calling the fr_tripadvisor.py spider and telling it to output to a file.
Programs opens a Firefox window to defined url. Each page is loaded in window while items are being parsed. Time to parse 1000 reviews is about a few minuts on my machine.


### A few words about scrapy

See the docs on how to easily create a project and how a module is supposed to look like

https://doc.scrapy.org/en/latest/intro/tutorial.html

In repertory "spiders" you define your routines, which means a set of urls to parse and how to parse them.
Four basics items are parsed from the reviews : title, rating, date, content of review
These items are defined in the "items.py" file.

Selenium is the module I found in order to solve the fact that I had to click in order to have whole review. 

For debugging I used the following command : 
$ scrapy shell https://www.tripadvisor.fr/Restaurant_Review-g187147-d719052-Reviews-or10-Epicure-Paris_Ile_de_France.html


This opens a scrapy shell in which you can test code (first lines examples below)

from selenium import webdriver
from scrapy import Selector

#opens firefox and loads url passed to parse()
driver = webdriver.Firefox()
print response.url
driver.get(response.url)
# pour avoir le  commentaire en entier
next = driver.find_element_by_xpath('//span[text()="Plus"]')
next.click()

sel = Selector(text=driver.page_source)
reviews = sel.xpath('//div[@class="wrap"]')

### Difficulties

I find it hard to obtain a nice full result of the review. It was hard to access the whole element and not the summary.
In some cases I also have a part of the restaurant owner in the item. 

# Langages for reviews
Working on english reviews


