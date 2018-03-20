#
# Script for scrapping products from Bed Bath And Beyond
#


import requests
import traceback
from db import Mdb
from bs4 import BeautifulSoup
from utils import sleep_scrapper, get_request_headers, scraper_csv_write


class BedBathAndBeyondScraper:

    def __init__(self, product_category, product_subcategory,
                 product_title, product_code):
        self.mdb = Mdb()
        self.product_category = product_category
        self.product_subcategory = product_subcategory
        self.product_title = product_title
        self.product_code = product_code

    def run(self):
        try:

            url = 'https://www.bedbathandbeyond.com/store/category' \
                  '/%s/%s/%s/%s/' \
                  % (self.product_category, self.product_subcategory,
                     self.product_title, self.product_code)

            print '[BedBathAndBeyondScraper] :: fetching data from url: ', url
            r = requests.get(url, headers=get_request_headers())
            if not r.status_code == 200:
                print "[BedBathAndBeyondScraper] :: Failed to get " \
                        "content of url: %s" % url
                return
            html_doc = r.content

            soup = BeautifulSoup(html_doc, 'html.parser')

            for div in soup.find_all('div', class_='productCo'
                                                   'ntent ec_listing'):
                self.scrap_result_row(div)
            sleep_scrapper('BedBathAndBeyondScraper')
        except Exception as exp:
            print '[BedBathAndBeyondScraper] :: run() :: Got exception: %s'\
                  % exp
            print(traceback.format_exc())

    def scrap_result_row(self, div):

        try:
            div = div.find('div', class_='prodInfo')
            sub_div = div.find('div', class_='prodName')
            a = sub_div.find('a')
            print '[BedBathAndBeyondScraper] :: title: ', a.text.strip()
            div = div.find('div', class_='prodPrice')
            sub_div = div.find('div', class_='priceOfProduct')
            sub = sub_div.find('div', class_='isPrice')
            print '[BedBathAndBeyondScraper] :: price: ', sub.text.strip()

            self.mdb.bedbathandbeyond_scraper_data(a.text.strip(), sub.text.strip())

            fname = 'data_bed_bath_and_beyond.csv'
            msg = "%s, %s," % (a.text.strip(), sub.text.strip())
            print "[BedBathAndBeyondScraper] :: scrap_result_row() :: " \
                  "msg:", msg
            scraper_csv_write(fname, msg)

        except Exception as exp:
            print '[BedBathAndBeyondScraper] :: scrap_result_row() :: ' \
                  'Got exception : %s' % exp
            print(traceback.format_exc())


if __name__ == '__main__':

    bedBathAndBeyond = BedBathAndBeyondScraper('furniture',
                                               'living-room-furniture',
                                               'living-room-collections',
                                               '14307')
    bedBathAndBeyond.run()
