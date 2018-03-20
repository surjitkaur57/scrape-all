from random import randint
import time


SCRAPPER_SLEEP_MIN = 30  # in seconds
SCRAPPER_SLEEP_MAX = 60  # in seconds


def get_request_headers():
    agents = ['Mozilla/5.0', 'Safari/533.1', 'Chrome/33.0.1750.117']
    return {'User-Agents': agents[randint(0, len(agents)-1)]}


def get_rand_in_range(min, max):
    return randint(min, max)


def get_scrapper_sleep():
    return get_rand_in_range(SCRAPPER_SLEEP_MIN, SCRAPPER_SLEEP_MAX)


def sleep_scrapper(scrapper_name):
    val = get_scrapper_sleep()
    print "\n\n[%s] :: SLEEPING FOR %d seconds.....\n\n" % (scrapper_name, val)
    time.sleep(val)
    print "\n\n[%s] :: RESUMED \n\n" % scrapper_name


def scraper_csv_write(fname, msg):
    msg = msg.encode("utf-8")

    """
    with open(fname, "a") as csv_file:
        writer = csv.writer(csv_file)3
        writer.writerow(row)
    """

    f = open(fname, "a")
    f.write("%s\n" % msg)
    f.close()
