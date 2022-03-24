import scrapy, json
from datetime import datetime

from base_urls import SehatQ
from ..items import ArticleItem

#scrapyrt: http://localhost:9080/crawl.json?spider_name=articles&start_requests=True&crawl_args=%7B%22pages%22%3A%201%7D
class ArticleSpider(scrapy.Spider):
    name= 'article'
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.ArticlePipeline': 300
        }
    }

    def __init__(self, pages= 1, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        
        if type(pages) == str:
            pages= int(pages)       

        self.start_urls= [f"{SehatQ}/artikel/kesehatan-mental?page={(page+1)}" for page in range(pages)]
        self.article_detail_url= 'https://api.sehatq.com/v1/content/articles'

    def parse(self, response):    
        try:
            content_items= response.css('div.content-item')

            for content_item in content_items:
                article_id= int(content_item.attrib['data-id'])
                yield scrapy.Request(f'{self.article_detail_url}/{article_id}', callback= self.parse_api)
        except Exception as ex:
            yield str(ex)
    
    def parse_api(self, response):
        data= json.loads(response.body)['data']
        article= ArticleItem()
        article['title']= data['title']
        article['header_img']= data['images'][0]['url']
        article['short_summary']= data['summary']
        article['author']= data['author']['name']
        article['reviewed_by']= data['reviewedBy']['name']
        article['posted_at']= datetime.strptime(data['updatedDate'].split(' ')[0], '%Y-%m-%d')
        article['content']= data['content']
        article['url_name']= article['title'].lower().replace(', ', ' ').replace(' ', '-')
        article['url']= response.url

        return article

    def extract_content(content):
        pass