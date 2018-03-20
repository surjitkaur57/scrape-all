#
# Script for scrapping
#


import requests
import traceback
from db import Mdb
from bs4 import BeautifulSoup
from utils import sleep_scrapper, get_request_headers, scraper_csv_write


class YellowPagesScraper:

    def __init__(self):
        self.mdb = Mdb()

    def run(self):
        base_url = 'https://www.yellowpages.com/search?search_terms=' \
                   'Dry%20Cleaners%20%26%20Laundries&geo_location_' \
                   'terms=New%20York%2C%20NY&page='

        for j in range(0, 1000, 1):
            try:
                url = base_url + str(j)
                print '[YellowPagesScraper] :: fetching data from url: ', url

                r = requests.get(url, headers=get_request_headers())
                if not r.status_code == 200:
                    print '[YellowPagesScraper] :: Failed to get the content ' \
                          'of url: %s' % url
                    return
                html_doc = r.content

                soup = BeautifulSoup(html_doc, 'html.parser')
                for div in soup.find_all('div', class_='info'):
                    self.scrap_result_row(div)
                sleep_scrapper('YellowPagesScraper')
            except Exception as exp:
                print '[YellowPagesScraper] :: run() :: Got exception: %s' % exp
                print(traceback.format_exc())

    def scrap_result_row(self, div):

        try:
            h2 = div.find('h2', class_='n')

            title = div.find('a', class_='business-name').text.strip()

            print "[YellowPagesScraper] :: title: %s" % title


            rating_count = 0
            span = div.find('span', class_='count')

            if span:
                span = span.text.strip()
                rating_count = span

                print "[YellowPagesScraper] :: rating_count: %s" % rating_count

            p = div.find('p', class_='adr')
            address = p.text
            print "[YellowPagesScraper] :: address: %s" % address


            phone = ''
            li = div.find('li', class_='phone primary')
            if li:
                phone = li.text.strip()
                print "[YellowPagesScraper] :: phone: %s" % phone
            else:
                print "[YellowPagesScraper] :: phone: %s" % li


            categories = ''
            cat_div = div.find('div', class_='categories')
            if cat_div:
                categories = cat_div.text.strip()
                print "[YellowPagesScraper] :: categories: %s" % categories
            else:
                print "[YellowPagesScraper] :: categories: %s" % cat_div

            self.mdb.yellowpages_scraper_data(title, rating_count, address, phone, categories)

            fname = 'data_yellow_pages.csv'
            msg = "%s, %s, %s, %s, %s" % (title, rating_count, address, phone, categories)
            print "[YellowPagesScraper] :: scrap_result_row() :: msg:", msg
            scraper_csv_write(fname, msg)

        except Exception as exp:
            print '[YellowPagesScraper] :: scrap_result_row() :: ' \
                  'Got exception: %s' % exp
            print(traceback.format_exc())


if __name__ == '__main__':
    yellowpages = YellowPagesScraper()
    yellowpages.run()

