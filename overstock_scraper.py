#
# Script for scrapping products from Overstock
#


import requests
import traceback
from db import Mdb
from bs4 import BeautifulSoup
from utils import sleep_scrapper, get_request_headers, scraper_csv_write


class OverStockScraper:

    def __init__(self, product_category, product_code):
        self.mdb = Mdb()
        self.product_category = product_category
        self.product_code = product_code

    def run(self):
        url = ''
        try:
            base_url = 'https://www.overstock.com/Home-Garden/%s/%s/' \
                       % (self.product_category, self.product_code)
            sufix = 'subcat.html?page='
            for j in range(1, 100, 1):
                url = base_url + sufix + str(j)
                print '[OverStockScraper] :: fetching data from url:', url
                r = requests.get(url, headers=get_request_headers())

                if not r.status_code == 200:
                    print "[OverStockScraper] :: Failed to " \
                          "get content of url: %s" % url
                    return

                html_doc = r.content

                soup = BeautifulSoup(html_doc, 'html.parser')

                for div in soup.find_all('div', class_='product-tile'):
                    # print '---------div', div
                    self.scrap_result_row(div)
                    # break
                sleep_scrapper('OverStockScraper')
        except Exception as exp:
            print '[OverStockScraper] :: run() :: Got exception : ' \
                  '%s and fetching data from url: %s' % (exp, url)
            print(traceback.format_exc())

    def scrap_result_row(self, div):
        try:
            div = div.find('div', class_='product-info')
            sub_div = div.find('div', class_='product-price-wrapper')
            price = sub_div.find('div', class_='product-price-container')\
                .text.strip()
            print '[OverStockScraper] :: price: ', price
            title = div.find('div', class_='product-title').text.strip()
            print '[OverStockScraper] :: title: ', title
            rating = div.find('div', class_='product-footer')
            print '[OverStockScraper] :: rating: ', rating

            self.mdb.overstock_scraper_data(price, title, rating)

            fname = 'data_over_stock.csv'
            msg = "%s, %s, %s," % (price, title, rating)
            print "[OverStockScraper] :: scrap_result_row() :: msg:", msg
            scraper_csv_write(fname, msg)

        except Exception as exp:
            print '[OverStockScraper] :: scrap_result_row() :: ' \
                  'Got exception: %s' % exp
            print(traceback.format_exc())


if __name__ == '__main__':
    overstock = OverStockScraper('Living-Room-Chairs', '2737')
    overstock.run()
