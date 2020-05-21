from keras import Model
import numpy as np

import Params
from CustomGenerator import getGenerator
from Params import *
from keras.models import load_model
import sys
import pandas as pd

from utils import get_project_root

"""
    # Features extraction Class
    once the CNN model is trained and achieved a good accuracy,  we extract features from the fully connected layer
    (before the output layer) and use them for another task (book recommendation)
"""

# loads model and weights
model = load_model(modelPath)
model.load_weights(modelWeights)

# Feed forward over the CNN model - gets the fully connected layer parameters
intermediate_layer_model = Model(inputs=model.input, outputs=model.get_layer('fullyConnetcted').output)

# intermediate_layer_model.summary()

# creates generator which contains all books
all_types_generator = getGenerator("allTypes")


# gathers the books text and labels - in order to concatenate all books together before we feed forward our model
'''
input: generator - all books generator , size = size of books in dataset
output: list of all books text, list of all books labels    
'''
def gathersBooksTogether(generator, size):
    count = 1
    x_extract, y_extract = [], []
    for ibatch, (x, y) in enumerate(generator):
        sys.stdout.write("\rBatch Progress: %d%%" % (count * 100 / size))
        sys.stdout.flush()
        count += 1
        x_extract.append(x)
        y_extract.append(y)
        ibatch += 1
        if ibatch == size:
            break
    # Concatenate everything together
    x_extract = np.concatenate(x_extract)
    y_extract = np.concatenate(y_extract)
    y_extract = np.int32([np.argmax(r) for r in y_extract])
    return x_extract, y_extract


# we take Victor feauture from  each book
extract_generator = getGenerator("AllBooks")
x_extract, y_extract = gathersBooksTogether(extract_generator, 607)

# gets a matrix where each row represents a book and his features vector
feauture_engg_data = intermediate_layer_model.predict(x_extract, verbose=0)

# selects the dominant features from each book
feauture_engg_data = pd.DataFrame(feauture_engg_data)
selected_cnn_fea_cols = [3, 4, 7, 13, 18, 22, 35, 37, 41, 44, 45, 48, 49, 55, 59, 65, 68, 69, 70, 71, 73, 74, 76, 78,
                         80, 83, 84, 87, 89, 90, 99, 104, 109, 111, 112, 113, 114, 119, 120, 122, 124]
X_arr = np.array(feauture_engg_data)
X = X_arr[:, selected_cnn_fea_cols]

# save books features extraction
root = get_project_root()
root = str(root)
w = open(root + "\\" + Params.projectName + "\\data_files\\" +  "\\feature_extraction.txt" , 'w')
for line in X:
    i = 0
    for num in line:
        w.write(str(num) + " ")
    w.write('\n')
y = np.array(y_extract)



