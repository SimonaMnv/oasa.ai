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


# calculate its response
def getResponse(msg):
    predict = classify(msg.lower(), synapse_0, synapse_1, words, classes)  # get class
    max = 0

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
                        text_tokens = word_tokenize(msg)
                        tokens_without_sw = " ".join([word for word in text_tokens if not word in str(custom_stopwords)])
                        stop_name_similarity = fuzz.partial_ratio(tokens_without_sw.lower(), stop_name[0].lower())
                        if stop_name_similarity > max:
                            max = stop_name_similarity
                            max_name = stop_name[0]
                            print(max_name, max)
                            stop_result = max_name
                            if max == 100:
                                break
                return result + " " + stop_result, tag
    else:  # doesn't belong to any class
        result = "Χμμμ. Για ξαναπές το αυτό"
        tag = "None"
        return result, tag


# Probabilistic results -> testing reasons
print(classify("Ποιό περνάει απο την στάση πλ κανιγγος", synapse_0, synapse_1, words, classes))

# STATIC:
# 1. poio lewforeio pernaei apo stash XXX  -> stopInfo
