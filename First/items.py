# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstItem(scrapy.Item):
    jobName = scrapy.Field()
    jobMoney = scrapy.Field()
    jobNeed = scrapy.Field()
    jobCompany = scrapy.Field()
    jobType = scrapy.Field()
    jobSpesk = scrapy.Field()
    jobClass=scrapy.Field()
    jobUrl=scrapy.Field()
      # name = scrapy.Field()
    pass
