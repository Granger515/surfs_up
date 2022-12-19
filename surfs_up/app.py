##9.5.2 Import dependencies and other set up

#Import general dependencies
import datetime as dt
import numpy as np
import pandas as pd

#Import dependencies for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Import Flask
from flask import Flask, jsonify

#Create Base
Base = automap_base()

#Create the engine
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={"check_same_thread": False})

#Reflect on database
Base.prepare(engine, reflect=True)

#Create variables for the classses
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create the session link
session = Session(engine)

#Create a flask application named 'app'
app = Flask(__name__)

##9.5.2 Create the Welcome Route - Allows access to all of analyses

#Define the welcome route
@app.route("/")

#Create other routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')



##9.5.3 Precipitation Route - Allows access to one year of Precipitation data

#Define Precipitation route
@app.route("/api/v1.0/precipitation")

#Create the Precipitation function
def precipitation():

   #Limit data to one year
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   #Get data
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    
   #Creates a dictionary to hold the data
   precip = {date: prcp for date, prcp in precipitation}

   #Returns the dictionary as a JSON structured file
   return jsonify(precip)




##9.5.4 Station Route - Allows access Stations data

#Define Station route
@app.route("/api/v1.0/stations")

#Create the Station function
def stations():

    #Get all stations
    results = session.query(Station.station).all()

    #Creates an array with the results of the previous querry, unravels it, and puts it in a list
    stations = list(np.ravel(results))

    #Returns the list as a JSON structured file
    return jsonify(stations=stations)




##9.5.5 Temperature Route - Allows access to one year of Temperature data

#Define Temperature route
@app.route("/api/v1.0/tobs")

#Create the Temperature function
def temp_monthly():

   #Limit data to one year
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   #Get data for one year (for a particular station)
   results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
   
   #Creates an array with the results of the previous querry, unravels it, and puts it in a list
   temps = list(np.ravel(results))

   #Returns the list as a JSON structured file
   return jsonify(temps=temps)




##9.5.6 Statistics Route - Allows access to minimum, maximum, and average temperatures

#Defines the start and end routes
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#Create the Stats function
def stats(start=None, end=None):

    #Calculates the values
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    #This block of code looks to see if there is an end date. If there is not it selects all data after the start date.
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    #This block of code looks to see if there is a start date. If there is not it selects all data before the end date. 
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    #Creates an array with the results of the previous querry, unravels it, and puts it in a list
    temps = list(np.ravel(results))
    
    #Returns the list as a JSON structured file  
    return jsonify(temps)

if __name__ == '__main__':
    app.run()