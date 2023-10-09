import sys
import os

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
import json

class JsonQuotesPipeline(object):

    def open_spider(self, spider):
        self.file = open('json_files/quotes.json', 'w', encoding="utf-8")
        self.data = []

    def close_spider(self, spider):
        json.dump(self.data, self.file, ensure_ascii=False)
        self.file.close()

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item
    
class JsonAuthorsPipeline(object):

    def open_spider(self, spider):
        self.file = open('json_files/authors.json', 'w', encoding="utf-8")
        self.data = []

    def close_spider(self, spider):
        json.dump(self.data, self.file, ensure_ascii=False)
        self.file.close()

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item