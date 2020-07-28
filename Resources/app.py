import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"api/v1.0/<start>/<end></br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).\
        order_by(Measurement.date).all()

    session.close()
    
    precip_info = []
    for date, prcp in results:
        row = {}
        row['date'] = date
        row['prcp'] = prcp
        precip_info.append(row)

    return jsonify(precip_info)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).all()

    session.close()

    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= last_year).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()

    return jsonify(tobs_results)

# Edit this, values showing up as null
@app.route("/api/v1.0/<start>")
def starting(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    start_info = []
    for result in results:
        row = {}
        row['Date'] = start
        row['Minimum Temperature'] = result[0]
        row['Average Temperature'] = result[1]
        row['Maximum Temperature'] = result[2]
        start_info.append(row)

    return jsonify(start_info)

# Edit this, values showing up as null
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    session.close()

    start_end_info = []
    for result in results:
        row = {}
        row['Start Date'] = start
        row['End Date'] = end
        row['Minimum Temperature'] = result[0]
        row['Average Temperature'] = result[1]
        row['Maximum Temperature'] = result[2]
        start_end_info.append(row)

    return jsonify(start_end_info)

if __name__ == '__main__':
    app.run(debug=True)