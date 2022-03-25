import requests
import re, string
from bs4 import BeautifulSoup as bs
import json
from lxml import etree
import pandas as pd
import time
class amazon_crawl():
	def __init__(self):
		self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
						'authority': 'www.amazon.com'}
	def web_crawl(self):
		session = requests.session()
		url = 'https://www.amazon.com/s?k=pc+monitor&page=1&language=en_US&currency=TWD'
		text_ = session.get(url, headers =self.headers).text
		html = etree.HTML(text_)
		items_url_list = html.xpath('//div/h2/a/@href')
		item_id_list = html.xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]/div[@data-component-type="s-search-result"]/@data-asin')

		for item_ord in range(len(item_id_list)):
			item_url = 'https://www.amazon.com'+items_url_list[item_ord]
			item_id = item_id_list[item_ord]
			print(item_url)
			print(item_id)
			text_item = session.get(item_url, headers = self.headers).text
			html_item = etree.HTML(text_item)	
			rating_count = html_item.xpath('//span[@id="acrCustomerReviewText"]/text()')
			try:
				print(rating_count[0])
			except:
				print(0)
			price = html_item.xpath('//span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span/text()')[0]
			print(price)
			brand = html_item.xpath('//tr[@class="a-spacing-small po-brand"]/td/span[@class="a-size-base"]/text()')
			print(brand)
			goods_spcs = html_item.xpath('//tr[@class="a-spacing-small po-specific_uses_for_product"]/td/span[@class="a-size-base"]/text()')
			print(goods_spcs) 
			refresh_rate = html_item.xpath('//tr[@class="a-spacing-small po-refresh_rate"]/td/span[@class="a-size-base"]/text()')
			print(refresh_rate)
			rating = html_item.xpath('//span[@id="acrPopover"]/@title')
			print(rating)
			size = html_item.xpath('//tr[@class="a-spacing-small po-display.size"]/td/span[@class="a-size-base"]/text()')
			print(size)
			date_frist_p = html_item.xpath('//table[@class="a-keyvalue prodDetTable"]/tbody/tr')
			print(date_frist_p)
			input()


amazon_crawl = amazon_crawl()
amazon_crawl.web_crawl()