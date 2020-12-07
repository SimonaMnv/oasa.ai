import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'i think it works'


@app.route('/list_bus')
def list_bus():
    with sqlite3.connect("oasa.db") as con:
        c = con.cursor()
        c.execute("SELECT * FROM buses_tables")
        return render_template('list_bus.html', data=c.fetchall())


@app.route('/list_stop')
def list_stop():
    with sqlite3.connect("oasa.db") as con:
        c = con.cursor()
        c.execute("SELECT * FROM stops_table")
        return render_template('list_stops.html', data=c.fetchall())


@app.route('/list_buses_stops')
def list_stops_buses():
    with sqlite3.connect("oasa.db") as con:
        c = con.cursor()
        c.execute("SELECT * FROM association_table")
        return render_template('list_buses_stops.html', data=c.fetchall())


if __name__ == '__main__':
    app.run(port=5002)
