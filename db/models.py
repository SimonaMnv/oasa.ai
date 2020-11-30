from flask_sqlalchemy import SQLAlchemy
import os
from db.app import app
from sqlalchemy.orm import relationship

# dir of db
basedir = os.path.abspath(os.path.dirname(__file__))
baseDB = os.path.join(basedir, 'oasa.db')

# mostly to update the URI
app.config.update(
    SECRET_KEY='not-a-big-secret',
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
                            'sqlite:///' + baseDB,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)


# create the 2 tables. buses and stops have many:many relationship ->
# define a helper table that is used for the relationship
junction_table = db.Table('buses_stops',
    db.Column('stops_RouteCode', db.Integer, db.ForeignKey('stop.RouteCode'), primary_key=True),
    db.Column('buses_RouteCode', db.Integer, db.ForeignKey('bus.RouteCode'), primary_key=True)
)


class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RouteCode = db.Column(db.String(60), nullable=False)
    stop_codes = db.Column(db.String(60), unique=False)
    stop_names = db.Column(db.String(60), unique=False)
    bus = relationship("Bus", secondary=junction_table)

    def __repr__(self):
        return '<Stop %r>' % self.stop_codes


class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    LineCode = db.Column(db.String(20), nullable=False)
    LineID = db.Column(db.String(20), nullable=False)
    RouteCode = db.Column(db.String(60), nullable=False)
    LineDescr = db.Column(db.String(60), nullable=False)
    stop = relationship("Stop", secondary=junction_table)

    def __repr__(self):
        return '<Bus %r>' % self.LineID


# create the initial database
db.create_all()
