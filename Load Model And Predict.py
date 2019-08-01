#!/usr/bin/env python
# coding: utf-8

# ## Load the Quickdraw model

# In[43]:


get_ipython().run_line_magic('matplotlib', 'inline')
from keras.models import load_model
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from PIL import Image
import io
import uuid
import numpy as np

import matplotlib.image as mpimg
from keras.applications.xception import (
    Xception, preprocess_input, decode_predictions)

import base64


# In[44]:


model = load_model("Quickdraw.h5")


# # Import a Custom Image

# In[68]:


manuallysaved = './lib/inputimages/9E8661F8.png'
image_size =(28,28)
im = image.load_img(manuallysaved, target_size=image_size,  grayscale=True)  #  from keras.preprocessing import image
originalsize = image.load_img(manuallysaved, grayscale=True)
im


# In[69]:


origarr = img_to_array(originalsize)
origarr.shape


# In[70]:


imgarr = img_to_array(im)
imgarr.shape


# In[71]:



# Flatten into a 1x28*28 array 
imgarr /= 255

# Flatten into a 1x28*28 array 
img = imgarr.flatten().reshape(-1,28,28,1)

img = 1 - img


# In[72]:


plt.imshow(img.reshape(28, 28), cmap=plt.cm.Greys)


# In[73]:


predictedclass = model.predict_classes(img)
predictedclass


# In[74]:


imgname = f"./static/qdimages/{predictedclass[0]}.png"
print(imgname)

img=mpimg.imread(imgname)
imgplot = plt.imshow(img)
plt.show()

