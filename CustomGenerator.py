import os
import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from keras.utils import np_utils, to_categorical
from Params import number_of_classes, projectName
from Params import batch_size


# load samples of a set( train, valid , test)
# get the path to 'data_files' package and the type of set(csv file) to load from this package
from utils import get_project_root


def load_samples(home,csv_file):
    data = pd.read_csv(os.path.join(home,csv_file))
    data = data[['FileName', 'Label', 'ClassName']]
    file_names = list(data.iloc[:,0])
    # Get the labels present in the second column
    labels = list(data.iloc[:,1])
    samples=[]
    for samp,lab in zip(file_names,labels):
        samples.append([samp,lab])
    return samples



# Custom generator - Yields the next batch.
# samples are in array [[book1_filename,label1], [book2_filename,label2],...].
# return a generator according to the type of set(train, valid, test)
def generator(samples, batch_size,root_dir, shuffle_data=True, resize = 224):
    num_samples = len(samples)
    while True:  # Loop forever so the generator never terminates
        # shuffle the samples
        samples = shuffle(samples)
        # Get index to start each batch: [0, batch_size, 2*batch_size, ..., max multiple of batch_size <= num_samples]
        for offset in range(0, num_samples, batch_size):
            # Get the samples which will be use in this batch
            batch_samples = samples[offset:offset + batch_size]
            # init X_train and y_train arrays for this batch
            X_train = []
            y_train = []
            # For each batch sample
            for batch_sample in batch_samples:
                # Load book filename (X) and label (y)
                bookFilename = batch_sample[0]
                label = batch_sample[1]
                f = open(os.path.join(root_dir, bookFilename))
                lines = f.readlines()
                arr = []
                for line in lines:
                    words = line.split()
                    for w in words:
                        arr.append(w)
                # apply any kind of preprocessing
                # Add batch sample to arrays
                X_train.append(arr)
                y_train.append(label)
                # assign a label for each sample
                train_labels = to_categorical(y_train,num_classes=number_of_classes)

            # Make sure they're numpy arrays (as opposed to lists)
            X_train = np.array(X_train)
            y_train = np.array(train_labels)
            # The generator part: yield the next training batch
            yield X_train, y_train



train_data_path = 'books_recognition_train.csv'
valid_data_path = 'books_recognition_valid.csv'
test_data_path = 'books_recognition_test.csv'
extract_data_path = 'books_recognition.csv'


# a function that gets a  string of set type(train, valid , test), and return a custom generator according to this type
def getGenerator(setType):
    # Create generator for each type of set (training, test, validation)
    root_dir = bla = get_project_root()
    root_dir = str(root_dir)
    root_dir = root_dir + "\\" + projectName
    if setType == "Train":
        train_generator = generator(load_samples('data_files',train_data_path),batch_size, root_dir)
        return train_generator
    elif setType == "Valid":
        valid_generator = generator(load_samples('data_files',valid_data_path),batch_size, root_dir)
        return valid_generator
    elif setType == "Test":
        test_generator = generator(load_samples('data_files',test_data_path),batch_size, root_dir)
        return test_generator
    elif setType == "AllBooks":
        extract_generator = generator(load_samples('data_files', extract_data_path), 1, root_dir)
        return extract_generator
    else:
        return "Invalid Input of set type"


