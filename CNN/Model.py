from keras.layers import Conv2D, MaxPooling2D, Embedding, Conv1D, MaxPooling1D
from keras.layers import Flatten, Dense, Dropout
from keras.models import Sequential
from keras.optimizers import rmsprop
import Params


# CNN model architecture - loads pre-trained weights if such are already exists.
def getModel(weightsPath=None):

    """
        input: 2D tensor with shape: (batch_size, sequence_length).
        each book contains 600 rows with 50 words in each row.
        input size = 600 * 50 = 30000
    """
    model = Sequential()
    """
        NLP mission - The embedding layer
        input params:
            # input_dim = size of vocabulary(size of unique words in each book)
            # output_dim = dimension of the dense embedding
            # input_length = sequence_length(input size)
        output: 3D tensor with shape: (batch_size, sequence_length, output_dim).  
    """
    model.add(Embedding(input_dim=5000, output_dim=100, input_length=30000))

    model.add(Conv1D(128, 5, activation='relu'))
    model.add(MaxPooling1D(5))

    model.add(Conv1D(128, 5, activation='relu'))
    model.add(MaxPooling1D(5))

    model.add(Conv1D(128, 5, activation='relu'))
    model.add(MaxPooling1D(35))

    # Dense = Fully connected layer - the layer which we will extract the books features from
    model.add(Flatten())
    model.add(Dense(128, name="fullyConnetcted", activation='relu'))

    # Softmax Dense Layer
    model.add(Dense(Params.number_of_classes, activation='softmax'))

    # Optimizer = 'rmsProp'
    opt = rmsprop(le=Params.learnRate)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# checks if the model has already been trained before
    if weightsPath:
        try:
            model.load_weights(weightsPath)
            print("cnn weights loaded.")
        except OSError:
            print("Failed loading cnn weights!")
    else:
        print("cnn weights are not provided.")

    return model