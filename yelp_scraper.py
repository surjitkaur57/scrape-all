import traceback
import requests
from db import Mdb
from bs4 import BeautifulSoup
from utils import sleep_scrapper, get_request_headers, scraper_csv_write


class YelpScraper:

    def __init__(self, product, location):
        self.product = product.replace(" ", "+")
        self.location = location.replace(" ", "+")
        self.mdb = Mdb()

    def run(self):

        base_url = "https://www.yelp.com/search?find_desc=%s&find_loc=%s,+NY&start=" % (self.product, self.location)

        for j in range(1, 1000, 10):
            try:
                url = base_url + str(j)
                print '[YelpScraper] :: fetching data from url: ', url
                r = requests.get(url, headers=get_request_headers())

                if not r.status_code == 200:
                    print '[YelpScraper] :: Failed to get content of url: %s' % url
                    return

                html_doc = r.content
                soup = BeautifulSoup(html_doc, 'html.parser')

                for li in soup.find_all('li', class_='regular-search-result'):
                    self.scrap_row_yelp(li)
                sleep_scrapper('YelpScraper')
            except Exception as exp:
                print '[YelpScraper] :: run() :: Got exceptiion : %s ' % exp
                print(traceback.format_exc())

    def scrap_row_yelp(self, li):
        try:
            h3 = li.find('h3', class_='search-result-title')

            # Getting title
            title = ''
            spans = h3.find_all('span')
            i = 0
            for span in spans:
                i += 1
            if i == 2:
                title = span.text.strip()

            print "[YelpScraper] :: title: %s" % title

            # Getting reviews count
            reviews_count = 0
            span = li.find('span', class_='review-count rating-qualifier')
            text = span.text
            lst = text.split()
            reviews_count = int(lst[0])

            print "[YelpScraper] :: reviews count: %d" % reviews_count

            # Getting services
            services = []
            span = li.find('span', class_='category-str-list')
            text = span.text
            lst = text.split(',')
            services = [itm.strip() for itm in lst]

            print "[YelpScraper] :: services: %s" % services

            # Getting address
            address = li.find('address').text.strip()

            print "[YelpScraper] :: address: %s" % address

            # Getting phone
            phone = li.find('span', class_='biz-phone').text.strip()

            print "[YelpScraper] :: phone: %s" % phone

            # Getting snippet
            p = li.find('p', class_='snippet').text.strip()
            lst = p.split('read more')
            snippet = lst[0].strip()
            print "[YelpScraper] :: snippet: %s" % snippet

            self.mdb.yelp_scraper_data(title, reviews_count, services, address, phone, snippet)

            fname = 'data_yelp.csv'
            msg = "%s, %s, %s, %s, %s, %s" % (title, reviews_count, services, address, phone, snippet)
            print "[IndeedScrapper] :: scrap_result_row() :: CSV file Msg: ", msg
            scraper_csv_write(fname, msg)

        except Exception as exp:
            print '[YelpScraper] :: scrap_row_yelp() :: Got exception: %s' % exp
            print(traceback.format_exc())

if __name__ == '__main__':
    yelp = YelpScraper('Dry Cleaning', 'New York')
    yelp.run()
