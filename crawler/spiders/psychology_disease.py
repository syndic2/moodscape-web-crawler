import scrapy

from base_urls import SehatQ
from ..items import PsychologyDiseaseItem

class PsychologyDiseaseSpider(scrapy.Spider):
    name= 'psychology_disease'
    start_urls= [
        f"{SehatQ}/penyakit/psikologi"
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.PsychologyDiseasePipeline': 300
        }
    }

    def parse(self, response):
        diseases= response.css('div.sc-dxgOiQ.cYiEHD')

        for disease in diseases.css('div.sc-ckVGcZ.dVYwMS'):
            url= f"{SehatQ}{disease.css('a.sc-gZMcBi.sc-kAzzGY.jXGOHm').attrib['href']}"

            print('url', url)

            yield response.follow(url, callback= self.parseData)
    
    def parseData(self, response):
        content_wrapper= response.xpath('//div[@class="sc-htpNat iZWQZt"]')
        accordion_wrapper= content_wrapper.xpath('.//div[@class="sc-htpNat kiHNpi accordion-disease"]')
        descriptions_section_wrapper= accordion_wrapper.xpath('.//div[@class="sc-fYxtnH kqjufG"]')
        short_description= descriptions_section_wrapper.xpath('string(.//div[@class="sc-htpNat iZWQZt"]/span[1])')

        disease= PsychologyDiseaseItem()
        disease['_id']= None
        disease['name']= content_wrapper.css('h1.sc-gZMcBi.lfRwAY.poppins::text').get()
        disease['short_description']= short_description.get()

        if len(content_wrapper.css('img.sc-jzJRlG.kAhOzf')) > 0:
            disease['img_url']= content_wrapper.css('img.sc-jzJRlG.kAhOzf').attrib['src']
        else:
            disease['img_url']= 'https://via.placeholder.com/150'

        disease['url']= response.url

        return disease
        
