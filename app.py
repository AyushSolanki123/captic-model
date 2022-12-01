from itertools import count
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import cv2
from predict import predict
import summarize
from scrape import scrape_bbc, scrape_hitwada, scrape_toi
import base64
from keras.models import load_model
import numpy as np
from keras.applications import ResNet50
from keras.optimizers import Adam
from keras.layers import Dense, Flatten, Input, Convolution2D, Dropout, LSTM, TimeDistributed, Embedding, Bidirectional, Activation, RepeatVector, Concatenate
from keras.models import Sequential, Model
from keras.utils import np_utils
from keras.preprocessing import image, sequence
import cv2
from keras_preprocessing.sequence import pad_sequences
from tqdm import tqdm
import urllib.request

vocab = np.load('vocab.npy', allow_pickle=True)

vocab = vocab.item()

inv_vocab = {v: k for k, v in vocab.items()}


print("+"*50)
print("vocabulary loaded")


embedding_size = 128
vocab_size = len(vocab)
max_len = 40


image_model = Sequential()

image_model.add(Dense(embedding_size, input_shape=(2048,), activation='relu'))
image_model.add(RepeatVector(max_len))


language_model = Sequential()

language_model.add(Embedding(input_dim=vocab_size,
                   output_dim=embedding_size, input_length=max_len))
language_model.add(LSTM(256, return_sequences=True))
language_model.add(TimeDistributed(Dense(embedding_size)))


conca = Concatenate()([image_model.output, language_model.output])
x = LSTM(128, return_sequences=True)(conca)
x = LSTM(512, return_sequences=False)(x)
x = Dense(vocab_size)(x)
out = Activation('softmax')(x)
model = Model(inputs=[image_model.input, language_model.input], outputs=out)

model.compile(loss='categorical_crossentropy',
              optimizer='RMSprop', metrics=['accuracy'])

model.load_weights('mine_model_weights.h5')

print("="*150)
print("MODEL LOADED")

resnet = ResNet50(include_top=False, weights='imagenet',
                  input_shape=(224, 224, 3), pooling='avg')


# resnet = load_model('model.h5')

print("="*150)
print("RESNET MODEL LOADED")


app = Flask(__name__)
CORS(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
count_api = 0


@app.route('/', methods=['GET', 'POST'])
def after():

    global model, resnet, vocab, inv_vocab

    result = predict(model, resnet, vocab, inv_vocab, request.json, count_api)

    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/text')
def generate_text_summarization():
    text = request.json['text']
    caption = summarize.text_summarize(text, count_api)
    result = {
        'caption': caption,
        'length': len(caption)
    }
    return jsonify(result)


@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    url = request.json['url']
    website = request.json['website']
    err_msg = 'wrong URL entered'
    success_msg = 'Data scraped successfully'
    global model, resnet, vocab, inv_vocab, count_api

    if website == 'BBC':
        response = scrape_bbc(url)
        if response == None:
            result = {
                'error': err_msg
            }
        else:
            result = {
                'data': response,
                'message': success_msg
            }
    elif website == 'TOI':
        response = scrape_toi(url)
        if response == None:
            result = {
                'error': err_msg
            }
        else:
            result = {
                'data': response,
                'message': success_msg
            }
    else:
        response = scrape_hitwada(url)
        if response == None:
            result = {
                'error': err_msg
            }
        else:
            result = {
                'data': response,
                'message': success_msg
            }

    result['call'] = True
    data = predict(model, resnet, vocab, inv_vocab, result, count_api)
    result['predict'] = data
    result['data']['count'] = len(result['data']['image_alts'].split())
    count_api += 1
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    app.run(debug=True)
