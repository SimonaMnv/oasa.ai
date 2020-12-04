from flask_sqlalchemy import SQLAlchemy
from db.app import app
import sqlite3
import regex as re
from db.models import Stop

db = SQLAlchemy(app)


def convert():
    with sqlite3.connect("oasa.db") as con:
        c = con.cursor()
        c.execute("SELECT stop_names FROM stops_table")
        data = c.fetchall()

        for datum in data:
            flag = 0

            # general conversions
            converted = (datum[0].replace('ΠΛ.', 'ΠΛΑΤΕΙΑ').replace('ΣΤ.', 'ΣΤΑΘΜΟΣ').replace('Μ.', 'ΜΕΓΑΛΟΥ')
                         .replace('ΣΠ.', 'ΣΠΥΡΟΥ').replace('ΙΔΡ. ΜΕΛ.', 'ΙΔΡΥΜΑ ΜΕΛΙΝΑ').replace('ΠΑΛ.', 'ΠΑΛΑΙΟ')
                         .replace('ΕΛ.', 'ΕΛΕΥΘΕΡΙΟΥ').replace('ΣΧ.', 'ΣΧΟΛΗ').replace('ΝΟΣΟΚ.', 'ΝΟΣΟΚΟΜΕΙΟ')
                         .replace('ΣΤΡ.', 'ΣΤΡΑΤΗΓΟΥ').replace('ΖΩΟΔ.', 'ΖΩΟΔΟΧΟΥ ').replace('ΠΡΑΚΤ.', 'ΠΡΑΚΤΟΡΕΙΟ')
                         .replace('ΟΙΚΟΛ.', 'ΟΙΚΟΛΟΓΙΚΟ ').replace('ΠΑΛΑΙΟ.', 'ΠΑΛΑΙΟ ').replace('ΝΙΚ.', 'ΝΙΚΟΛΑΟΥ ')
                         .replace('ΕΘΝ.', 'ΕΘΝΙΚΗ').replace('ΓΕΩΡ.', 'ΓΕΩΡΓΙΟΥ').replace('ΚΩΝ', 'ΚΩΝΣΤΑΝΤΙΝΟΥ')
                         .replace('ΑΘ.', 'ΑΘΑΝΑΣΙΟΥ ').replace('ΜΕΓ.', 'ΜΕΓΑ').replace('ΠΛ  ', 'ΠΛΑΤΕΙΑ ')
                         .replace('ΝΟΣ.', 'ΝΟΣΟΚΟΜΕΙΟ').replace('ΑΓ .', 'ΑΓΙΟΣ '))
            db.session.query(Stop).filter(Stop.stop_names == datum[0]).update({'stop_names': converted})

            # "-Α + -ΑΣ + -Η"
            k = re.search("[Α]{1}$", datum[0])
            k1 = re.search("[ΑΣ]{2}$", datum[0])
            k2 = re.search("[Η]{1}$", datum[0])
            if k or k1 or k2:
                flag = 1
                converted = (datum[0].replace('ΑΓ.', 'ΑΓΙΑ'))
                db.session.query(Stop).filter(Stop.stop_names == datum[0]).update({'stop_names': converted})

            # "-ΡΩΝ"
            k = re.search("[ΡΩΝ]{3}$", datum[0])
            if k and flag == 0:
                flag = 1
                converted = (datum[0].replace('ΑΓ.', 'ΑΓΙΩΝ'))
                db.session.query(Stop).filter(Stop.stop_names == datum[0]).update({'stop_names': converted})

            # "-ΟΣ"
            k = re.search("[ΟΣ]{2}$", datum[0])  # match last 2 characters
            k1 = re.search("[ΩΝ]{2}$", datum[0])
            k2 = re.search("[ΗΣ]{2}$", datum[0])
            if (k or k1 or k2) and flag == 0:
                flag = 1
                converted = (datum[0].replace('ΑΓ.', 'ΑΓΙΟΣ'))
                db.session.query(Stop).filter(Stop.stop_names == datum[0]).update({'stop_names': converted})

            # "-OI"
            k = re.search("[ΟΙ]{2}$", datum[0])
            k1 = re.search("[ΕΣ]{2}$", datum[0])
            if (k or k1) and flag == 0:
                converted = (datum[0].replace('ΑΓ.', 'ΑΓΙΟΙ'))
                db.session.query(Stop).filter(Stop.stop_names == datum[0]).update({'stop_names': converted})

            # "-ΟΥ"
            k = re.search("[ΟΥ]{2}$", datum[0])
            if k and flag == 0:
                converted = (datum[0].replace('ΑΓ.', 'ΑΓΙΟΥ'))
                db.session.query(Stop).filter(Stop.stop_names == datum[0]).update({'stop_names': converted})

        db.session.commit()
        db.session.flush()


convert()
