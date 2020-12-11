from flask import Flask, render_template, request
from chatbot.bot import getResponse
from db.models import Stop, Bus
from chatbot.utils.logger import log_chat

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("basic_index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    resp, tag, result = getResponse(userText)

    if tag == "stopInfo" and result is not None:
        stops = [st for st in Stop.query.filter_by(stop_names=result.stop_names).all()]
        bus_codes = [b.bus.line_id + ": " + b.bus.line_descr for st in stops for b in st.buses]
        resp = str(resp) + '<br/>' + ", ".join(bus_codes)
    if tag == "busRoute" and result is not None:
        buses = [bs for bs in Bus.query.filter_by(line_id=result.line_id).all()]
        stop_names = [s.stop.stop_names for bs in buses for s in bs.stops]
        resp = str(resp) + '<br/>' + ", ".join(stop_names)
    if tag == "busTime" and result is not None:
        for times in result:
            resp += '<br/>' + times

    log_chat(userText, resp)

    return str(resp)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5001)
