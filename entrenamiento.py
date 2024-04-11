import random
import json
import pickle
import numpy as np 

import nltk
from nltk.stem import WordNetLemartizer

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import sgd_experimental

lemmatizer = WordNetLemartizer()

intents = json.loads(open('intents.json').read())

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

words = []
classes = []
documents = []
ignore_letters = ['?','!','¿','.',',']

for intent in intents['intents']:
    for pattern in intent['intents']:
        words_list = nltk.word_tokenize(pattern)
        words.extend(words_list)
        documents.append((words_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes), open('classes.pkl', 'wb')

training = []
outoput_empty = [0]*len(classes)
for document in documents:
    bag = []
    word_pattenrs = document[0]
    word_pattenrs = [lemmatizer.lemmatize(word.lower()) for word in word_pattenrs]
    for word in words:
        bag.append(1) if word in word_pattenrs else bag.append(0)
    ouput_row = list(outoput_empty)
    ouput_row[classes.index(document[1])] = 1
    training.append([bag, ouput_row])
random.shuffle(training)
training = np.array(training)
print(training)

train_x = list(training[:,0])
train_y = list(train[:,1])

model = Sequential()
model.add(Dense(128, input_shape = (len(train_x[0]),), Activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, Activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), Activation = 'softmax'))

sgd = sgd_experimental.SGD(learning_rate=0.001, decay=1e-6, momentum=0.9, nesterov=True)