# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    biz_revnum = scrapy.Field() #calculated sequentially within code
    biz_date = scrapy.Field()
    biz_rating = scrapy.Field()
    biz_text = scrapy.Field()
    biz_photo = scrapy.Field()
    biz_checkin = scrapy.Field()
    biz_useful = scrapy.Field()
    biz_funny = scrapy.Field()
    biz_cool = scrapy.Field()
    biz_rev_id = scrapy.Field()


class ReviewerScrapeItem(scrapy.Item):
	biz_revnum = scrapy.Field() #use as primary key in SQL
	rev_name = scrapy.Field()
	#rev_start = scrapy.Field()
	rev_elite_start = scrapy.Field()
	rev_elite_finish = scrapy.Field()
	rev_friends = scrapy.Field()
	rev_followers = scrapy.Field()
	rev_recent_rev = scrapy.Field()
	rev_reviews = scrapy.Field()
	rev_photos = scrapy.Field()
	rev_fives = scrapy.Field()
	rev_fours = scrapy.Field()
	rev_threes = scrapy.Field()
	rev_twos = scrapy.Field()
	rev_ones = scrapy.Field()
	rev_useful = scrapy.Field()
	rev_funny = scrapy.Field()
	rev_cool = scrapy.Field()
	rev_tips = scrapy.Field()
	rev_updates = scrapy.Field()
	rev_bookmarks = scrapy.Field()
	rev_firsts = scrapy.Field()
	rev_compliments = scrapy.Field()

