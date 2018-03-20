import os
from flask import Flask, render_template, request
from db import Mdb

app = Flask(__name__)
mdb = Mdb()


@app.route('/')
def home():
    temp_data = {'title': 'Scrap Utils'}
    return render_template('index.html', **temp_data)

   
@app.route('/indeed_scraper')
def indeed_scraper():
    indeed = mdb.get_indeed_data()
    # print 'data---------', data
    temp_data = {'title': 'Scrap_utils', 'indeed': indeed}
    return render_template('indeed.html', **temp_data)


@app.route('/overstock_scraper')
def overstock_scraper():
    overstock = mdb.get_overstock_data()
    temp_data = {'title': 'Scrap_utils', 'overstock': overstock}
    return render_template('overstock.html', **temp_data)


@app.route('/bed_bath_and_beyond')
def bed_bath_and_beyond():
    bedbathandbeyond = mdb.get_bedbathandbeyond_data()
    temp_data = {'title': 'Scrap_utils', 'bedbathandbeyond': bedbathandbeyond}
    return render_template('bed_bath_and_beyond.html', **temp_data)


@app.route('/google_news')
def google_news():
    google_news = mdb.get_google_news_data()
    temp_data = {'title': 'Scrap_utils', 'googleNews': google_news}
    return render_template('google_news.html', **temp_data)


@app.route('/home_depot')
def home_depot():
    homedepot = mdb.get_homedepot_data()
    temp_data = {'title': 'Scrap_utils', 'homedepot': homedepot}
    return render_template('home_depot.html', **temp_data)


@app.route('/samsclub')
def samsclub():
    samsclub = mdb.get_samsclub_data()
    temp_data = {'title': 'Scrap_utils', 'samsclub': samsclub}
    return render_template('samsclub.html', **temp_data)


@app.route('/yelp_scraper')
def yelp_scraper():
    yelp = mdb.get_yelp_data()
    # print 'data---------', data
    temp_data = {'title': 'Scrap_utils', 'yelp': yelp}
    return render_template('yelp.html', **temp_data)


@app.route('/yellow_pages_scraper')
def yellow_pages_scraper():
    yellowpages = mdb.get_yellowpages_data()
    # print 'data---------', yellowpages
    temp_data = {'title': 'Scrap_utils', 'yellowpages': yellowpages}
    return render_template('yellow_pages.html', **temp_data)


@app.route('/flipkart_scraper')
def flipkart_scraper():
    flipkart = mdb.get_flipkart_data()
    print 'data---------', flipkart
    temp_data = {'title': 'Scrap_utils', 'flipkart': flipkart}
    return render_template('flipkart.html', **temp_data)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
