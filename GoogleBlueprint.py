from flask import Blueprint,request,redirect,url_for,render_template
from URLOptimize import URLOptimize
import google

google_blueprint = Blueprint('google_blueprint',__name__)

@google_blueprint.route('/google')
def google_search():
    no_optimize = request.args.get('no_optimize')
    query = request.args.get('q')
    if not query:
        redirect(url_for('root'))

    urls = google.search(query,stop=20)
    urls_dict = URLOptimize.optimize_urls(urls)

    return render_template('google_search.html',urls_dict=urls_dict,query=query,no_optimize=bool(no_optimize))
