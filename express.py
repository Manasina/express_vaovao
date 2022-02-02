# import scrapy
import scrapy
from scrapy.crawler import CrawlerProcess

# create class
class VaoSpider(scrapy.Spider):
    name = 'vaospider'

    def start_requests(self):
        # list of all category
        categories = ['politique', 'economie', 'faits-divers',
                    'social', 'culture', 'regions', 'sport']

        # for loop for each category
        for category in categories:
            url = f"https://lexpress.mg/category/{category}/"
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        for i in response.xpath('//h2[@class="entry-title h3"]/a/@href').extract():
            yield scrapy.Request(i, callback = self.journal)

        next_page_url = response.xpath('//a[contains(text(),"Suiv")]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
    
    def journal(self, response):
        title = response.xpath('//h1/text()').extract_first()
        date = [i for i in response.url.split('/') if i.isnumeric()]
        day, month, year = date
        official_date = f"{year}-{month}-{day}"


process = CrawlerProcess()
process.crawl(VaoSpider)
process.start()