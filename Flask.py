# Dependencies
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, send_file



# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
        f"<h1> Welcome to Andrew's Homework </h1>"
        f"Available Routes:<br/>"
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<h2> dates should be entered YYYY-MM-DD <br/></h2>"
        f"/api/v1.0/start=<date><br/>"
        f"      ex: /api/v1.0/start=2015-08-07<br/>"
        f"/api/v1.0/end=<date><br/>"
        f"      ex: /api/v1.0/end=2015-08-07<br/>"
        f"/api/v1.0/start=<date>/end=<date><br/>"
        f"      ex: /api/v1.0/start=2015-08-07/end=2016-08-07<br/>"
        
    )

@app.route("/api/v1.0/percipitation")
def percipitation():
    """the last 12 months of precipitation"""
   # Query 
    conn = engine.connect()
    prcp_df = pd.read_sql("SELECT date, prcp FROM measurement WHERE date BETWEEN '2016-08-23' AND '2017-08-23'", conn).set_index('date').sort_index(axis=0)
    # Convert Data Frame to HTML
    prcp_html= prcp_df.to_html()
    
    return (prcp_html) 

@app.route("/api/v1.0/stations")
def stations():
    """all stations"""
    # Query
    session = Session(engine)
    stations = session.query(Station.station).all()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """the last 12 months of temperatures recorded"""
    # Query
    session = Session(engine)
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-18')
    
  # Create a dictionary from the row data and append to a list
    tobs_data = []
    for date, t in tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = t
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/start=<start_date>")
def start_date_query(start_date):
    """Fetch the temperature data from start date"""
    #Query
    conn = engine.connect()
    tobs_start_df = pd.read_sql_query(f"SELECT MIN(tobs), MAX(tobs), AVG(tobs) FROM measurement WHERE date >='{start_date}'", conn)
    # Convert Data Frame to JSON
    tobs_start_json = tobs_start_df.to_json()

    return jsonify(tobs_start_json)

@app.route("/api/v1.0/end=<end_date>")
def end_date_query(end_date):
    """Fetch the temperature data from end date"""
    # Query
    conn = engine.connect()
    tobs_end_df = pd.read_sql_query(f"SELECT MIN(tobs), MAX(tobs), AVG(tobs) FROM measurement WHERE date <='{end_date}'", conn)
    # Convert Data Frame to HTML
    tobs_end_html = tobs_end_df.to_html()

    return (tobs_end_html)

@app.route("/api/v1.0/start=<start_date>/end=<end_date>")
def start_end_query(start_date, end_date):
    """Fetch the temperature data from start and end date"""
    # Query
    conn = engine.connect()
    tobs_cust_df = pd.read_sql_query(f"SELECT MIN(tobs), MAX(tobs), AVG(tobs) FROM measurement WHERE date BETWEEN '{start_date}' AND '{end_date}'", conn)
    # Convert Data Frame to HTML
    tobs_cust_html = tobs_cust_df.to_html()

    return (tobs_cust_html)


if __name__ == '__main__':
    app.run(debug=True)