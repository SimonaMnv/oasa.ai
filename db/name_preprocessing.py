from flask_sqlalchemy import SQLAlchemy
from db.app import app
from db.models import bus, stop
import sqlite3

db = SQLAlchemy(app)


# 1. Whenever "ΑΓ." or "ΣΤ." e.t.c are found as stop names, replace them with the full name
def convert():
    with sqlite3.connect("oasa.db") as con:
        c = con.cursor()
        c.execute("SELECT stop_names FROM stop")
        data = c.fetchall()

        # TODO: There are more
        for datum in data:
            converted = (datum[0].replace('ΠΛ.', 'ΠΛΑΤΕΙΑ').replace('ΣΤ.', 'ΣΤΑΘΜΟΣ').replace('Μ.', 'ΜΕΓΑΛΟΥ')
                         .replace('ΣΠ', 'ΣΠΥΡΟΥ').replace('ΙΔΡ. ΜΕΛ.', 'ΙΔΡΥΜΑ ΜΕΛΙΝΑ').replace('ΠΑΛ.', 'ΠΑΛΑΙΟ')
                         .replace('ΕΛ.', 'ΕΛΕΥΘΕΡΙΟΥ').replace('ΣΧ.', 'ΣΧΟΛΗ').replace('ΝΟΣΟΚ.', 'ΝΟΣΟΚΟΜΕΙΟ')
                         .replace('ΣΤΡ.', 'ΣΤΡΑΤΗΓΟΥ'))
            print(datum[0], "__", converted)

            # update db
            db.session.query(stop).filter(stop.stop_names == datum[0]).update({'stop_names': converted})
            db.session.commit()
            db.session.flush()


convert()
