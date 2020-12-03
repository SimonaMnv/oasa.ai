from flask_sqlalchemy import SQLAlchemy
from db.app import app
from db.models import Stop
import sqlite3
import regex as re

db = SQLAlchemy(app)


def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail


# 1. Whenever "ΑΓ." or "ΣΤ." e.t.c are found as stop names, replace them with the full name
def convert():
    with sqlite3.connect("oasa.db") as con:
        c = con.cursor()
        c.execute("SELECT stop_names FROM stops_table")
        data = c.fetchall()

        for datum in data:
            # 1. general conversion
            converted = (datum[0].replace('ΠΛ.', 'ΠΛΑΤΕΙΑ').replace('ΣΤ.', 'ΣΤΑΘΜΟΣ').replace('Μ.', 'ΜΕΓΑΛΟΥ')
                                 .replace('ΣΠ', 'ΣΠΥΡΟΥ').replace('ΙΔΡ. ΜΕΛ.', 'ΙΔΡΥΜΑ ΜΕΛΙΝΑ').roasaeplace('ΠΑΛ.',
                                                                                                        'ΠΑΛΑΙΟ')
                                 .replace('ΕΛ.', 'ΕΛΕΥΘΕΡΙΟΥ').replace('ΣΧ.', 'ΣΧΟΛΗ').replace('ΝΟΣΟΚ.', 'ΝΟΣΟΚΟΜΕΙΟ')
                                 .replace('ΣΤΡ.', 'ΣΤΡΑΤΗΓΟΥ'))
            print(datum[0], "__", converted)
    
            # 2. "- ΟΣ" suffix conversion
            k = re.search("[ΟΣ]{2}$", datum[0])  # match last 2 characters
            if k:
                # converted = replace_last(datum[0], 'ΑΓ.', 'ΑΓΙΟΣ')
                converted = (datum[0].replace('ΑΓ.', 'ΑΓΙΟΣ'))
                print(datum[0], "__", converted)

            # 3. "- Α" suffix conversion
            k = re.search("[A]{1}$", datum[0])  # match last 1 characters
            if k:
                converted = (datum[0].replace('ΑΓ.', 'ΑΓΙΑ'))
                print(datum[0], "__", converted)

            # update db
            db.session.query(Stop).filter(Stop.stop_names == datum[0]).update({'stop_names': converted})
            db.session.commit()
            db.session.flush()


convert()
