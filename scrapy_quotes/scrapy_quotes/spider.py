import sys
import os

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import scrapy

class SpiderQuotes(scrapy.Spider):
    name = "spider_quotes"
    start_urls = ["http://quotes.toscrape.com"]
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ROBOTSTXT_OBEY": "False",
        "TELNETCONSOLE_ENABLED": "False",
        "CONCURRENT_REQUESTS": 64,
        "FEED_EXPORT_ENCODING": "utf-8",
        "LOG_LEVEL": "DEBUG",
        "LOG_FILE": "logs/scrapy.log",
        "URLLENGTH_LIMIT": 0,
        "DOWNLOAD_MAXSIZE": 0,
        "RETRY_TIMES": 10,
        "REFERRER_POLICY": "no-referrer",
        "FEED_EXPORT_INDENT": 2,
        "ITEM_PIPELINES": {
            'pipelines.JsonQuotesPipeline': 1
            }
    }
    
    def parse(self, response):
        print(f"Processing {response.url} in quotes/authors function")
        for quote in response.css('div.quote'): 
            yield { 
                'tags': quote.css('div.tags a.tag::text').getall(),
                'author': quote.css('small.author::text').get().strip(), 
                'quote': quote.css('span.text::text').get()
            }
            
            print(f"\nSuccessfully parsed {response.url}")
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

class SpiderAuthors(scrapy.Spider):
    name = "spider_authors"
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ROBOTSTXT_OBEY": "False",
        "TELNETCONSOLE_ENABLED": "False",
        "CONCURRENT_REQUESTS": 64,
        "FEED_EXPORT_ENCODING": "utf-8",
        "LOG_LEVEL": "DEBUG",
        "LOG_FILE": "logs/scrapy.log",
        "URLLENGTH_LIMIT": 0,
        "DOWNLOAD_MAXSIZE": 0,
        "RETRY_TIMES": 10,
        "REFERRER_POLICY": "no-referrer",
        "FEED_EXPORT_INDENT": 2,
        "ITEM_PIPELINES": {
            'pipelines.JsonAuthorsPipeline': 1
            }

    }
    
    def parse(self, response):
        
        for href in response.css('span a::attr(href)').getall():
            yield response.follow(href, callback=self.parse_author)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        for quote in response.css('div.author-details'): 
            yield { 
                'fullname': quote.css('h3.author-title::text').get(), 
                'born_date': quote.css('span.author-born-date::text').get(), 
                'born_location': quote.css('span.author-born-location::text').get(),
                'description': quote.css('div.author-description::text').get().strip(), 
            }

