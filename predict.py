from PIL import Image
from io import BytesIO
import cv2
import base64
from tqdm import tqdm
import urllib.request
from keras_preprocessing.sequence import pad_sequences
import numpy as np
import summarize
import requests


def predict(model, resnet, vocab, inv_vocab, data, count_api):
    max_len = 40

    loc = 'static/file.jpg'
    if 'call' not in data.keys():
        img = data['file'].split(',')[1]
        img = Image.open(BytesIO(base64.decodebytes(bytes(img, 'utf-8'))))
        img.save(loc)
    else:
        urllib.request.urlretrieve(
            data['data']['image_urls'],
            loc)

    print("="*50)
    print("IMAGE SAVED")

    image = cv2.imread('static/file.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = cv2.resize(image, (224, 224))

    image = np.reshape(image, (1, 224, 224, 3))

    incept = resnet.predict(image).reshape(1, 2048)

    print("="*50)
    print("Predict Features")

    text_in = ['startofseq']

    final = ''

    print("="*50)
    print("GETING Captions")

    count = 0
    while tqdm(count < 20):

        count += 1

        encoded = []
        for i in text_in:
            encoded.append(vocab[i])

        padded = pad_sequences(
            [encoded], maxlen=max_len, padding='post', truncating='post').reshape(1, max_len)

        sampled_index = np.argmax(model.predict([incept, padded]))

        sampled_word = inv_vocab[sampled_index]

        if sampled_word != 'endofseq':
            final = final + ' ' + sampled_word

        text_in.append(sampled_word)

    result = {'caption': final}

    # if 'article' in data['data'].keys():
    #     text = data['data']['article']
    #     description = summarize.text_summarize(text, count_api)
    #     result = {
    #         'caption': final,
    #         'description': description
    #     }
    return result
