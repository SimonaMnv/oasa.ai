import requests


def oasa_bus_time(routecode):
    # take stop code
    responseSTOPCODE = requests.post("http://telematics.oasa.gr/api/?act=webGetStops&p1=" + str(routecode))
    json_response2 = responseSTOPCODE.json()
    stop_codes = []
    stop_names = []
    for sc in json_response2:
        stop_codes.append(sc['StopCode'])  # each stop has a stop code
        stop_names.append(sc['StopDescr'])  # for each stop code we have a stop name

    time_results = []
    # take real time arrival
    for stop_code, stop_name in zip(stop_codes, stop_names):
        responseBUSTIME = requests.post("http://telematics.oasa.gr/api/?act=getStopArrivals&p1=" + str(stop_code))
        json_response3 = responseBUSTIME.json()

        if json_response3 is not None:
            time_results.append(stop_name + " σε: " + json_response3[0]['btime2'] + " λεπτά")

    return time_results
