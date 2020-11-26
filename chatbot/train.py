import numpy as np
import json
import spacy
import time

from chatbot.brain import train
from chatbot.utils import utils

nlp = spacy.load('el_core_news_lg')

# Loading training data
training_data = []
training_data_file = 'data/training_dataGREEK.json'
with open(training_data_file, encoding='utf-8') as data_file:
    training_data = json.load(data_file)

words = []
classes = []
documents = []
ignore_words = ['?', '!', ';', '-PRON-']
# loop through each sentence in our training data
for intent in training_data['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = nlp(utils.strip_accents(pattern))
        # Stemming and removing words
        # add to our words list
        lemmas = [w1.lemma_ for w1 in w if w1.lemma_ not in ignore_words]
        words.extend(lemmas)
        # add to documents in our corpus
        documents.append(([w1.orth_ for w1 in w], lemmas, intent['class']))
        # add to our classes list
        if intent['class'] not in classes:
            classes.append(intent['class'])

# remove duplicates
print(words)
words = list(set(words))

# remove duplicates
classes = list(set(classes))

# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of lemmatized words for the pattern
    pattern_words = doc[1]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    training.append(bag)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[2])] = 1
    output.append(output_row)

X = np.array(training)
y = np.array(output)

start_time = time.time()

train(X, y, classes, words, hidden_neurons=25, alpha=0.1, epochs=250000, dropout=False, dropout_percent=0.2)

elapsed_time = time.time() - start_time
print("processing time:", elapsed_time, "seconds")
