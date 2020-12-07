import json
import numpy as np
import spacy
from fuzzywuzzy import fuzz
from nltk import word_tokenize
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chatbot.utils.utils import classify
import random
from db.models import Stop, db
from spacy.lang.el.stop_words import STOP_WORDS
from chatbot.utils.utils import strip_accents
import Levenshtein as lev

nlp = spacy.load('el_core_news_lg')
engine = create_engine('sqlite:///oasa.db')
Session = sessionmaker(bind=engine)
session = Session()

# Loading training data
training_data = []
training_data_file = 'data/training_dataGREEK.json'
with open(training_data_file, encoding='utf-8') as data_file:
    training_data = json.load(data_file)

# add JSON patterns in stop words
custom_stopwords = []
custom_stopwords.append(STOP_WORDS)
for intent in training_data['intents']:
    for pattern in intent['patterns']:
        w = nlp(strip_accents(pattern.lower()))
        for word in w:
            custom_stopwords.append(word)

# load our calculated synapse values
synapse_file = 'data/synapses.json'
with open(synapse_file) as data_file:
    synapse = json.load(data_file)
    synapse_0 = np.asarray(synapse['synapse0'])
    synapse_1 = np.asarray(synapse['synapse1'])
    words = synapse['words']
    classes = synapse['classes']

intents = json.loads(open('data/training_dataGREEK.json', encoding='utf-8').read())

excluded_pos = ["VERB", "SYM", "NUM", "ADP", "AUX", "ADV", "PRON"]


# calculate its response
def getResponse(msg):
    predict = classify(msg.lower(), synapse_0, synapse_1, words, classes, excluded_pos=excluded_pos)  # get class
    min = 19800

    # does usr_input belong to a class?
    if predict['probability']:
        tag = predict['probability'][0][0]  # take the class only (example : busStop, stopInfo e.t.c)
        list_of_intents = intents['intents']  # belongs to some class, get a random answer
        for i in list_of_intents:
            if i['class'] == tag:
                result = random.choice(i['responses'])
                # TODO: 1. Static info -- StopInfo class detected:
                if tag == 'stopInfo':
                    query = db.session.query(Stop.stop_names)
                    for stop_name in query:
                        # use a similarity metric to suggest a stop
                        # also, create custom stopwords list that has the default + all words from the JSON patterns
                        lev_distance = lev.distance(stop_name[0].lower(), predict['excluded_sentence'].lower())
                        if lev_distance < min:
                            min = lev_distance
                            min_name = stop_name[0]
                            print(min_name, min)
                            stop_result = min_name
                            if min == 0:
                                break
                return result + " " + stop_result, tag
    else:  # doesn't belong to any class
        result = "Χμμμ. Για ξαναπές το αυτό"
        tag = "None"
        return result, tag


# Probabilistic results -> testing reasons
print(classify("ποιο παει αγιο δημητριο", synapse_0, synapse_1, words, classes))

# STATIC:
# 1. poio lewforeio pernaei apo stash XXX  -> stopInfo
