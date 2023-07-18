# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text
import datetime as dt

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (f"Home page <br/>"
            f"Available Routes: <br/>"
            f"/api/v1.0/precipitation <br/>"
            f"/api/v1.0/stations <br/>"
            f"/api/v1.0/tobs")

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    return jsonify(session.query(measurement.date, measurement.prcp).\
            filter(measurement.date >= (dt.date(2017, 8, 23) - dt.timedelta(days=365))))

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    return jsonify(session.query(measurement.station).all())
    

@app.route("/api/v1.0/tobs")
def temperatures():
    print("Server received request for 'Temperatures' page...")
    return jsonify(session.query(measurement.tobs, func.count(measurement.tobs)).group_by(measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= (dt.date(2017, 8, 23) - dt.timedelta(days=365))))

@app.route("/api/v1.0/<start>")
def start_date(start_date):
    start = start_date.replace(" ", "").lower()
    for date in (session.query(measurement.date, measurement.tobs)):
        search_term = date["start_date"].replace(" ", "").lower()
        
        if search_term == date:
            return jsonify(start)
        
    return jsonify({"error": f"Date not found"}), 404

# @app.route("/api/v1.0/<start>/<end>")

if __name__ == "__main__":
    app.run(debug=True)