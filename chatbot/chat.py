from flask import Flask, render_template, request
from chatbot.bot import getResponse

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("basic_index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    resp, tag = getResponse(userText)
    return str(resp, tag)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)