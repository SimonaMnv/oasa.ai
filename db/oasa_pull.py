import requests
from flask_sqlalchemy import SQLAlchemy
from db.app import app
from db.models import Bus, Stop, Association

# connect to OASA API -> this API returns LineCode, LineID, LineDescr
responseINFO = requests.post("http://telematics.oasa.gr/api/?act=webGetLines")
json_response = responseINFO.json()

db = SQLAlchemy(app)


# fill up the stops table with info from the OASA API
def fill_stops():
    for resp in json_response:
        # Take the routecode, need linecode for that
        routecodeResponse = requests.post(
            "http://telematics.oasa.gr/api/?act=webGetRoutes&p1=" + resp['LineCode']).json()
        routecode = routecodeResponse[0]['RouteCode']

        # take stop codes and names, need routecode for that. One to many
        responseStopCode = requests.post("http://telematics.oasa.gr/api/?act=webGetStops&p1=" + str(routecode)).json()
        for sc in responseStopCode:
            stop_codes = (sc['StopCode'])  # each stop has a stop code
            stop_names = (sc['StopDescr'])  # for each stop code we have a stop name

            record = Stop(route_code=routecode, stop_codes=stop_codes, stop_names=stop_names)  # change to bulk insert
            db.session.add(record)
            db.session.commit()


# fill up the bus table with info from the OASA API
def fill_bus():
    for resp in json_response:
        # Take the routecode too, need linecode for that
        routecodeResponse = requests.post(
            "http://telematics.oasa.gr/api/?act=webGetRoutes&p1=" + resp['LineCode']).json()
        routecode = routecodeResponse[0]['RouteCode']

        record = Bus(line_code=resp['LineCode'], line_id=resp['LineID'], line_descr=resp['LineDescr'],
                     route_code=routecode)

        db.session.add(record)
        db.session.commit()

        fill_associations(record)


def fill_associations(bus):
    [insert_association(bus, stop) for stop in Stop.query.filter_by(route_code=bus.route_code).all()]


def insert_association(bus, stop):
    assoc = Association()
    assoc.buses_id = bus.id
    assoc.stops_id = stop.id
    db.session.add(assoc)
    db.session.commit()


# fill bus and stop tables
fill_stops()
fill_bus()

# # TODO: fill the bidirectional many:many relationship
# b = Bus()
# a = Association(extra_data="some data")
# a.stop = Stop()
# b.stops.append(a)
