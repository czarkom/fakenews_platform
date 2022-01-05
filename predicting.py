import time

import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import websiteParser
from tensorflow import keras
from numpy import argmax
import json
import random


def predict_random(url, path_to_model):
    time.sleep(5)
    f = open('mocked_result.json')
    input_data = json.load(f)

    input_data['rating'] = random.randint(100, 500)/100
    return input_data


def predict_from_mock(url, path_to_model):
    f = open('mocked_result.json')
    input_data = json.load(f)
    input_data.pop('url')
    input_data['rating'] = predict_value(input_data, path_to_model)
    return input_data


def predict_from_parser(url, path_to_model):
    input_data = websiteParser.parse_website_js(url)
    input_data.pop('url')
    input_data['rating'] = predict_value(input_data, path_to_model)
    return input_data


def predict_value_binary(input_data, path_to_model):
    df = pd.DataFrame([input_data])
    normalized_df = (df) / float(df.max(axis=1))
    input = normalized_df.values
    model = keras.models.load_model(path_to_model)
    predicted_value = argmax(model.predict(input), axis=-1).astype('int')[0]
    return predicted_value

def predict_value_regression(input_data, path_to_model):
    df = pd.DataFrame([input_data])
    normalized_df = (df) / float(df.max(axis=1))
    input = normalized_df.values
    model = keras.models.load_model(path_to_model)
    predicted_value = model.predict(input.reshape(-1, 1, 40))*5.
    return predicted_value[0][0]


def recalculate_model(path_to_model, cursor):
    model = keras.models.load_model(path_to_model)
    cursor.execute("SELECT * FROM websites")
    dataset = cursor.fetchall()
    X, y = dataset[:, :-1], dataset[:, -1]
    history = model.fit(X, y, validation_split=0.33, epochs=150, batch_size=95)
    # tutaj może jakiś log z dokładnością
    model.save(path_to_model)
    learning_graph(history)


def learning_graph(history):
    # na wypadek jakby były metryki dokładności
    # plt.plot(history.history['accuracy'])
    # plt.plot(history.history['val_accuracy'])
    # plt.title('model accuracy')
    # plt.ylabel('accuracy')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    # plt.savefig('/graphs/acc_graph.png')
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('/graphs/loss_graph.png')
