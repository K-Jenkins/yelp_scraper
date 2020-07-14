# yelp_scraper
Web scraper requests a given merchant Yelp page, parses reviews on the page and then requests the next page of reviews using pagination (as implemented by Yelp using review number). On completion of a given merchant review page, the scraper requests each reviewer's page and parses biographic metrics. As of 7/14/20, all data is pipelined to a SQLite3 database after each page request. The project uses the [scrapy framework](https://github.com/scrapy) and [scrapy-user-agents package](https://pypi.org/project/scrapy-user-agents/); proxies are not currently used due, in part, to Yelp requiring HTTPS requests.

Those interested in using the program will need to insert a merchant page URL within the program on lines 12, 19 and 205, within the quotes and replacing [MERCHANT URL]. Program must be run using scrapy method: scrapy crawl yelp_spider

The current program uses "if/else" to check if certain elements are present before attempting to parse them. Future commits will replace these checks with "try/except" statements. Some code is commented-out for future update, such code includes explanation of why it is commented out.
