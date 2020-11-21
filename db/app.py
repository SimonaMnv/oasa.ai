import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


# print list
@app.route('/')
def hello_world():
    return 'i think it works'


@app.route('/list_bus')
def list_bus():
    with sqlite3.connect("oasa.db") as con:
        c = con.cursor()
        c.execute("SELECT * FROM bus")
        return render_template('list_bus.html', data=c.fetchall())


if __name__ == '__main__':
    app.run()
