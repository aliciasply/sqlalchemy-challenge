#!/usr/bin/env python
# coding: utf-8

# In[1]:
# Import Dependencies

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify
import datetime as dt


# In[2]:


# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# conn = engine.connect()


# In[3]:


# Declare a Base using `automap_base()` / reflect an existing database into a new model 
# or use Base = declarative_base()
# Connecting the file to the engine 
Base = automap_base()

# Use the Base class to reflect the database tables/ reflect the tables
Base.prepare(engine, reflect=True)


# In[4]:


# Save references to each table
# Assign the 'measurement' class & 'station' class to a variable called `Measurement` & `Station`
# Assigning 2 tables to these 2 variables 
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[5]:


# Flask Setup
app = Flask(__name__)


# In[9]:


# Home page ("/")

  # List all routes that are available.

@app.route("/")
def home():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")

  # * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  # * Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of date and prcp """
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # creating a blank list

    combine_data = []
    for date, prcp in results:
      dictionary = {}
      dictionary[date] = prcp
      combine_data.append(dictionary)

    return jsonify(combine_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query station data
    results = session.query(Station.station).all()
    session.close()

    result = list(np.ravel(results)) 
    return jsonify(result)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate one year before last day of data
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year
    
    # Query all data from TOBS
    station_month = session.query(Measurement.tobs).order_by(Measurement.tobs.asc()).filter(Measurement.station=='USC00519281').filter(Measurement.date>'2016-08-23').all()
    
    session.close()

    active = list(np.ravel(station_month)) 
    return jsonify(active)


@app.route("/api/v1.0/<start>")
def temp(start):
    session = Session(engine)

    t = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date==start)
    session.close()

    x = []
    dictionary = {}
    for temp in t:
        dictionary["TMIN"] = temp[0]
        dictionary["TMAX"] = temp[1]
        dictionary["TAVG"] = temp[2]
    
    x.append(dictionary)
    return jsonify(x)
        
@app.route("/api/v1.0/<start>/<end>")
def temps(start,end):
    session = Session(engine)

    t = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>start).filter(Measurement.date<end)
    session.close()

    x = []
    dictionary = {}
    for temp in t:
        dictionary["TMIN"] = temp[0]
        dictionary["TMAX"] = temp[1]
        dictionary["TAVG"] = temp[2]
    
    x.append(dictionary)
    return jsonify(x)


# In[ ]:
if __name__ == '__main__':
    app.run(debug=True)



