from flask import Flask, render_template, request
from chatbot.bot import getResponse
from db.models import Stop

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("basic_index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    resp, tag, stop = getResponse(userText)
    if stop is not None:
        stops = [st for st in Stop.query.filter_by(stop_names=stop.stop_names).all()]
        bus_codes = [b.bus.line_id + ": " + b.bus.line_descr for st in stops for b in st.buses]
        resp = str(resp) + " είναι παιδάκι μου πολλά, να πχ: " + ", ".join(bus_codes)
        resp += ", αλλά μεγάλη γυναίκα είμαι, μπορεί να ξεχνάω τίποτα"
    return str(resp)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5001)