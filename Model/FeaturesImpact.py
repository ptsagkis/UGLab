from matplotlib.pyplot import xticks
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot
from Config.Constants import Constants
from Services.FileUtils import FileUtils


class FeaturesImpact:
    """
    couple of methods to support the representation of feature's impact
    """

    def __init__(self, project_path):
        self.project_path = project_path
        self.plot_labels = [
            'road_net',
            'city_dist',
            'coast_dist',
            'height',
            'slope',
            'hillshade',
            'aspect',
            'pop',
            '1', '2', '3', '4', '5', '6', '7', '8',
            't-1 class A',
            't-1 class B',
        ]

    def printImportanceLR(self, X_train, y_train, show=False):
        """
        Set the solver. @default: 'lbfgs'
        ‘newton-cg’ - [‘l2’, ‘none’]
        ‘lbfgs’ - [‘l2’, ‘none’]
        ‘liblinear’ - [‘l1’, ‘l2’]
        ‘sag’ - [‘l2’, ‘none’]
        ‘saga’ - [‘elasticnet’, ‘l1’, ‘l2’, ‘none’]
        """
        model = LogisticRegression(solver='lbfgs', max_iter=1000)
        # fit the model
        model.fit(X_train, y_train)
        # get importance
        importance = model.coef_[0]
        # remove last two elements
        importance_m = importance[:len(importance)]
        # print summarize feature importance
        for i, v in enumerate(importance):
            print('Feature: %0d, Score: %.5f' % (i, v))
        # plot feature importance
        pyplot.bar([x for x in range(len(importance_m))], [float(i)/sum(list(map(abs, importance_m))) for i in list(map(abs, importance_m))])
        locs, labels = xticks()
        pyplot.subplots_adjust(bottom=0.2)
        xticks([*range(0, 18, 1)],
               self.plot_labels,
               rotation=90)  # Set text labels and properties.
        FileUtils.delete_file(self.project_path + Constants.ML_RESULTS_DIR + 'FEATURE_IMPACT_LR.png')
        pyplot.savefig(self.project_path + Constants.ML_RESULTS_DIR + 'FEATURE_IMPACT_LR.png')
        if show:
            pyplot.show()

    def printImportanceRF(self, X_train, y_train, show=False):
        model = RandomForestRegressor()
        # fit the model
        model.fit(X_train, y_train)
        # get importance
        importance = model.feature_importances_
        # remove last two elements
        importance_m = importance[:len(importance)]
        # summarize feature importance
        for i, v in enumerate(importance):
            print('Feature: %0d, Score: %.5f' % (i, v))
        # plot feature importance
        pyplot.bar([x for x in range(len(importance_m))], list(map(abs, importance_m)))
        locs, labels = xticks()
        pyplot.subplots_adjust(bottom=0.2)

        xticks([*range(0, 18, 1)],
               self.plot_labels,
               rotation=45)  # Set text labels and properties.
        FileUtils.delete_file(self.project_path + Constants.ML_RESULTS_DIR + 'FEATURE_IMPACT_RF.png')
        pyplot.savefig(self.project_path + Constants.ML_RESULTS_DIR + 'FEATURE_IMPACT_RF.png')
        if show:
            pyplot.show()
