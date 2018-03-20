#
# Script for scrapping products from Samsclub
#


import requests
import traceback
from db import Mdb
from bs4 import BeautifulSoup
from utils import sleep_scrapper, get_request_headers, scraper_csv_write


class SamsclubScraper:

    def __init__(self):
        self.mdb = Mdb()

    def run(self):

        for j in range(0, 2, 1):
            try:
                # url = base_url + str(j) + sufix
                url = 'https://www.samsclub.com/sams/coffee-tea-cocoa' \
                      '/1493.cp?xid=cat_sub&navAction=jump'
                print '[SamsclubScraper] :: fetching data from url: ', url
                r = requests.get(url, headers=get_request_headers())

                if not r.status_code == 200:
                    print "[SamsclubScraper] :: Failed to get content " \
                          "of url: %s" % url
                    return

                html_doc = r.content

                soup = BeautifulSoup(html_doc, 'html.parser')

                for div in soup.find_all('div', class_='products-card'):
                    self.scrap_result_row(div)
                sleep_scrapper('SamsclubScraper')

            except Exception as exp:
                print '[SamsclubScraper] :: run() :: Got exception : %s' % exp
                print(traceback.format_exc())

    def scrap_result_row(self, div):
        try:
            # name
            figure = div.find('figure', title='Full title')
            a = figure.find('a', class_='cardProdLink')
            name = a.find('figcaption', class_='img-text').text.strip()
            print '[SamsclubScraper] :: name: ', name

            # rating
            rat = div.find('div', class_='cust-rating-details')
            cust_rating = rat.find('div', class_='cust-rating')
            rating = cust_rating.find('span', class_='rating-mem')\
                .text.strip()
            print '[SamsclubScraper] :: Rating: ', rating

            # price
            prods_details = div.find('div', class_='prods-details')
            price = prods_details.find('div', class_='sc-price-v2')\
                .text.strip()
            print '[SamsclubScraper] :: price: ', price

            # save Price
            prods_details = div.find('div', class_='prods-details')
            save = ''
            save_off = prods_details.find('div', class_='save-off-price')
            if save_off:
                save_price = save_off.text.strip()
                print '[SamsclubScraper] :: save-price: ', save_price

            self.mdb.samsclub_data(name, rating, price, save_price)

            fname = 'data_samsclub.csv'
            msg = "%s, %s, %s, %s," % (name, rating, price, save_price)
            print "[SamsclubScraper] :: scrap_result_row() :: msg:", msg
            scraper_csv_write(fname, msg)

        except Exception as exp:
            print '[SamsclubScraper] :: scrap_result_row() :: ' \
                  'Got exception: %s' % exp
            print(traceback.format_exc())

if __name__ == '__main__':
    samsclub = SamsclubScraper()
    samsclub.run()
