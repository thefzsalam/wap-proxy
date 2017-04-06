from Wotd import Wotd


from flask import Blueprint, render_template

wotd_blueprint = Blueprint('wotd_blueprint',__name__)

@wotd_blueprint.route('/wotd')
def wotd():
    return render_template('wotd.html',**Wotd.get())    
