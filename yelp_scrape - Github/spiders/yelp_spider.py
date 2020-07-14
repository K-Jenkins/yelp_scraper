# -*- coding: utf-8 -*-
import scrapy
from ..items import YelpScrapeItem, ReviewerScrapeItem
from random import randint
from time import sleep

#-----------------------------------------------------------------

class YelpSpiderSpider(scrapy.Spider):
	name = 'yelp_spider'
	allowed_domains = ['yelp.com']
	start_urls = ['[MERCHANT URL]']

	start = 20

	#-------------------------------------------------------------

	def parse(self, response):
		yield scrapy.Request('[MERCHANT URL]', callback=self.parse_biz, meta={'biz_revnum': 1})

	#-------------------------------------------------------------

	def parse_biz(self, response):
		reviews = YelpScrapeItem()

		html_block = response.css(".lemon--li__373c0__1r9wz.margin-b3__373c0__q1DuY.padding-b3__373c0__342DA.border--bottom__373c0__3qNtD.border-color--default__373c0__3-ifU")

		#initialize rev_num for count outside of generator
		rev_num = response.meta["biz_revnum"]

		print(f"---SCRAPING PAGE {YelpSpiderSpider.start/20}---")

		count = 0

		for i in html_block:
			count += 1

			#sequential number of merchant review
			review_num = rev_num
			rev_num +=1

			#-----------------------------------------------------		

			#basic CSS selectors
			review_text = i.css(".lemon--span__373c0__3997G.raw__373c0__3rKqk").css("::text").get()
			review_rev_id = i.css(".lemon--a__373c0__IEZFH.link__373c0__1G70M.link-color--inherit__373c0__3dzpk.link-size--inherit__373c0__1VFlE").css("::attr(href)").get()

			#replace html \xa0 with space
			review_text = review_text.replace("\xa0", " ")

			#-----------------------------------------------------

			#reformat date to ISO8601 YYYY-MM-DD
			def reformat_date(date_val):
				date_tokens = date_val.split("/")
				iso_format = "{}-{}-{}".format(date_tokens[2], date_tokens[0], date_tokens[1])
				return iso_format

			review_date = i.css("span.lemon--span__373c0__3997G.text__373c0__2Kxyz.text-color--mid__373c0__jCeOG.text-align--left__373c0__2XGa-").css("::text").get()
			review_date = reformat_date(review_date)

			#-----------------------------------------------------

			#unique CSS attribute per rating 1-5			
			review_code = [
				".lemon--div__373c0__1mboc.i-stars__373c0__1BRrc.i-stars--regular-1__373c0__3vajv.border-color--default__373c0__3-ifU.overflow--hidden__373c0__2y4YK",
				".lemon--div__373c0__1mboc.i-stars__373c0__1BRrc.i-stars--regular-2__373c0__2lHau.border-color--default__373c0__3-ifU.overflow--hidden__373c0__2y4YK",
				".lemon--div__373c0__1mboc.i-stars__373c0__1BRrc.i-stars--regular-3__373c0__31uEG.border-color--default__373c0__3-ifU.overflow--hidden__373c0__2y4YK",
				".lemon--div__373c0__1mboc.i-stars__373c0__1BRrc.i-stars--regular-4__373c0__1W3ZU.border-color--default__373c0__3-ifU.overflow--hidden__373c0__2y4YK",
				".lemon--div__373c0__1mboc.i-stars__373c0__1BRrc.i-stars--regular-5__373c0__1P0Eg.border-color--default__373c0__3-ifU.overflow--hidden__373c0__2y4YK"
			]

			#iterate over attributes to find true rating
			def get_rating(rating_list):
				for n in range(5):
					if i.css(rating_list[n]):
						check_rating = i.css(rating_list[n]).css("::attr(aria-label)").get()[0]
						check_rating = int(check_rating)
						return check_rating

			review_rating = get_rating(review_code)

			#-----------------------------------------------------
			
			# #---working but does not handle occaisonal additional text elements---
			# #---see general extraction methods below---
			# #photo count in plain text within CSS element
			# #extract text as list			
			# review_photo = i.css(".lemon--a__373c0__IEZFH.link__373c0__1G70M.link-color--blue-dark__373c0__85-Nu.link-size--inherit__373c0__1VFlE").css("::text").getall()

			# #check if value at end of photo_list is number of photos
			# #list format: [' ', '1 photo']
			# #list format with 0 photos: []
			# def photo_check(photo_list):
			# 	if len(photo_list) > 0:
			# 		if int(float(photo_list[-1].split(" ")[0])): #
			# 			return  int(float(photo_list[-1].split(" ")[0]))
			# 		else:
			# 			return 1
			# 	else:
			# 		return 0

			# #update review_photo to integer rating
			# review_photo = photo_check(review_photo)
			# #---|---

			#-----------------------------------------------------

			#unique review block sometimes contains multiple badges
			#number of badges changes CSS element structure
			#above CSS selector does not handle unknown badge types
			#below CSS selector captures all of unique review block
			#below functions identify desired items
			review_badge = i.css(".lemon--div__373c0__1mboc.arrange-unit__373c0__o3tjT.arrange-unit-grid-column--8__373c0__2dUx_.border-color--default__373c0__3-ifU").css("::text").getall()

			#search through list of text for item with photo
			def photo_check(badge_list):
				if len(badge_list) > 0:
					for i in badge_list:
						if len(i.split()) > 1:
							if i.split()[1] == "photo" or i.split()[1] == "photos":
								#print("---Photo identified---")
								return i.split()[0]
							else:
								return 0
			
			#search through list of text for item with check-in
			def checkin_check(badge_list):
				if len(badge_list) > 0:
					for i in badge_list:
						if len(i.split()) > 1:
							if i.split()[1] == "check-in" or i.split()[1] == "check-ins":
								#print("---Checkin identified---")
								return i.split()[0]
							else:
								return 0
			
			review_photo = photo_check(review_badge)
			review_checkin = checkin_check(review_badge)

			#-----------------------------------------------------

			#review bumps in plain text within CSS element
			#extract text from multiple sibling elements as list
			#full bump format without slicing: ['Useful', ' ', '2', 'Funny', ' ', '2', 'Cool', ' ', '1']
			#full bump format with 0 reviews: ['Useful', 'Funny', 'Cool', ' ', '1']
			review_useful = i.css(".lemon--span__373c0__3997G.text__373c0__2Kxyz.text-color--black-extra-light__373c0__2OyzO.text-align--left__373c0__2XGa-.text-size--small__373c0__3NVWO")[0].css("::text").getall()
			review_funny = i.css(".lemon--span__373c0__3997G.text__373c0__2Kxyz.text-color--black-extra-light__373c0__2OyzO.text-align--left__373c0__2XGa-.text-size--small__373c0__3NVWO")[1].css("::text").getall()
			review_cool = i.css(".lemon--span__373c0__3997G.text__373c0__2Kxyz.text-color--black-extra-light__373c0__2OyzO.text-align--left__373c0__2XGa-.text-size--small__373c0__3NVWO")[2].css("::text").getall()

			#check if value at end of review bump list is a number
			#individual bump format: ['Useful', ' ', '2']
			#individual bump format with 0 reviews: ['Useful']
			def bump_check(bump_list):
				if bump_list[-1][0] in "1234567890":
					return int(bump_list[-1])
				else:
					return 0

			#update review bump to integer rating
			review_useful = bump_check(review_useful)
			review_funny = bump_check(review_funny)
			review_cool = bump_check(review_cool)

			#-----------------------------------------------------

			#debugging
			print("")
			print(f"Review #: {review_num}")
			print(f"Review date: {review_date}")
			print(f"Review rating: {review_rating}")
			print(f"Review text: {review_text}")
			print(f"Number of useful reviews: {review_useful}")
			print(f"Number of funny reviews: {review_funny}")
			print(f"Number of cool reviews: {review_cool}")			
			print(f"Number of photos: {review_photo}")
			print(f"Reviewer ID: {review_rev_id}")
			print("")
			
			#-----------------------------------------------------

			#assign scraped values to structure in file: items
			reviews["biz_revnum"] = review_num
			reviews["biz_date"] = review_date
			reviews["biz_rating"] = review_rating
			reviews["biz_text"] = review_text
			reviews["biz_photo"] = review_photo
			reviews["biz_checkin"] = review_checkin
			reviews["biz_useful"] = review_useful
			reviews["biz_funny"] = review_funny
			reviews["biz_cool"] = review_cool
			reviews["biz_rev_id"] = review_rev_id
			
			#-----------------------------------------------------

			yield reviews

			#pass reviewer URL to parse_rev method below
			yield scrapy.Request("https://www.yelp.com"+review_rev_id, callback=self.parse_rev, meta={'biz_revnum': review_num})

		#---------------------------------------------------------
		
		#go to next page
		#recursively call parse_biz method
		next_page = f"https://www.yelp.com/biz/the-butchers-son-berkeley?start={YelpSpiderSpider.start}"
		if YelpSpiderSpider.start < 1300: #stop on page num / 20
			print("Going to next page in 10 seconds")
			sleep(10)
			YelpSpiderSpider.start += 20
			yield response.follow(next_page, callback = self.parse_biz, meta={'biz_revnum': rev_num})

	#-------------------------------------------------------------

	def parse_rev(self, response):
		revr_num = response.meta["biz_revnum"]
		reviewer_block = response.css(".main-content-wrap.main-content-wrap--full")
		reviewer = ReviewerScrapeItem()

		#---------------------------------------------------------

		#text in html tags requires xpath
		revr_name = reviewer_block.xpath("/html/body/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[2]/h1/text()").get()
		revr_friends = reviewer_block.xpath("/html/body/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]/strong/text()").get()
		revr_reviews = reviewer_block.xpath("/html/body/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[1]/ul/li[2]/strong/text()").get()
		revr_photos = reviewer_block.xpath("/html/body/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[1]/ul/li[3]/strong/text()").get()
		revr_useful = reviewer_block.xpath("/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/ul/li[1]/strong/text()").get()
		revr_funny = reviewer_block.xpath("/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/ul/li[2]/strong/text()").get()
		revr_cool = reviewer_block.xpath("/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/ul/li[3]/strong/text()").get()
		revr_tips = reviewer_block.xpath("/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/ul/li[1]/strong/text()").get()
		revr_updates = reviewer_block.xpath("/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/ul/li[2]/strong/text()").get()
		revr_bookmarks = reviewer_block.xpath("/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/ul/li[3]/strong/text()").get()
		revr_firsts = reviewer_block.xpath("/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/ul/li[4]/strong/text()").get()
		revr_followers = reviewer_block.xpath("/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/ul/li[5]/strong/text()").get()

		#xpath changes based on page content, unreliable
		#revr_start = reviewer_block.xpath("/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[5]/ul/li[2]/p/text()").get() 
		
		#---------------------------------------------------------

		#reformat date to ISO8601 YYYY-MM-DD
		def reformat_date(date_val):
			date_tokens = date_val.split("/")
			iso_format = "{}-{}-{}".format(date_tokens[2], date_tokens[0], date_tokens[1])
			return iso_format
		
		#remove excess characters from date
		revr_recent_rev = reviewer_block.css(".rating-qualifier::text").getall()[0]
		revr_recent_rev = revr_recent_rev.replace(" ", "").replace("\n", "")
		revr_recent_rev = reformat_date(revr_recent_rev)

		#---------------------------------------------------------

		revr_rate_list = []
		revr_fives = 0
		revr_fours = 0
		revr_threes = 0
		revr_twos = 0
		revr_ones = 0

		#histogram of ratings is not rendered on every reviewer page
		if reviewer_block.css(".histogram_count::text").getall():
			#ordered but not unique list of elements
			revr_rate_list = reviewer_block.css(".histogram_count::text").getall()
			revr_fives = revr_rate_list[0]
			revr_fours = revr_rate_list[1]
			revr_threes = revr_rate_list[2]
			revr_twos = revr_rate_list[3]
			revr_ones = revr_rate_list[4]

		#---------------------------------------------------------

		#sum number of compliments
		#easier to extract list than in-page sum
		revr_compliments = 0
		if reviewer_block.css(".inline-layout.up-6.clearfix"):
			#Yelp has 11 different compliment types
			#compliment types identifiable only by attribute: background-color: #0073bb
			for i in range(11): 
				#number of compliment items changes per page
				if reviewer_block.xpath(f"/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[4]/ul/li[{str(i)}]/div[2]/small/text()").get():
					comp_val = reviewer_block.xpath(f"/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[4]/ul/li[{str(i)}]/div[2]/small/text()").get()
					revr_compliments += int(comp_val)

		# #---for future use---
		# #Yelp compliment type CSS attribute dict
		# comp_dict = {
		# "background-color: #0073bb": "Like Your Profile",
		# "background-color: #d32323": "Cute Pic",
		# "background-color: #41a700": "You're Funny",
		# "background-color: #f15c00": "Thank You",
		# "background-color: #666666": "Good Writer",
		# "background-color: #fec011": "Great Lists",
		# "background-color: #f15c00": "Just a Note",
		# "background-color: #333333": "Great Photo",
		# "background-color: #d32323": "Hot Stuff",
		# "background-color: #0097ec": "You're Cool",
		# "background-color: #f1bd79": "Write More"
		# }
		# #---|---

		#---------------------------------------------------------

		revr_elite = None
		revr_elite_start = 0
		revr_elite_finish = 0

		#elite badge years within identical CSS elements
		#list format: ['\n                \n\n    ', 'Elite 2020', '\n\n                \n\n    ', '’19']
		if reviewer_block.css(".badge-bar.u-space-r1").css("::text").getall():
			revr_elite = reviewer_block.css(".badge-bar.u-space-r1").css("::text").getall()
			revr_elite = revr_elite[1::2]

		#assign elite years if badge(s) present
		if revr_elite != None:
			if revr_elite[0]:
				revr_elite_finish = revr_elite[0].replace("Elite ", "") #most recent elite year
				if len(revr_elite) >= 2:
					#elites with more than 9 years contian additional "overflow" element
					#last text in "overflow" is not badge year
					if revr_elite[-1].replace("’", "") in "11121314151617181920":
						revr_elite_start = revr_elite[-1].replace("’", "20")
					else:
						revr_elite_start = "2011"
				else:
					revr_elite_start = revr_elite[0].replace("Elite ", "") #start = finish if only current year

		#---------------------------------------------------------

		#recode null values to 0
		def zero_out(val):
			if val != None:
				return val
			else:
				return 0

		#---------------------------------------------------------

		reviewer["biz_revnum"] = response.meta["biz_revnum"]
		reviewer["rev_name"] = revr_name
		reviewer["rev_elite_start"] = revr_elite_start
		reviewer["rev_elite_finish"] = revr_elite_finish
		reviewer["rev_friends"] = revr_friends
		reviewer["rev_followers"] = zero_out(revr_followers)
		reviewer["rev_recent_rev"] = revr_recent_rev	
		reviewer["rev_reviews"] = zero_out(revr_reviews)
		reviewer["rev_photos"] = zero_out(revr_photos)
		reviewer["rev_fives"] = zero_out(revr_fives)
		reviewer["rev_fours"] = zero_out(revr_fours)
		reviewer["rev_threes"] = zero_out(revr_threes)
		reviewer["rev_twos"] = zero_out(revr_twos)
		reviewer["rev_ones"] = zero_out(revr_ones)
		reviewer["rev_useful"] = zero_out(revr_useful)
		reviewer["rev_funny"] = zero_out(revr_funny)
		reviewer["rev_cool"] = zero_out(revr_cool)
		reviewer["rev_tips"] = zero_out(revr_tips)
		reviewer["rev_updates"] = zero_out(revr_updates)
		reviewer["rev_bookmarks"] = zero_out(revr_bookmarks)
		reviewer["rev_firsts"] = zero_out(revr_firsts)
		reviewer["rev_compliments"] = zero_out(revr_compliments)

		yield reviewer

