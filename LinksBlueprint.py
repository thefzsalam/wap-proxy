from flask import Blueprint,request,redirect,url_for, render_template
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from URLOptimize import URLOptimize

links_blueprint = Blueprint('links_blueprint',__name__)

@links_blueprint.route('/links')
def links():
    url = request.args.get('url')
    if not url:
        redirect(url_for('root'))

    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page)
    urls = []
    for link in soup.findAll('a'):
        # resolve relative
        link_url = urljoin(url,link.get('href'))
        urls+=[link_url]
    urls_dict = URLOptimize.optimize_urls(urls)
    return render_template('links.html',main_url = url,urls_dict = urls_dict)


