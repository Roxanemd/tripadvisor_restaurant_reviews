# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# items to parse
# ici on pourrait rajouter les notes cuisine, ambiance etc...
class TripAdvisorItem(scrapy.Item):
    title = scrapy.Field()
    rating=scrapy.Field()
    date=scrapy.Field()
    content=scrapy.Field()

    
