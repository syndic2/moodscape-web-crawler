# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from extensions import mongo
from utilities.helpers import get_sequence

#class CrawlerPipeline:
#    def process_item(self, item, spider):
#        return item

class PsychologyDiseasePipeline:

    def __init__(self):
        mongo.sequences.delete_one({ '_id': 'psychology_diseases' })
        mongo.psychology_diseases.delete_many({})

    def process_item(self, disease, spider):
        try:
            disease['_id']= get_sequence('psychology_diseases')
            result= mongo.psychology_diseases.insert_one(dict(disease))

            if result.inserted_id is None:
                return { 'item': None, 'error': 'Failed store in database' }

            return disease
        except:
            spider.crawler.engine.close_spider(self, 'Processing item failed. Spider close automatically.')

class ArticlePipeline:

    def __init__(self):
        mongo.sequences.delete_one({ '_id': 'articles' })
        mongo.articles.delete_many({})

    def process_item(self, article, spider):
        try:
            article['_id']= get_sequence('articles')
            result= mongo.articles.insert_one(dict(article))

            if result.inserted_id is None:
                return { 'item': None, 'error': 'Failed store in database' }

            return article
        except:
            spider.crawler.engine.close_spider(self, 'Processing item failed. Spider close automatically.')
