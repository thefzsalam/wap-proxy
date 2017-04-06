from flask import Blueprint,request,redirect,url_for
import google

google_blueprint = Blueprint('google_blueprint',__name__)

@google_blueprint.route('/google')
def google_search():
    no_optimize = request.args.get('no_optimize')
    query = request.args.get('q')
    if not query:
        redirect(url_for('root'))


    urls = google.search(get_vars['q'][0],stop=20)
    if not no_optimize:
        urls_ = []
        for url in urls
            if url.startswith('https://'):
                url = url.replace('https://','http://',1)
            if url.startswith('http://en.wikipedia'):
                url = url.replace('en.wiki','en.m.wiki',1)
            # NOTE: Imagify URL
            url = url_for('imagify',url=url)
            urls_ += [url]
        urls = urls_

    return render_template('google_search.html',urls=urls,query=query,no_optimize=bool(no_optimize))
