#
# Script for scrapping products from flipkart
#


import requests
import traceback
from bs4 import BeautifulSoup
from db import Mdb
from utils import sleep_scrapper, get_request_headers, scraper_csv_write


class FlipkartScraper:

    def __init__(self, product):
        self.product = product
        self.mdb = Mdb()

    def run(self):

        try:
            base_url = 'https://www.flipkart.com/search?as=off&as-show=' \
                       'on&otracker=start&page='
            sufix = '&q=%s&viewType=list' % self.product

            for i in range(1, 100, 1):
                url = base_url + str(i) + sufix
                print '[FlipkartScraper] :: fetching data from url: ', url

                r = requests.get(url, headers=get_request_headers())
                if not r.status_code == 200:
                    print '[FlipkartScraper] :: Failed to get the content ' \
                          'of url: %s' % url
                    return
                html_doc = r.content

                soup = BeautifulSoup(html_doc, 'html.parser')
                # for div in soup.find_all('div', class_='col col-7-12'):
                for div in soup.find_all('div', class_='_1-2Iqu row'):
                    # print '---------------------div', div
                    self.scrap_result_row(div)
                sleep_scrapper('FlipkartScraper')
        except Exception as exp:
            print '[FlipkartScraper] :: run() :: Got exception: %s' % exp
            print(traceback.format_exc())

    def scrap_result_row(self, div):

        try:
            Product_div = div.find('div', class_='col col-7-12')
            title = Product_div.find('div', class_='_3wU53n').text.strip()
            print '[FlipkartScraper] :: title . . . . ..:', title
            # title_description = div.find('div', class_='OiPjke').text.strip()
            # print'[FlipkartScraper] :: title_description: ', title_description

            rating = div.find('div', class_='niH0FQ')
            sub_rating = rating.find('span', class_='_38sUEc').text.strip()
            print '[FlipkartScraper] :: rating . . . . .:', sub_rating

            specifications_div = div.find('div', class_='_3ULzGw')
            specifications = specifications_div.find('ul', class_='vFw0gD').text.strip()
            print '[FlipkartScraper] :: specifications .: ', specifications

            product_price = div.find('div', class_='_6BWGkk')
            div_price = product_price.find('div', class_='_1uv9Cb')
            price = div_price.find('div', class_='_1vC4OE _2rQ-NK').text.strip()
            print '[FlipkartScraper] :: price . . . . . :', price

            self.mdb.flipkart_scraper_data(title, sub_rating, specifications, price)

            fname = 'data_flipkart.csv'
            msg = "%s, %s, %s, %s," % (title, sub_rating, specifications, price)
            print "[FlipkartScraper] :: scrap_result_row() :: msg:", msg
            scraper_csv_write(fname, msg)

        except Exception as exp:
            print '[FlipkartScraper] :: scrap_result_row() :: ' \
                  'Got exception: %s' % exp
            print(traceback.format_exc())

if __name__ == '__main__':
    flipkart = FlipkartScraper('iphones')
    flipkart.run()

