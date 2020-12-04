import unicodedata
import numpy as np
import spacy

nlp = spacy.load('el_core_news_lg')


# TODO: run once to install greek package (spacy v. 2.3.0)
# python -m spacy download el_core_news_lg


# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1 / (1 + np.exp(-x))
    return output


# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output * (1 - output)


def clean_up_sentence(sentence):
    # lemmatize sentence
    return [word.lemma_ for word in nlp(sentence)]


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)

    return np.array(bag)


def think(sentence, words, synapse_0, synapse_1, show_details=False):
    x = bow(sentence, words, show_details)
    if show_details:
        print("sentence:", sentence, "\n bow:", x)
    # input layer is our bag of words
    l0 = x
    # matrix multiplication of input and hidden layer
    l1 = sigmoid(np.dot(l0, synapse_0))
    # output layer
    l2 = sigmoid(np.dot(l1, synapse_1))
    return l2


def classify(sentence, synapse_0, synapse_1, words, classes, ERROR_THRESHOLD=0.2, show_details=False):
    sentence = strip_accents(sentence)
    results = think(sentence, words, synapse_0, synapse_1, show_details)

    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    # Sorting by keys (When there are more than one classification)
    results.sort(key=lambda x: x[1], reverse=True)
    probability = [[classes[r[0]], r[1]] for r in results]
    # print ("%s \n classification: %s" % (sentence, return_results))
    parsed_words = nlp(sentence)
    entities = [[entity.orth_, entity.ent_type_] for entity in parsed_words if entity.ent_type_]
    variables = [[entity.orth_, entity.dep_] for entity in parsed_words if entity.dep_ == 'dobj']
    return {"probability": probability, "entities": entities, "variables": variables}


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

