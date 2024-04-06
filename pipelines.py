# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient


class JobParserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy_mo

    def process_item(self, item, spider):
        vacancy_name = ''.join(item['name'])
        company_name = ''.join(item['company_name'])
        company_address = ''.join(item['company_address'])
        salary = ''.join(item['salary'])
        vacancy_link = item['vacancy_link']
        site_scraping = item['site_scraping']

        vacancy_json = {
            'vacancy_name': vacancy_name, \
            'company_name': company_name, \
            'company_address': company_address, \
            'salary': salary, \
            'vacancy_link': vacancy_link, \
            'site_scraping': site_scraping
            }

        collection = self.mongobase[spider.name]
        collection.insert_one(vacancy_json)
        return vacancy_json
