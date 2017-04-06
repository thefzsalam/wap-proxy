from ImagifyBlueprint import imagify_blueprint
from WotdBlueprint import wotd_blueprint
from TrainTimeBlueprint import traintime_blueprint
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import send_from_directory

app = Flask(__name__)
app.register_blueprint(imagify_blueprint)
app.register_blueprint(wotd_blueprint)
app.register_blueprint(traintime_blueprint)



@app.route('/')
def root():
    return app.send_static_file('index.html')


    
