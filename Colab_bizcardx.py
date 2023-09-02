!pip install easyocr
!pip install pymongo

import easyocr
from PIL import Image
import numpy as np
import pymongo

def image_to_text(path):
    img = Image.open(path)

    # Convert the PIL Image to a numpy array
    image_np = np.array(img)

    reader = easyocr.Reader(['en'])
    text = reader.readtext(image_np, detail=0, paragraph=True)
    return text

def store_mongodb(data):
  gopi = pymongo.MongoClient("mongodb+srv://gopiashokan:gopiroot@gopi.xdp3lkp.mongodb.net/?retryWrites=true&w=majority")
  db = gopi['bizcardx']
  col = db['image_data']
  col.insert_one(data)

def temp_collection_drop():
    gopi = pymongo.MongoClient("mongodb+srv://gopiashokan:gopiroot@gopi.xdp3lkp.mongodb.net/?retryWrites=true&w=majority")
    db = gopi['bizcardx']
    col = db.list_collection_names()
    if len(col) > 0:
        for i in col:
            db.drop_collection(i)

def text_to_mongodb(path):
  # extract data from image
  text = image_to_text(path)
  data = {'data':text}

  # delete existing data
  temp_collection_drop()

  # store extracted data
  store_mongodb(data)

text_to_mongodb('/content/1.png')