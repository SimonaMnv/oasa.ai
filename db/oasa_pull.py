import requests
from flask_sqlalchemy import SQLAlchemy
from db.app import app
from db.models import bus, stop

# connect to OASA API
responseINFO = requests.post("http://telematics.oasa.gr/api/?act=webGetLines")
json_response = responseINFO.json()

db = SQLAlchemy(app)


# fill up the bus table with info from the OASA API
def fill_bus():
    for resp in json_response:
        record = bus(LineCode=resp['LineCode'], LineID=resp['LineID'], LineDescr=resp['LineDescr'])
        db.session.add(record)
        db.session.commit()

# TODO: fill up the stops table
