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

class ArticlePipeline:

    def __init__(self):
        mongo.sequences.delete_one({ '_id': 'articles' })

    def process_item(self, article, spider):
        try:
            _id= get_sequence('articles')
            is_article_exist= mongo.articles.find_one({ '_id' : _id })

            if is_article_exist is None:
                article['_id']= _id
                result= mongo.articles.insert_one(dict(article))

                if result.inserted_id is None:
                    spider.crawler.engine.close_spider(self, 'Processing item failed. Spider close automatically.')
            else:
                result= mongo.articles.find_one_and_update(
                    { '_id': _id },
                    { '$set': dict(article) }
                )

                if result is None:
                    spider.crawler.engine.close_spider(self, 'Processing item failed. Spider close automatically.')

            return article
        except:
            spider.crawler.engine.close_spider(self, 'Processing item failed. Spider close automatically.')
