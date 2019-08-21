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
import boto3
import requests
from io import BytesIO


app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = './lib/inputimages'

model = None
graph = None

def qdload_model():
    global model
    global graph
    model = load_model("Quickdraw.h5")
    graph = K.get_session().graph

def prepareimage(filepath):
    

### OLD code when file is uploaded to local filesystem
    # image_size = (28, 28)
    # im = image.load_img(filepath, target_size=image_size, grayscale=True)

### New code when file is uploaded AWS S3 bucket.
    if filepath.startswith('https://'):
        response = requests.get(filepath)
        s3image = Image.open(BytesIO(response.content)).convert('L')
        im = s3image.resize((28, 28))


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

    qdload_model()
    
    result = {"success": False}
    if request.method == 'POST':

        reqpayload = request.get_data()
        reqparams= json.loads(reqpayload)

        # print(reqparams)
        
        data = base64.b64decode(reqparams["imagedata"])
    
        randomString = uuid.uuid4().hex # get a random string in a UUID fromat
        randomString  = randomString.upper()[0:8] # convert it in a uppercase letter and length 5 letters.

        filename = f"./lib/inputimages/{randomString}.png"
        s3filename = f"{randomString}.png"

        #### OLD code to save images to filesystem.
      
        # image_result = open(filename, "wb")
        # image_result.write(data)
        # image_result.close()


        ######## UPLOAD TO AWS S3 BUCKET #######

        S3_BUCKET = os.environ['S3_BUCKET']
        s3= boto3.resource('s3')
        s3.Bucket(S3_BUCKET).put_object(Key=s3filename, Body=data, ACL ='public-read')
        print("########### file uploaded to s3 successfully ###############")
        
        s3fileurl = f"https://doodlepredictionimages.s3-us-west-1.amazonaws.com/{s3filename}"

        image = prepareimage(s3fileurl)


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
