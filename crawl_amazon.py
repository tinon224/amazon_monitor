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

        self.item_id_list = []
        self.item_page_list = []
        self.item_page_order_list = []
        self.item_rating_count_list = []
        self.item_price_list = []
        self.item_brand_list = []
        self.item_goods_spcs_list = []
        self.item_refresh_rate_list = []
        self.item_size_list = []
        self.item_avg_rating_list = []
        self.item_5star_rate_list = []
        self.item_4star_rate_list = []
        self.item_3star_rate_list = []
        self.item_2star_rate_list = []
        self.item_1star_rate_list = []
        self.item_review_list = []
        self.item_pro_date_list = []
        self.item_url_list = []

        self.data_dict = {"id":self.item_id_list, "page":self.item_page_list, "order": self.item_page_order_list, "rating_count" : self.item_rating_count_list, 
                          "price" : self.item_price_list, "brand" : self.item_brand_list, "goods_spcs": self.item_goods_spcs_list, "refresh_rate" : self.item_refresh_rate_list, 
                          "size" : self.item_size_list, "avg_rating" : self.item_avg_rating_list, "5star_rating" : self.item_5star_rate_list, "4star_rating" : self.item_4star_rate_list, 
                           "3star_rating" : self.item_3star_rate_list, "2star_rating" : self.item_2star_rate_list, "1star_rating" : self.item_1star_rate_list,
                            "review_key_word" : self.item_review_list, "pro_date" : self.item_pro_date_list, "item_url" : self.item_url_list        
                         }
                
  
    def web_crawl(self,page):
        session = requests.session()
        url = f'https://www.amazon.com/s?k=pc+monitor&page={page}&rh=n%3A1292115011&dc&language=en_US&currency=TWD&qid=1648440009&rnid=2941120011&ref=sr_nr_n_1'
        text_ = session.get(url, headers =self.headers).text
        html = etree.HTML(text_)
        items_url_list = html.xpath('//div/h2/a/@href')
        id_list = html.xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]/div[@data-component-type="s-search-result"]/@data-asin')

        for item_ord in range(len(id_list)):
            item_url = 'https://www.amazon.com'+items_url_list[item_ord]
            item_id = id_list[item_ord]

            if item_id in self.item_id_list:
                continue

            text_item = session.get(item_url, headers = self.headers).text
            html_item = etree.HTML(text_item)   
            rating_count = html_item.xpath('//span[@id="acrCustomerReviewText"]/text()')
            try:
                rating_count = rating_count[0]
            except:
                rating_count = '0 ratings'
            try:    
                price = html_item.xpath('//span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span/text()')[0]
            except:
                price = None

            try:
                brand = html_item.xpath('//tr[@class="a-spacing-small po-brand"]/td/span[@class="a-size-base"]/text()')[0]
            except:
                brand = None

            goods_spcs = html_item.xpath('//tr[@class="a-spacing-small po-specific_uses_for_product"]/td/span[@class="a-size-base"]/text()')
 
            refresh_rate = html_item.xpath('//tr[@class="a-spacing-small po-refresh_rate"]/td/span[@class="a-size-base"]/text()')

            size = html_item.xpath('//tr[@class="a-spacing-small po-display.size"]/td/span[@class="a-size-base"]/text()')

            avg_rating = html_item.xpath('//span[@id="acrPopover"]/@title')

            five_star_rate = html_item.xpath('//a[@class="a-link-normal 5star"]/@title')
            four_star_rate = html_item.xpath('//a[@class="a-link-normal 4star"]/@title')
            three_star_rate = html_item.xpath('//a[@class="a-link-normal 3star"]/@title')
            two_star_rate = html_item.xpath('//a[@class="a-link-normal 2star"]/@title')
            one_star_rate = html_item.xpath('//a[@class="a-link-normal 1star"]/@title')


            time.sleep(1)
            url_review = f'https://www.amazon.com/hz/reviews-render/ajax/lazy-widgets/stream?asin={item_id}&language=en_US&lazyWidget=cr-summarization-attributes&lazyWidget=cr-age-recommendation&lazyWidget=cr-solicitation&lazyWidget=cr-summarization-lighthut'
            text_review = session.post(url_review).text
            text_review = re.sub(r'\\','',text_review)
            try:
                text_review = re.search(r'''"lighthouseTerms":(?:[/]|[\S\s])*}}''',text_review).group()
                text_review = re.sub('[":}]',"",text_review)
                text_review = text_review[14:]
                text_review = text_review.split('/')
            except:
                text_review = []
            
            pro_date = html_item.xpath('//td[@class="a-size-base prodDetAttrValue"]/text()')
            try:
                pro_date = re.sub(r'\s','',pro_date[-1])
                pro_date = re.search(r'[A-Z][a-z]*\d*,\d*',pro_date).group()
 
            except:
                pro_date = None

            self.item_id_list.append(item_id)
            self.item_page_list.append(page)
            self.item_page_order_list.append(item_ord)
            self.item_rating_count_list.append(rating_count)
            self.item_price_list.append(price)
            self.item_brand_list.append(brand)
            self.item_goods_spcs_list.append(goods_spcs)
            self.item_refresh_rate_list.append(refresh_rate)
            self.item_size_list.append(size)
            self.item_avg_rating_list.append(avg_rating)
            self.item_5star_rate_list.append(five_star_rate)
            self.item_4star_rate_list.append(four_star_rate)
            self.item_3star_rate_list.append(three_star_rate)
            self.item_2star_rate_list.append(two_star_rate)
            self.item_1star_rate_list.append(one_star_rate)
            self.item_review_list.append(text_review)
            self.item_pro_date_list.append(pro_date)
            self.item_url_list.append(item_url)
            time.sleep(1)

            



amazon_crawl = amazon_crawl()

for a in range(39,80):
    data = amazon_crawl.web_crawl(a)
df = pd.DataFrame(amazon_crawl.data_dict)
df.to_excel('data2.xlsx')
