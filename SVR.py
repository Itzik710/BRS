from sklearn.svm import SVR
import numpy as np
from MySQL import *
import sys

# Fit the SVR model according to the given training data (All books that the user has read and rated)
#x_train = all of the books feature data
#y_train = all of the books rating data
def getUserRecommendedList(self,id):
    # list of [book filename, book features]
    allBooksFileNameAndFeatures = MySQL.getAllBooksFeatures("")
    # list of all user's attributes [book filename, book features,rating]
    userHistory = MySQL.getUserBooksFeatures("",id)
    # SVR model: kernel = Radial basis function
    clf = SVR(kernel="rbf", gamma=0.1, C=1.7, epsilon=0.2, verbose=1)
    # separate returned data from MySQL to 3 different lists
    userFilenames = [] # filenames according to the files in books package
    userFeatures = []
    userRatings = []
    for bookFilename in userHistory:
        userFilenames.append(bookFilename[0])
        userFeatures.append(ConvertFeatureVectorToFloatFormat(bookFilename[1]))
        userRatings.append(bookFilename[2])
    x_train = userFeatures
    y_train = userRatings
    # Train SVR model
    clf.fit(x_train, y_train)

    # collecting all books recommendations for a specific user (from a books which he doesn't read yet).
    predict = []
    for sample in allBooksFileNameAndFeatures:
        if sample[0] not in userFilenames :
            x_test = sample[1]
            x_test = ConvertFeatureVectorToFloatFormat(x_test)
            arr = []
            arr.append(x_test)
            v = clf.predict(arr)
            if sample[0] not in predict:
                predict.append([sample[0],v * 20])
    return predict


# convert features vector from string to float
def ConvertFeatureVectorToFloatFormat(featuresStringVector):
    featureFloatVector = []
    words = featuresStringVector.split(" ")
    for word in words:
        word = float(word)
        featureFloatVector.append(word)
    return featureFloatVector


