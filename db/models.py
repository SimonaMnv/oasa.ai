from flask_sqlalchemy import SQLAlchemy
import os
from db.app import app

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


# create our 2 tables
class bus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    LineCode = db.Column(db.String(20), nullable=False)
    LineID = db.Column(db.String(20), nullable=False)
    LineDescr = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<Bus %r>' % self.LineID


class stop(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stop_code = db.Column(db.String(60), unique=False, nullable=False)
    stop_names = db.Column(db.String(60), unique=False, nullable=False)

    def __repr__(self):
        return '<Stop %r>' % self.stop_code


# create the initial database
db.create_all()


# TODO: a third table (union) that has One-to-Many Relationship [1 Bus : N Stops]
