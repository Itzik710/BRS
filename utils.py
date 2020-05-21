from pathlib import Path
# import os
# import string
# from nltk.corpus import stopwords
# import numpy
# from keras.preprocessing.text import one_hot
# from keras_preprocessing.sequence import pad_sequences

# get the project root folder
def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent

#
#
#
# # Removes POS(part of speech tagging) from all of the books files
# # in order to use this function, enter your own folders names.
# def removePos(directory):
#     for file in os.listdir(directory):
#         readFilename = str(file.title(),'utf-8')
#         writeFilename= readFilename[:-10]
#         with open("<Directory>// + readFilename", 'r') as f:
#             with open("<New Directory>// + writeFilename", 'w') as w:
#                 lines = f.readlines()
#                 for line in lines:
#                     if '@' in line:
#                         continue
#                     w.write(" ".join(word.split("/")[0] for word in line.split()))
#                     w.write("\n")
#
#
#
# # Pre-Processing - Receives a directory containing all the text files of the books and writes them to a new folder after filtering
# # in order to use this function, enter your own folders names.
# def preProcessing(directory):
#     for file in os.listdir(directory):
#         filename = str(file.title(), 'utf-8')
#         # print(filename)
#         f = open(" <Directory>// + <Filename> ", 'r')
#         lines = f.readlines()
#         w = open("<New Directory>// + <Filename>", 'w')
#         for line in lines:
#             tokens = line.split()
#             # convert to lower case
#             tokens = [w.lower() for w in tokens]
#             # remove punctuation from each word
#             table = str.maketrans('', '', string.punctuation)
#             stripped = [w.translate(table) for w in tokens]
#             # remove remaining tokens that are not alphabetic
#             words = [word for word in stripped if word.isalpha()]
#             # filter out stop words
#             stop_words = set(stopwords.words('english'))
#             words = [w for w in words if not w in stop_words]
#             for word in words:
#                 w.write(word+" ")
#             w.write("\n")
#
#
#
#
# '''
#  Pre-Pre-Processing - Receives a directory containing all the text files of the books, same row_length for all files, same vocabulary size for all files.
#  and writes them to a new folder after converting them to a one-hot encoding docs
# # in order to use this function, enter your own folders names.
# '''
# def convertBooksToOneHotEncoding(directory, row_length, vocab_size):
# 	row_length = 50 # row length (50 words in each row)
# 	vocab_size = 5000 # vocabulary size
# 	for file in os.listdir(directory):
# 		filename = str(file.title(),'utf-8')
# 		f = open("<Directory>// + <Filename>", 'r')
# 		lines = f.readlines()
# 		encoded_docs = [one_hot(d, vocab_size) for d in lines])
# 		padded_docs = pad_sequences(encoded_docs, maxlen=row_length, padding='post')
# 		writingFilename = "<New Directory>// + <Filename>"
# 		numpy.savetxt(writingFilename, padded_docs, fmt="%d")
#
