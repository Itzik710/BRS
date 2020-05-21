import keras
from keras.callbacks import ModelCheckpoint, CSVLogger

from shutil import copyfile
from CNN.Model import getModel
import CustomGenerator;

#
# training params
from Params import modelWeights, modelPath, num_train_samples, batch_size, num_test_samples, logFolder

trainWeights = 'trainWeights.h5'
epochs = 8

# save weights after each epoch
class CustomCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch):
        try:
            copyfile(trainWeights, "ModelGraphs/epoch" + str(epoch) + "_weights.h5")
        except OSError:
            pass
        return



# train CNN model
def trainModel():
    # training and validation generator creations
    train_generator = CustomGenerator.getGenerator("Train")
    valid_generator = CustomGenerator.getGenerator("Valid")

    # gets CNN model
    model = getModel(weightsPath=modelWeights)
    model.save(modelPath)
    model.summary()

    step_size_train = num_train_samples // batch_size
    step_size_test = num_test_samples // batch_size

    csbLogger = CSVLogger(logFolder + '/training.csv')

    ccb = CustomCallback()
    callbacks_list = [
        ModelCheckpoint(filepath=trainWeights, monitor='val_acc'),
        ccb,
        csbLogger
    ]

    history = model.fit_generator(
        train_generator,
        steps_per_epoch=step_size_train,
        epochs=epochs,
        validation_data=valid_generator,
        validation_steps=step_size_test,
        callbacks=callbacks_list)

    # saves model weights
    model.save_weights(trainWeights)
if __name__ == '__main__':
    trainModel()