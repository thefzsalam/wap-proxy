from flask import Blueprint, render_template
from TrainTime import TrainTime

traintime_blueprint = Blueprint('traintime_blueprint',__name__)


@traintime_blueprint.route('/traintime/')
def traintime_index():
    return render_template('traintime_index.html',stations = list(TrainTime.getAvailableStations())+list(TrainTime.getAvailableBwStations()))


@traintime_blueprint.route('/traintime/<string:station>')
def traintime(station):
    if '-' in station:
        trains,timestamp = TrainTime.getTrainsBwStations(station)
        if trains is None:
            return traintime_blueprint.send_static_file('traintime_error.html')
        return render_template('traintime_bw_stations.html',trains = trains,timestamp = timestamp)
    else:
        trains,timestamp = TrainTime.getTrainsFromStation(station)
        if trains is None:
            return traintime_blueprint.send_static_file('traintime_error.html')
        return render_template('traintime_from_station.html',
                           trains = trains, timestamp = timestamp)
