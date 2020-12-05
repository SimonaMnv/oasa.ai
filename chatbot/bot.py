import json
import numpy as np
from fuzzywuzzy import fuzz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chatbot.utils.utils import classify
import random
from db.models import Stop, db

engine = create_engine('sqlite:///oasa.db')
Session = sessionmaker(bind=engine)
session = Session()

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

                    entity = " ".join([obj for term in predict['entities'] for obj in term if obj.islower()])
                    entity = entity if len(entity) > 0 else msg.lower()

                    query = db.session.query(Stop.stop_names)
                    for stop_name in query:
                        # find the name of the stop from db
                        if stop_name[0].lower() in msg.lower().split(" "):
                            result = result + " " + stop_name[0]
                            return result, tag
                        else:
                            # else, use a similarity metric to suggest a similar stop
                            # TODO: think about some way to filter out false positives (eg. ΡΙΟ / ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ)
                            stop_name_similarity = fuzz.partial_ratio(entity, stop_name[0].lower())
                            if stop_name_similarity > max:
                                max = stop_name_similarity
                                max_name = stop_name[0]
                                print(max_name, max)
                    result = result + " " + max_name

                return result, tag
    else:  # doesn't belong to any class
        result = "Χμμμ. Για ξαναπές το αυτό"
        tag = "None"
        return result, tag


# Probabilistic results -> testing reasons
print(classify("Ποιό περνάει απο την στάση πλ κανιγγος", synapse_0, synapse_1, words, classes))

# STATIC:
# 1. poio lewforeio pernaei apo stash XXX  -> stopInfo
