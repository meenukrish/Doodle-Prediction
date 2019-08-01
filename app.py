import os
from flask import Flask, jsonify, render_template, request, redirect
import base64
import uuid
import json


import tensorflow as tf 
from keras.models import load_model
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from keras import backend as K
from PIL import Image
import io


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './lib/inputimages'

model = None
graph = None

def qdload_model():
    global model
    global graph
    model = load_model("Quickdraw.h5")
    graph = K.get_session().graph

def prepareimage(filepath):
    
    image_size = (28, 28)
    im = image.load_img(filepath, target_size=image_size, grayscale=True)
             
    imagearr = img_to_array(im)
    # imagearr.shape

    # Flatten into a 1x28*28 array 
    imagearr /= 255

    # Flatten into a 1x28*28 array 
    img = imagearr.flatten().reshape(-1, 28,28,1)

    # img.shape

    img = 1 - img

    return img


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/slides")
def slides():
    """Return the homepage."""
    return render_template("slides.html")


@app.route("/predict", methods=['GET', 'POST'])
def predictimage():
    result = {"success": False}
    if request.method == 'POST':

        reqpayload = request.get_data()
        reqparams= json.loads(reqpayload)

        # print(reqparams)
        
        data = base64.b64decode(reqparams["imagedata"])
    
        randomString = uuid.uuid4().hex # get a random string in a UUID fromat
        randomString  = randomString.upper()[0:8] # convert it in a uppercase letter and length 5 letters.

        filename = f"./lib/inputimages/{randomString}.png"

        image_result = open(filename, "wb")
        image_result.write(data)
        image_result.close()

        image = prepareimage(filename)

        global model
        global graph
        with graph.as_default():
            predictedclass = model.predict_classes(image)
            # predictedclass
            category = str(predictedclass[0])

            print("******************")
            print(f"Returned category: {category}")
            print("******************")

            result["category"] =  category
            result["success"] = True
        
        return jsonify(result)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
    qdload_model()
    app.run(debug=True)
