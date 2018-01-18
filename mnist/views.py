from django.shortcuts import render_to_response,render, redirect
import keras
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.misc import imsave, imread, imresize
import tensorflow as tf
import io
from django.core.files.base import ContentFile
import numpy as np
import os
from keras.models import model_from_json

from .forms import ImageData

from mnist.forms import ImageData

#opening saved model and compiling it before loading the view
json_file = open('./model/model.json','r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("./model/model.h5")
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
graph = tf.get_default_graph()

def home(request):
    prediction = ""
    if request.method == 'POST':
        form = ImageData(request.POST)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            prediction = predict(image)     
    else:
        form = ImageData()
    return render(request, "alwin.html", {'form':form, 'prediction': prediction})

def predict(image): #The prediction function, it feeds image to the model and it predicts
    convertImage(image)
    x = imread('alwin.png',mode='L')
    
    x = np.invert(x)
    
    x = imresize(x,(28,28))

    x = x.reshape(1,28,28,1)

    with graph.as_default():
        result = model.predict(x)
        return np.argmax(result,axis=1)

def convertImage(data): #function to convert canvas image from base64 string to a .png file
    i = base64.b64decode(data)
    i = io.BytesIO(i)
    i = mpimg.imread(i, format='JPG')

    plt.imshow(i, interpolation='nearest')
    plt.axis('off')
    plt.savefig('alwin.png')
    plt.close()
    
    