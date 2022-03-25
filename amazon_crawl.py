import scrapy


class AmazonCrawlSpider(scrapy.Spider):
    name = 'amazon_crawl'
    allowed_domains = ['https://www.amazon.com']
    start_urls = ['https://www.amazon.com/s?k=monitor&page=1']

    def parse(self, response):
    	for page in range(30):
        	page_url = f'https://www.amazon.com/s?k=monitor&page={page}'
        	yield scrapy.Request(page_url, callback = parse_page)

    def parse_page(self, response):
        items = response.xpath('//div/h2/a/@href')
        for item_url in tems:
            item_url = 'https://www.amazon.com'+item_url
            yield scrapy.Request(item_url, callback = parse_item)

    def parse_item(self, response):
        
    	

