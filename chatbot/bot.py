import json
import numpy as np
import spacy
from nltk import word_tokenize
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chatbot.utils.utils import classify
import random
from db.models import Stop, db, Bus
from spacy.lang.el.stop_words import STOP_WORDS
from chatbot.utils.utils import strip_accents
import Levenshtein as lev
import re
from chatbot.oasa_api import oasa_bus_time

nlp = spacy.load('el_core_news_lg')
engine = create_engine('sqlite:///oasa.db')
Session = sessionmaker(bind=engine)
session = Session()

# Loading training data
training_data = []
training_data_file = 'data/training_dataGREEK.json'
with open(training_data_file, encoding='utf-8') as data_file:
    training_data = json.load(data_file)

stops = [word_tokenize(strip_accents(stop_name[0].lower())) for stop_name in db.session.query(Stop.stop_names)]
stops = [item for sublist in stops for item in sublist]
exclude_POS_sw = ["NUM"]

# add JSON patterns in stop words
custom_stopwords = [strip_accents(stop_word) for stop_word in STOP_WORDS if strip_accents(stop_word) not in stops]
for intent in training_data['intents']:
    for pattern in intent['patterns']:
        w = nlp(strip_accents(pattern.lower()))
        for word in w:
            custom_stopwords.append(str(word))

# load our calculated synapse values
synapse_file = 'data/synapses.json'
with open(synapse_file) as data_file:
    synapse = json.load(data_file)
    synapse_0 = np.asarray(synapse['synapse0'])
    synapse_1 = np.asarray(synapse['synapse1'])
    words = synapse['words']
    classes = synapse['classes']

intents = json.loads(open('data/training_dataGREEK.json', encoding='utf-8').read())


def stop_preprocessing():
    print("lala")


# calculate its response
def getResponse(msg):
    predict = classify(msg.lower(), synapse_0, synapse_1, words, classes)
    min = 19800
    min_stop = None
    flag = 0

    # does usr_input belong to a class?
    if predict['probability']:
        tag = predict['probability'][0][0]  # take the class only (example : busStop, stopInfo e.t.c)
        list_of_intents = intents['intents']  # belongs to some class, get a random answer
        for i in list_of_intents:
            if i['class'] == tag:
                result = random.choice(i['responses'])
                # TODO: 1. Static info -- StopInfo class detected: Return stop info
                if tag == 'stopInfo':
                    query = db.session.query(Stop)
                    text_tokens = word_tokenize(predict['excluded_sentence'].lower())
                    tokens_without_sw = " ".join([word for word in text_tokens if word not in custom_stopwords])
                    print("REMAINING SENTENCE 1:", tokens_without_sw)
                    for stop in query:
                        # use a similarity metric to suggest a stop, exclude some POS
                        # also, create custom stopwords list that has the default + all words from the JSON patterns
                        lev_distance = lev.distance(stop.stop_names.lower(), tokens_without_sw)
                        if lev_distance < min:
                            min = lev_distance
                            min_name = stop.stop_names
                            print(min_name, min)
                            stop_result = min_name
                            min_stop = stop
                            if min == 0:
                                break
                    return result + " " + stop_result, tag, min_stop
                # TODO: 2. Static info -- busRoute class detected: Return bus info
                if tag == 'busRoute':
                    query = db.session.query(Bus)
                    bus_id_format = re.findall(r'[α-ζ][0-9]{1,3}|[0-9]{1,3}|[0-9]{1,3}[α-ζ] ', msg.lower())
                    print("REMAINING SENTENCE 2:", bus_id_format)
                    for bus in query:
                        if bus.line_id in bus_id_format[0].upper() and bus_id_format[0].upper() in bus.line_id:
                            bus_result = bus_id_format[0].upper()
                            flag = 1
                            found_bus = bus
                    if flag == 0:
                        return "Δέν το ξέρω αυτό το λεωφορείο", tag, None
                    return result + " " + bus_result, tag, found_bus
                # TODO: 3. Dynamic (oasa_API) info -- busTime class detected: Return bus estimated time
                if tag == 'busTime':
                    query_bus = db.session.query(Bus)
                    bus_id_format = re.findall(r'[α-ζ][0-9]{1,3}|[0-9]{1,3}|[0-9]{1,3}[α-ζ] ', msg.lower())
                    for bus in query_bus:
                        if bus.line_id in bus_id_format[0].upper() and bus_id_format[0].upper() in bus.line_id:
                            route_code = bus.route_code
                    bus_times = oasa_bus_time(route_code)
                    return result + " " + bus_id_format[0] + " ", tag, bus_times
                return "Δέν ξέρω σε πόσο θα έρθει αυτό το λεωφορείο", tag, None
    else:  # doesn't belong to any class
        result = "Χμμμ. Για ξαναπές το αυτό"
        tag = "None"
        return result, tag, None


# Probabilistic results -> testing reasons (this doesnt have cust_sw in it yet)
print(classify("σε ποσο ερχεται το β12", synapse_0, synapse_1, words, classes))
