import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import websiteParser
from tensorflow import keras

def predictValue(url, path_to_model):
    input_data = websiteParser.parse_website_js(url)
    model = keras.models.load_model(path_to_model)
    predicted_value = model.predict(input_data)
    return predicted_value

def recalculateModel(path_to_model, cursor):
    model = keras.models.load_model(path_to_model)
    cursor.execute("SELECT * FROM websites")
    dataset = cursor.fetchall()
    X, y = dataset[:,:-1], dataset[:,-1] 
    history = model.fit(X, y, validation_split=0.33, epochs=150, batch_size=95)
    #tutaj może jakiś log z dokładnością
    model.save(path_to_model)
    learningGraph(history)

def learningGraph(history):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('/graphs/acc_graph.png')
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('/graphs/loss_graph.png')