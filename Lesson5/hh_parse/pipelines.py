# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


# class HhParsePipeline:
#     collection_name = 'hh_scrapy'
#
#     def __init__(self):
#         client = pymongo.MongoClient()
#         self.db = client["gb_parse_123"]
#
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert_one(item)
#         return item
#
#
# class HhVacancyPipeline:
#     collection_name = 'hh_vacancy_scrapy'
#
#     def __init__(self):
#         client = pymongo.MongoClient()
#         self.db = client["gb_parse_123"]
#
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert_one(item)
#         return item


class HhEmployerPipeline:
    collection_name = 'hh_employer_scrapy'

    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client["gb_data_mining"]

    def process_item(self, item, spider):
        if 'employer' in item.get('url', []):
            self.db[self.collection_name].insert_one(item)
        return item


class HhVacancyPipeline:
    collection_name = 'hh_vacancy_scrapy'

    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client["gb_data_mining"]

    def process_item(self, item, spider):
        if 'vacancy' in item.get('url', []):
            self.db[self.collection_name].insert_one(item)
        return item