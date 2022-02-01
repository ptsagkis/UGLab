import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, cohen_kappa_score, precision_score, recall_score, f1_score, \
    classification_report
from sklearn.preprocessing import StandardScaler


class RandomForestModel:

    def __init__(self, project_path):
        self.project_path = project_path

    def run_model(self, train_data_csv, test_data_csv, predict_data_csv, output_csv, normalize=False):
        # load the train dataset
        trainDataSet = np.loadtxt(train_data_csv, delimiter=';')
        testDataSet = np.loadtxt(test_data_csv, delimiter=';')
        predictDataSet = np.loadtxt(predict_data_csv, delimiter=';')
        # split into input (X) and output (y) variables
        # create scaler
        scaler = StandardScaler()
        X = trainDataSet[:, 2:20]
        X_test = testDataSet[:, 2:20]
        # dataset to start model
        X_predict = predictDataSet[:, 2:20]
        if normalize == True:
            # fit and transform in one stepZ
            X = scaler.fit_transform(trainDataSet[:, 2:20])
            X_test = scaler.fit_transform(testDataSet[:, 2:20])
            # dataset to start model
            X_predict = scaler.fit_transform(predictDataSet[:, 2:20])

        y = trainDataSet[:, 20]
        y_from = testDataSet[:, 19]
        y_test = testDataSet[:, 20]

        x_coords = trainDataSet[:, 0:1]
        y_coords = trainDataSet[:, 1:2]

        parameters = {
            'bootstrap': True,
            'class_weight': None,
            'criterion': 'gini',
            'max_depth': None,
            'max_features': 'auto',
            'max_leaf_nodes': None,
            'min_impurity_decrease': 0.0,
            # 'min_impurity_split': None,
            'min_samples_leaf': 1,
            'min_samples_split': 2,
            'min_weight_fraction_leaf': 0.0,
            'n_estimators': 100,
            'n_jobs': 1,
            'oob_score': False,
            'random_state': None,
            'verbose': 0,
            'warm_start': False
        }
        RF_model = RandomForestClassifier(**parameters)

        RF_model.fit(X, y)

        # and do the prediction for 2018
        y_predict = np.round(RF_model.predict(X_test), 0)
        # prediction for 2030
        y_future_predict = np.round(RF_model.predict(X_predict), 0)
        # do the metrics
        self._create_model_metrics(y_test, y_predict, RF_model, X_test)

        if os.path.exists(output_csv):
            os.remove(output_csv)
        with open(output_csv, 'ab') as f:
            np.savetxt(f, np.around(np.column_stack((x_coords, y_coords, y_from, y_test, y_predict, y_future_predict)),
                                    decimals=2),
                       fmt='%.2f',
                       delimiter=';')


    @staticmethod
    def _create_model_metrics(y_test, y_predict, model, X_test):
        """
        Just print some metrics on the console
         https://muthu.co/understanding-the-classification-report-in-sklearn/
        :param y_test:
        :param y_predict:
        :return:
        """
        score = accuracy_score(y_test, y_predict)
        print("score: {}".format(score))
        print("cohen kappa: {}".format(cohen_kappa_score(y_test, y_predict)))
        print("Precision score: {}".format(precision_score(y_test, y_predict)))
        print("Recall score: {}".format(recall_score(y_test, y_predict)))
        print("F1 Score: {}".format(f1_score(y_test, y_predict)))
        print("classification_report", classification_report(y_test, y_predict))
