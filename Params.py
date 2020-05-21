import os

# Project main parameters Class

projectName = 'finalProject'

modelPath = 'Model/cnn_model.h5'
modelWeights = 'Model/cnn_weights.h5'

# number of train samples - a 70% from the dataset
num_train_samples = 424
# number of validation samples - a 10% from the dataset
num_valid_samples = 61
# number of test samples - a 20% from the dataset
num_test_samples = 122

# batch size
batch_size = 32
# HyperParams
nbatch = 32  # 32 default. Number of samples to propagate each epoch.
# learn rate
learnRate = 0.001

# number of classes - in our case the number of authors(106 different authors)
number_of_classes = 106

# Log folder to save weights and training graphs.
logFolder = "ModelGraphs"
try:
    os.makedirs(logFolder)
except OSError:
    pass