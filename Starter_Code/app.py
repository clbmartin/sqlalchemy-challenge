# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
app=Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station =Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


@app.route("/")
# reflect an existing database into a new model

# reflect the tables
def home():
    return(
        f"<center><h2>Welcome to the Hawaii Climate Analysis Local API</h2></center>"
        f"<center><h3>Select from one of the avaialble routes:</<h3></center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>/api/v1.0/stations</center>"
        f"<center>/api/v1.0/tobs</center>"
        f"<center>/api/v1.0/start/end</center>"
    )
@app.route("/api/v1.0/precipitation")
def precip():
   
   # Calculate the date one year from the last date in data set.
    previousYear = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previousYear).all()

    session.close()

    precipitation= {date: prcp for date, prcp in results}
    return jsonify(precipitation)             

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    session.close()


    stationList =list(np.ravel(results))

    return jsonify(stationList)


@app.route("/api/v1.0/tobs")
def temperatures():

    previousYear = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.tobs).\
            filter(Measurement.station =='USC00519281').\
            filter (Measurement.date >= previousYear).all()
    
    session.close()         


    temperatureList =list(np.ravel(results))

    return jsonify(temperatureList)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dataStats(start=None, end=None):
           
    selection =[func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)] 

    if not end:

        startDate = dt.datetime.strptime(start, "%m%dY")

        results = session.query(*selection).filter(Measurement.date>=startDate)

        session.close()

        temperatureList =list(np.ravel(results))

        return jsonify(temperatureList)

    else:

        startDate = dt.datetime.strptime(start, "%m%dY")
        endDate = dt.datetime.strptime(end, "%m%dY")

        results = session.query(*selection)\
            .filter(Measurement.date>=startDate)\
            .filter (Measurement.date <= endDate).all()


        session.close()

        temperatureList =list(np.ravel(results))

    return jsonify(temperatureList)

if __name__ == '__main__':
  app.run(debug=True)
# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
