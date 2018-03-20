#
# Script for scrapping jobs details from Indeed
#


import requests
from db import Mdb
from bs4 import BeautifulSoup
from utils import sleep_scrapper, get_request_headers, scraper_csv_write



class IndeedScrapper:

    def __init__(self, domain, pos, location):

        self.domain = domain.replace(" ", "+")
        self.post = pos.replace(" ", "+")
        self.location = location.replace(" ", "+")
        self.mdb = Mdb()

    def run(self):

        base_url = 'https://www.indeed.co%s/jobs?q=%s&l=%s&start=' % (self.domain, self.post, self.location)
        for j in range(0, 1000, 10):
            url = ''
            try:
                url = base_url + str(j)
                print '[IndeedScrapper] :: fetching data from url:', url
                r = requests.get(url, headers=get_request_headers())

                if not r.status_code == 200:
                    print "[IndeedScrapper] :: Failed to " \
                          "get content of url: %s" % url
                    return

                html_doc = r.content

                soup = BeautifulSoup(html_doc, 'html.parser')
                # print '----------soup', soup
                for div in soup.find_all('div'):
                    # ignore divs with classes
                    if not div.attrs.has_key('class'):
                        continue

                    cls = div.attrs['class']
                    if 'row' in cls and 'result' in cls:
                        self.scrap_result_row(div)
                sleep_scrapper('IndeedScraper')
            except Exception as exp:
                print '[IndeedScraper] :: run() :: Got exception : ' \
                      '%s and fetching data from url: %s' % (exp, url)

    def scrap_result_row(self, div):

        try:
            # title
            title = div.find('span', class_='company').text.strip()
            print "[IndeedScrapper] :: title: %s" % title

            # location
            span = div.find('span', class_='location')
            location = span.text.strip()
            print "[IndeedScrapper] :: location: %s" % location

            # salary
            sal = ''
            span = div.find('span', class_='no-wrap')
            if span:
                sal = span.text.strip()
                print "[IndeedScrapper] :: salary: %s" % sal

            # summary
            span = div.find('span', class_='summary')
            summary = span.text.strip()
            print "[IndeedScrapper] :: summery: %s" % summary

            self.mdb.indeed_scraper_data(title, location, sal, summary)

            fname = 'data_indeed.csv'
            msg = "%s, %s, %s, %s," % (title, location, sal, summary)
            print "[IndeedScrapper] :: scrap_result_row() :: msg:", msg
            scraper_csv_write(fname, msg)

        except Exception as exp:
            print '[IndeedScrapper] :: scrap_result_row() :: ' \
                  'Got exception : %s' % exp

if __name__ == '__main__':
    # scraper = IndeedScrapper('m', 'python', 'United States')
    scraper = IndeedScrapper('.in', 'python', 'mohali punjab')
    scraper.run()
