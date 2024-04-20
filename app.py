# Import the dependencies.
import datetime as dt
import numpy as np

import pandas


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from flask import Flask, send_file
import os


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# adding image to landing page
#image_path = os.path.join("/static/Images.jpeg")




#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
   
    return (
        #f"<img src=image_path, alt='Image'>"
        "Welcome to Hawaii Climate Analysis API!"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>" 
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/temp/&lt;start_date&gt;/<br/>"
        "/api/v1.0/temp/&lt;start_date&gt;/&lt;end_date&gt/<br/>"
        "To format the date '2022-01-01'"
   )
#@app.route('/image')
#def get_image():
    #return send_file(image_path, mimetype = 'image/jpeg')

@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= recent_date).all()
    precipit = {date:prcp for date, prcp in precipitation}
    print(precipit)
    return jsonify(precipit)


@app.route("/api/v1.0/stations")
def stations():
   station_results = session.query(Station.station).all()
   stations = list(np.ravel(station_results))
   return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():

    recent_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= recent_date).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



@app.route("/api/v1.0/temp/<start>/")

@app.route("/api/v1.0/temp/<start>/<end>/")



def stats(start, end= None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        starting_date = dt.datetime.strptime(start,"%Y-%m-%d")

        results = session.query(*sel).\
                filter(Measurement.date >= starting_date).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)