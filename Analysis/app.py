# Import the dependencies.

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()


# reflect the tables

Base.prepare(engine, reflect=True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Home page.

@app.route("/")
def home_page(): return ("Available Routes:<br/>"
                            "/api/v1.0/precipitation<br/>"
                            "/api/v1.0/stations<br/>"
                            "/api/v1.0/tobs<br/>"
                            "/api/v1.0/<start><br/>"
                            "/api/v1.0/<start>/<end><br/>")

# Precipitation page.

@app.route("/api/v1.0/precipitation")
def precipitation(): 
    results = session.query(Measurement.date, Measurement.prcp).all()
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

# Stations page.

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# Tobs page.

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()
    tobs = list(np.ravel(results))
    return jsonify(tobs)

# Start page.

@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    start = list(np.ravel(results))
    return jsonify(start)

# Start and end page.

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    start_end = list(np.ravel(results))
    return jsonify(start_end)

if __name__ == '__main__':
    app.run(debug=True)

