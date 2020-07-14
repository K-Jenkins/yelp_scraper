# yelp_scraper
Web scraper requests a given merchant Yelp page, parses reviews on the page and then requests the next page of reviews using pagination (as implemented by Yelp using review number). On completion of a given merchant review page, the scraper requests each reviewer's page and parses biographic metrics. As of 7/14/20, all data is pipelined to a SQLite3 database after each page request. The project uses the scrapy framework and scrapy-user-agents package; proxies are not currently used due, in part, to Yelp requiring HTTPS requests.

Those interested in using the program will need to insert a merchant page URL within the program on line X, within the quotes and replacing [MERCHANT URL].
