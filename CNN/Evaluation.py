from CustomGenerator import getGenerator
from Params import *
from keras.models import load_model
import numpy as np
import sys
import os


# CNN Evaluation Class
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


size = nbatch  # the maximum test batch size


print("\nLoading the CNN model and weights.....")
model = load_model(modelPath)
model.load_weights(modelWeights)

print("Loading the test data.....")

# test generator creation
# test Data - 20% of the dataset
test_generator = getGenerator("Test")

count = 1
x_test, y_test = [], []
for ibatch, (x, y) in enumerate(test_generator):
    sys.stdout.write("\rBatch Progress: %d%%" % (count * 100 / size))
    sys.stdout.flush()
    count += 1
    x_test.append(x)
    y_test.append(y)
    ibatch += 1
    if ibatch == size:
        break

# gathering everything together
x_test = np.concatenate(x_test)
y_test = np.concatenate(y_test)
y_test = np.int32([np.argmax(r) for r in y_test])

# get the test predictions from the model and calculate the accuracy
print("\nget test data predictions.....")
y_pred = np.int32([np.argmax(r) for r in model.predict(x_test, verbose=1)])
match = (y_test == y_pred)
# displays the percentage of accuracy
accuracyInPercentage = 'Testing Accuracy = %.2f%%' % (np.sum(match) * 100 / match.shape[0])
print(accuracyInPercentage)

try:
    text_file = open(logFolder + "/TestAccuracy.txt", "w")
    text_file.write(accuracyInPercentage)
    text_file.close()
except OSError:
    pass
