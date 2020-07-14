# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from .items import YelpScrapeItem, ReviewerScrapeItem

class YelpScrapePipeline:
	# def process_item(self, item, spider):
	# 	return item
	
	def __init__(self):
		self.sql_conn()
		self.c.execute("DROP TABLE IF EXISTS review_table")
		self.c.execute("DROP TABLE IF EXISTS reviewer_table")
		self.create_table()
		pass

	#-------------------------------------------------------------

	def sql_conn(self):
		self.conn = sqlite3.connect("yelp_test.db")
		self.c = self.conn.cursor()
	
	#-------------------------------------------------------------

	def create_table(self):

		#create table for reviewers
		#dict of value type
		#alternatively pass in items
		#if pass in items, create dictionary for python type to SQL type
		biz_header_dict = {
			"biz_revnum": "INT", 
			"biz_date": "TEXT",
			"biz_rating": "INT",
			"biz_text": "TEXT",
			"biz_photo": "INT",
			"biz_chekin": "INT",
			"biz_useful": "INT",
			"biz_funny": "INT",
			"biz_cool": "INT",
			"biz_rev_id": "TEXT"
			}

		#create string of header-type list
		biz_table_header_type = [biz_header_dict[i] for i in biz_header_dict.keys()]
		biz_table_header_name = [i for i in biz_header_dict.keys()]
		biz_table_header_list = ["{} {}".format(biz_table_header_name[i], biz_table_header_type[i]) for i in range(len(biz_table_header_name))]
		biz_table_header_final = ", ".join(biz_table_header_list)

		self.c.execute("CREATE TABLE review_table({})".format(biz_table_header_final))

		#---------------------------------------------------------

		#create table for reviewers
		#dict of value type
		#alternatively pass in items
		#if pass in items, create dictionary for python type to SQL type
		rev_header_dict = {
			"biz_revnum": "INT",
			"rev_name": "TEXT",
			#"rev_start": "TEXT", #unreliable, to updated in future commit
			"rev_elite_start": "INT",
			"rev_elite_finish": "INT",
			"rev_friends": "INT",
			"rev_followers": "INT",
			"rev_recent_rev": "TEXT",		
			"rev_reviews": "INT",
			"rev_photos": "INT",
			"rev_fives": "INT",
			"rev_fours": "INT",
			"rev_threes": "INT",
			"rev_twos": "INT",
			"rev_ones": "INT",
			"rev_useful": "INT",
			"rev_funny": "INT",
			"rev_cool": "INT",
			"rev_tips": "INT",
			"rev_updates": "INT",
			"rev_bookmarks": "INT",
			"rev_firsts": "INT",
			"rev_compliments": "INT"
			}

		#create string of header-type list
		rev_table_header_type = [rev_header_dict[i] for i in rev_header_dict.keys()]
		rev_table_header_name = [i for i in rev_header_dict.keys()]
		rev_table_header_list = ["{} {}".format(rev_table_header_name[i], rev_table_header_type[i]) for i in range(len(rev_table_header_name))]
		rev_table_header_final = ", ".join(rev_table_header_list)

		self.c.execute("CREATE TABLE reviewer_table({})".format(rev_table_header_final))

	#-------------------------------------------------------------

	def process_item(self, items, spider):
		if len(items) == 10:
			print("Pipeline: BIZ review number -- {}".format(items["biz_revnum"]))
			print("")
			self.store_review(items)

		if len(items) == 22:
			print("Pipeline: REVR review number -- {}".format(items["biz_revnum"]))
			print("")
			self.store_reviewer(items)

		#return items

	#-------------------------------------------------------------

	def store_review(self, items):
		#generate list of SQL value insertions
		item_keys = [i for i in items.keys()]

		#generate number of SQL value insertions
		insert_num_list = ["?" for i in range(len(item_keys))]
		insert_num_final = ", ".join(insert_num_list)

		#generate list values to insert
		insert_value_list = [items[i] for i in item_keys]

		self.c.execute("INSERT INTO review_table VALUES ({})".format(insert_num_final), insert_value_list)
		self.conn.commit()

	#-------------------------------------------------------------

	def store_reviewer(self, items):
		#generate list of SQL value insertions
		item_keys = [i for i in items.keys()]

		#generate number of SQL value insertions
		insert_num_list = ["?" for i in range(len(item_keys))]
		insert_num_final = ", ".join(insert_num_list)

		#generate list values to insert
		insert_value_list = [items[i] for i in item_keys]

		self.c.execute("INSERT INTO reviewer_table VALUES ({})".format(insert_num_final), insert_value_list)
		self.conn.commit()