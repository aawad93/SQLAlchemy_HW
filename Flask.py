import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<end>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/percipitation")
def percipitation():
    """the last 12 months of precipitation"""
    # Query percipitation data
    session = Session(engine)
    prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-18')
    
  # Create a dictionary from the row data and append to a list
    prcp_data = []
    for date, p in prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = p
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    """all stations"""
    # Query all stations
    stations = session.query(Station.station).all()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """the last 12 months of temperatures recorded"""
    # Query tobs data
    session = Session(engine)
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-18')
    
  # Create a dictionary from the row data and append to a list of all_passengers
    tobs_data = []
    for date, t in tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = t
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start_date_query(start):
    """Fetch the temperature data from start date"""
    start_date = start.replace("/","-").replace(" ","-")
    tobs_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date)

    return jsonify(tobs_start)

@app.route("/api/v1.0/<end>")
def start_date_query(end):
    """Fetch the temperature data from start date"""
    end_date = end.replace("/","-").replace(" ","-")
    tobs_end = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date <= end_date)

    return jsonify(tobs_end)

@app.route("/api/v1.0/<start>/<end>")
def start_date_query(start, end):
    """Fetch the temperature data from start date"""
    start_date = start.replace("/","-").replace(" ","-")
    end_date = end.replace("/","-").replace(" ","-")
    tobs_custom = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)

    return jsonify(tobs_custom)


if __name__ == '__main__':
    app.run(debug=True)