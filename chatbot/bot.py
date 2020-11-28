import json
import numpy as np
from chatbot.utils.utils import classify
import random

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
    predict = classify(msg, synapse_0, synapse_1, words, classes)

    # does usr_input belong to a class?
    if predict['probability']:
        tag = predict['probability'][0][0]  # take the class only (example : busStop)

        list_of_intents = intents['intents']  # belongs to some class, get a random answer
        for i in list_of_intents:
            if i['class'] == tag:
                result = random.choice(i['responses'])
                return result, tag
    else:  # doesn't belong to any class
        result = "Χμμμ. Για ξαναπές το αυτό"
        tag = "None"
        return result, tag


# Probabilistic results -> testing reasons
print(classify("σε πόσο ρε γιαγια", synapse_0, synapse_1, words, classes))
