import scrapy

from base_urls import SehatQ
from ..items import ArticleItem

#scrapyrt: http://localhost:9080/crawl.json?spider_name=articles&start_requests=True&crawl_args=%7B%22pages%22%3A%201%7D
class ArticleSpider(scrapy.Spider):
    name= 'article'

    def __init__(self, pages= 1, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        
        if type(pages) == str:
            pages= int(pages)

        self.start_urls= [f"{SehatQ}/artikel/kesehatan-mental?page={(page+1)}" for page in range(pages)]

    def parse(self, response):
        articles= response.css('div.sc-htpNat.iZWQZt.content-item')

        for article in articles:
            url= f"{SehatQ}{article.css('a.sc-gZMcBi.sc-kAzzGY.jXGOHm')[1].attrib['href']}"
            
            yield response.follow(url, callback= self.parseData)
    
    def parseData(self, response):
        content_wrapper= response.css('div.sc-dxgOiQ.fzOVOq div.sc-ckVGcZ.hhqONq')

        article= ArticleItem()
        article['_id']= None
        article['title']= content_wrapper.css('h1.sc-gZMcBi.ktSmQt.poppins::text').get()
        article['short_summary']= content_wrapper.css('span.sc-gZMcBi.gQCEgT::text').get()
        article['author']= content_wrapper.css('a.sc-gZMcBi.sc-kAzzGY.bdXpyA.Anchor-NexLink::text')[0].get()
        article['posted_at']= content_wrapper.css('span.sc-gZMcBi.hhLaDY::text').get()
        article['reviewed_by']= content_wrapper.css('a.sc-gZMcBi.sc-kAzzGY.bdXpyA.Anchor-NexLink::text')[0].get()

        if len(content_wrapper.css('img.sc-jzJRlG.dQXahA.sc-cmTdod.dEHRBV')) > 0:
            article['header_img']= content_wrapper.css('img.sc-jzJRlG.dQXahA.sc-cmTdod.dEHRBV').attrib['src']
        elif len(content_wrapper.css('img.sc-jzJRlG.dQXahA.sc-jwKygS.edxZPO')) > 0:
            article['header_img']= content_wrapper.css('img.sc-jzJRlG.dQXahA.sc-jwKygS.edxZPO').attrib['src']
        else:
            article['header_img']= 'https://via.placeholder.com/150'
        
        article['content']= content_wrapper.xpath('string(//div[@class="sc-htpNat eGAHHA"])').get()
        article['url_name']= article['title'].lower().replace(', ', ' ').replace(' ', '-')
        article['url']= response.url
        
        return article  

    def extract_content(content):
        pass