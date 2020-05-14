from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route('/')
def home():
    print('Home page request')
    return (
        f'Welcome to the Hawaii Vacation Weather home page. Pick a path.<br>'
        f'/api/v1.0/precipitation<br>'
        f'/api/v1.0/stations<br>'
        f'/api/v1.0/tobs<br>'
        f'For the below please add a date between /yyyy-mm-dd/. before 2017-08-24<br>'
        f'/api/v1.0/<start><br>'
        f'/api/v1.0/<start>/<end><br>'
    )

@app.route('/api/v1.0/precipitation')
def precip():
    print('query and print precipitation data')
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    precip_data = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict['Date'] = date
        precip_dict['Precipitation'] = prcp
        precip_data.append(precip_dict)
    
    return jsonify(precip_data)

@app.route('/api/v1.0/stations')
def station():
    print('Query and Print station JSON')

    session = Session(engine)
    
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    stations = []
    for station, name, lat, lng, ele in results:
        stat_dict = {}
        stat_dict['Station'] = station
        stat_dict['Name'] = name
        stat_dict['Latitude'] = lat
        stat_dict['Longitude'] = lng
        stat_dict['Elevation'] = ele
        stations.append(stat_dict)

    
    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    print('Query and Print TOBS JSON')

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-08-23').all()
    session.close()

    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['TOBS'] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)
@app.route('/api/v1.0/<start>')
def date_temp(start):
    print('Query and Print temp data for start date')


    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    temp_list = []
    for min, avg, max in results:
        temp_dict = {}
        temp_dict['Min'] = min
        temp_dict['Avg'] = avg
        temp_dict['Max'] = max
        temp_list.append(temp_dict)

    return jsonify(temp_list)

@app.route('/api/v1.0/<start>/<end>')
def start_end_temp(start, end):
    print('Query and Print temp data for start date')


    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date<=end).all()
    session.close()
    temp_list = []
    for min, avg, max in results:
        temp_dict = {}
        temp_dict['Min'] = min
        temp_dict['Avg'] = avg
        temp_dict['Max'] = max
        temp_list.append(temp_dict)

    return jsonify(temp_list)


if __name__ == "__main__":
    app.run(debug = True)