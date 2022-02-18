# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstagramParserPipeline:
    def process_item(self, item, spider):

        return item



class MongoPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        try:
            if not collection.count_documents({"user_id": item['user_id']}):
               collection.insert_one(item)
            else:
                if len(item['subscriptions']) > 1:
                    collection.replace_one({"user_id": item['user_id']}, item, upsert=True)
                else:
                    if item['subscriptions'][0] is not None:
                        doc = collection.find_one({"user_id": item['user_id']})
                        subs = set(doc['subscriptions'] + item['subscriptions'])
                        subs.discard(None)
                        collection.update({"user_id": item['user_id']}, {"$set":  {'subscriptions': list(subs)}}, upsert=True)

        except ValueError:
            print(ValueError)

        return item