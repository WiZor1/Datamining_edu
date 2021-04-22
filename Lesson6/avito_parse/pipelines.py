# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class AvitoParsePipeline:
    collection_name = 'avito_scrapy'

    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client["gb_data_mining"]

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item