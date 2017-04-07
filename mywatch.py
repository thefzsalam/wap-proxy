from ImagifyBlueprint import imagify_blueprint
from WotdBlueprint import wotd_blueprint
from TrainTimeBlueprint import traintime_blueprint
from GoogleBlueprint import google_blueprint
from LinksBlueprint import links_blueprint
from flask import Flask

app = Flask(__name__)
app.register_blueprint(imagify_blueprint)
app.register_blueprint(wotd_blueprint)
app.register_blueprint(traintime_blueprint)
app.register_blueprint(google_blueprint)
app.register_blueprint(links_blueprint)



@app.route('/')
def root():
    return app.send_static_file('index.html')


    
