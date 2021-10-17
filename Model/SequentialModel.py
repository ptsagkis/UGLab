import numpy as np
import matplotlib.pyplot as plt
import os

from keras import Sequential

from keras.callbacks import ModelCheckpoint
from keras.layers import Dense
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score, cohen_kappa_score
from sklearn.preprocessing import StandardScaler
from Model.FeaturesImpact import FeaturesImpact
from Services.FileUtils import FileUtils
from Config.Constants import Constants


class SequentialModel:
    """
     A class to support model execution procedure
    """

    def __init__(self, project_path, epochs=300, batch_size=500):
        self.project_path = project_path
        self.epochs = epochs
        self.batch_size = batch_size

    def run_model(self, train_data_csv, test_data_csv, predict_data_csv, output_csv1, normalize=False):
        """
        Get the data set created from previous steps @MLData.Translate
        and break them down into ML data
        :param train_data_csv:
        :param test_data_csv:
        :param predict_data_csv:
        :param output_csv1:
        :param normalize:
        :return: void
        """
        # create the folder to hold ml data
        FileUtils.create_dir(self.project_path + '\\ml_data')

        # load the train dataset
        train_data_set = np.loadtxt(train_data_csv, delimiter=';')
        test_data_set = np.loadtxt(test_data_csv, delimiter=';')
        predict_data_set = np.loadtxt(predict_data_csv, delimiter=';')

        # split into input (X) and output (y) variables and do some normalisation
        x_coords, y_coords, X, X_test, X_predict, y, y_from, y_test = self._normalize_data(
            train_data_set, test_data_set, predict_data_set, normalize
        )
        # draw feature impact to a plot
        feats_impact = FeaturesImpact(self.project_path)
        feats_impact.printImportanceLR(X, y, False)
        feats_impact.printImportanceRF(X, y, False)
        # get the number of columns out of the first sample
        model = self._create_model(len(X[0]))

        checkpoint = ModelCheckpoint(self.project_path + Constants.MODEL_CHECKPOINT_FILE, monitor='val_accuracy', verbose=1,
                                     save_weights_only=True, save_best_only=True, mode='max')
        callbacks_list = [checkpoint]
        # train the model
        hist_2 = model.fit(X, y,
                           callbacks=callbacks_list,
                           epochs=self.epochs,
                           batch_size=self.batch_size,
                           verbose=2,
                           validation_data=(X_test, y_test))

        # and do the prediction for 2018
        y_predict = np.round(model.predict(X_test), 0)
        # prediction for 2030
        y_future_predict = np.round(model.predict(X_predict), 0)
        # do the metrics
        self._create_model_metrics(y_test, y_predict, model, X_test)

        if os.path.exists(output_csv1):
            os.remove(output_csv1)
        with open(output_csv1, 'ab') as f:
            np.savetxt(f, np.around(np.column_stack((x_coords, y_coords, y_from, y_test, y_predict, y_future_predict)),
                                    decimals=2),
                       fmt='%.2f',
                       delimiter=';')
        self._print_data_loss_plot(hist_2, self.project_path)
        self._print_data_accuracy_plot(hist_2, self.project_path)

    @staticmethod
    def _normalize_data(train_data_set, test_data_set, predict_data_set, normalize):
        """
        Scales the data to a number from 0 to 1
        Splits the dataset into x,y coords
        and into input (X) and output (y)
        :param train_data_set:
        :param test_data_set:
        :param predict_data_set:
        :param normalize: boolean
        :return:
        """
        scaler = StandardScaler()
        # scaler = MinMaxScaler()
        X = train_data_set[:, 2:20]
        X_test = test_data_set[:, 2:20]

        x_coords = train_data_set[:, 0:1]
        y_coords = train_data_set[:, 1:2]

        # dataset to start model
        X_predict = predict_data_set[:, 2:20]
        if normalize:
            # fit and transform in one stepZ
            X = scaler.fit_transform(train_data_set[:, 2:20])
            X_test = scaler.fit_transform(test_data_set[:, 2:20])
            # dataset to start model
            X_predict = scaler.fit_transform(predict_data_set[:, 2:20])

        y = train_data_set[:, 20]
        y_from = test_data_set[:, 19]
        y_test = test_data_set[:, 20]
        return x_coords, y_coords, X, X_test, X_predict, y, y_from, y_test

    @staticmethod
    def _create_model(input_dim):
        """
        This is the heart of our model
        We have a neural network with 4 layers
        1 input layer
        2 hidden layers
        1 ouptut layer
        :param input_dim: number of columns. Transition rules
        :return:
        """
        model = Sequential()
        model.add(Dense(20, input_dim=input_dim, activation='relu'))
        model.add(Dense(80, activation='relu'))
        model.add(Dense(120, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
        return model

    @staticmethod
    def _create_model_metrics(y_test, y_predict, model, X_test):
        """
        Just print some metrics on the console
         https://muthu.co/understanding-the-classification-report-in-sklearn/
        :param y_test:
        :param y_predict:
        :return:
        """
        loss, accuracy = model.evaluate(X_test, y_test)
        print('Accuracy: %.2f' % (accuracy * 100))
        print('accuracy', accuracy)
        print('loss', loss)
        print("cohen kappa: {}".format(cohen_kappa_score(y_test, y_predict)))
        print("Precision score: {}".format(precision_score(y_test, y_predict)))
        print("Recall score: {}".format(recall_score(y_test, y_predict)))
        print("F1 Score: {}".format(f1_score(y_test, y_predict)))
        print("classification_report", classification_report(y_test, y_predict))

    @staticmethod
    def _print_data_loss_plot(hist, project_path, show=False):
        """
        Save and show the data loss plot
        :param hist:
        :return:
        """
        plt.plot(hist.history['loss'])
        plt.plot(hist.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='upper right')
        FileUtils.delete_file(project_path + Constants.ML_RESULTS_DIR + 'val_loss.png')
        plt.savefig(project_path + Constants.ML_RESULTS_DIR + 'val_loss.png')
        if show:
            plt.show()

    @staticmethod
    def _print_data_accuracy_plot(hist, project_path, show=False):
        """
        Save and show the data accuracy plot
        :param hist:
        :return:
        """
        plt.plot(hist.history['accuracy'])
        plt.plot(hist.history['val_accuracy'])
        plt.title('Model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='upper right')
        FileUtils.delete_file(project_path + Constants.ML_RESULTS_DIR + 'val_accuracy.png')
        plt.savefig(project_path + Constants.ML_RESULTS_DIR + 'val_accuracy.png')
        if show:
            plt.show()
