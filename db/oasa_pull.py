import requests
from flask_sqlalchemy import SQLAlchemy
from db.app import app
from db.models import bus, stop

# connect to OASA API -> this API returns LineCode, LineID, LineDescr
responseINFO = requests.post("http://telematics.oasa.gr/api/?act=webGetLines")
json_response = responseINFO.json()

db = SQLAlchemy(app)


# fill up the bus table with info from the OASA API
def fill_bus():
    for resp in json_response:
        # Take the routecode too, need linecode for that
        routecodeResponse = requests.post(
            "http://telematics.oasa.gr/api/?act=webGetRoutes&p1=" + resp['LineCode']).json()
        routecode = routecodeResponse[0]['RouteCode']

        record = bus(LineCode=resp['LineCode'], LineID=resp['LineID'], LineDescr=resp['LineDescr'], RouteCode=routecode)
        db.session.add(record)
        db.session.commit()


# fill up the stops table with info from the OASA API
def fill_stops():
    for resp in json_response:
        # Take the routecode, need linecode for that
        routecodeResponse = requests.post("http://telematics.oasa.gr/api/?act=webGetRoutes&p1=" + resp['LineCode']).json()
        routecode = routecodeResponse[0]['RouteCode']

        # take stop codes and names, need routecode for that. One to many
        responseStopCode = requests.post("http://telematics.oasa.gr/api/?act=webGetStops&p1=" + str(routecode)).json()
        for sc in responseStopCode:
            stop_codes = (sc['StopCode'])   # each stop has a stop code
            stop_names = (sc['StopDescr'])  # for each stop code we have a stop name

            record = stop(RouteCode=routecode, stop_codes=stop_codes, stop_names=stop_names)   # change to bulk insert
            db.session.add(record)
            db.session.commit()


# fill db
fill_bus()
fill_stops()
