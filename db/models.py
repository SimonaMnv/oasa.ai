from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy import String

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
class Association(db.Model):
    __tablename__ = 'association_table'
    stops_id = db.Column(db.Integer, db.ForeignKey('stops_table.id'), primary_key=True)
    buses_id = db.Column(db.Integer, db.ForeignKey('buses_table.id'), primary_key=True)
    extra_data = db.Column(String(50))
    bus = relationship("Bus", back_populates="stops")
    stop = relationship("Stop", back_populates="buses")


class Stop(db.Model):
    __tablename__ = 'stops_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_code = db.Column(db.String(60), nullable=False)
    stop_codes = db.Column(db.String(60), unique=False)
    stop_names = db.Column(db.String(60), unique=False)
    buses = relationship("Association", back_populates="stop")

    def __repr__(self):
        return '<Stop %r>' % self.stop_codes


class Bus(db.Model):
    __tablename__ = 'buses_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    line_code = db.Column(db.String(20), nullable=False)
    line_id = db.Column(db.String(20), nullable=False)
    route_code = db.Column(db.String(60), nullable=False)
    line_descr = db.Column(db.String(60), nullable=False)
    stops = relationship("Association", back_populates="bus")

    def __repr__(self):
        return '<Bus %r>' % self.line_id


# create the initial database
db.create_all()
