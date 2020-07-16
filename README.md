# yelp_scraper
Web scraper requests a given merchant Yelp page, parses reviews on the page and then requests the next page of reviews using pagination (as implemented by Yelp using review number). On completion of a given merchant review page, the scraper requests each reviewer's page and parses biographic metrics. As of 7/14/20, all data is pipelined to a SQLite3 database after each page request. The project uses the [scrapy framework](https://github.com/scrapy) and [scrapy-user-agents package](https://pypi.org/project/scrapy-user-agents/); proxies are not currently used due, in part, to Yelp requiring HTTPS requests.

Visualizations: [Tableau Public keith.jenkins6463#!](https://public.tableau.com/profile/keith.jenkins6463#!/)

Those interested in using the program will need to insert a merchant page URL within the program on lines 12, 19 and 205, within the quotes and replacing [MERCHANT URL]. Program must be run via shell using scrapy method: scrapy crawl yelp_spider

Dependencies: scrapy, random, time, SQLite3

--Roadmap--

Replace "if/else" checks with "try/except"

Replace SQLite3 db generation, write with PostgreSQL

Update commented-out code (contextual explanation within comments)

Develop parse_search to scrape search results page (one level higher), cycle through multiple merchants

Develop basic GUI, likely using Kivy
