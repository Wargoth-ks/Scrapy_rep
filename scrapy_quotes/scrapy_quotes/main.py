import sys
import os

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time

from scrapy.crawler import CrawlerProcess
from spider import SpiderQuotes, SpiderAuthors
from uploads import upload_json

def main():
    
    print("\nCreating CrawlerProcess\n")

    process = CrawlerProcess()
    process.crawl(SpiderQuotes)
    process.crawl(SpiderAuthors)
    process.start()

    print("\nSpider finish!!!\n")
    
    print("\nUploading files to the mongoDB\n")
    upload_json()
    
    print("\nDone!\n")
    
if __name__ == "__main__":
    start_time = time.time()
    
    print("\nProgram is starting...\n")
    print("\nCreating CrawlerProcess\n")
    
    main()
    
    elapsed_time = time.time() - start_time
    print(f"\nElapsed time: {elapsed_time:.2f} seconds\n")