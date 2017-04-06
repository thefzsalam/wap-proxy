from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlencode
from Imagify import Imagify


from flask import Blueprint, render_template,\
                  request,\
                  send_from_directory

imagify_blueprint = Blueprint('imagify_blueprint',__name__)

IMAGIFY_ROOT_PATH = Path('imagify_cache')
if not IMAGIFY_ROOT_PATH.is_dir():
    IMAGIFY_ROOT_PATH.mkdir()

URL_NON_OPTIMIZE_WHITELIST = ['stackexchange.com',
                              'm.wikipedia.org','googleweblight.com']

@imagify_blueprint.route('/imagify')
def imagify():

    url = request.args.get('url').strip()
    if not url:
        return redirect(url_for('root'))
    if not url.startswith('http'):
        url = "http://"+url
    for u in URL_NON_OPTIMIZE_WHITELIST:
        i = url.find(u)
        if i>0 and i<20:
            # if a non optimize url is found somewhere near
            # the beginning of th url, don't optimize
            break
    else:
        url = 'https://googleweblight.com/?lite_url='+url

    index = request.args.get('index')
    if index is None:
        index = 0
    else:
        try:
            index = int(index)
        except ValueError:
            return redirect(url_for('root'))
    title = request.args.get('title')

    imagify = Imagify(IMAGIFY_ROOT_PATH)
    if not title or imagify.get_lasturl() != url:
        title = imagify.imagify(url)

    max_index = imagify.get_no_of_tiles() - 1
    if index <= max_index and index>=0:
        imgurl = imagify.get_tile(index)
    else:
        return redirect(url_for('root'))

    if index>0:
        params = urlencode({
            'title':title,
            'index':index-1,
            'url':url
        })
        appurl_imagify_prev = "/imagify?%s" % params
    else:
        appurl_imagify_prev = None
    if index<max_index:
        params = urlencode({
            'title':title,
            'index':index+1,
            'url':url
        })
        appurl_imagify_next = "/imagify?%s" % params
    else:
        appurl_imagify_next = None
    
    appurl_imagify_links = "/links?%s" % params
    
    return render_template('imagify.html',
                           title = title,
                           imgurl = imgurl,
                           appurl_imagify_next = appurl_imagify_next,
                           appurl_imagify_prev = appurl_imagify_prev,
                           appurl_imagify_links = appurl_imagify_links
                          )

@imagify_blueprint.route('/'+str(IMAGIFY_ROOT_PATH)+'/<path:path>')
def send_imagify_cache(path):
    return send_from_directory(IMAGIFY_ROOT_PATH, path,cache_timeout=1)
