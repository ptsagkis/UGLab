from Config.Constants import Constants
from Model.RandomForestModel import RandomForestModel
from Model.SequentialModel import SequentialModel


class ModelJob:
    """
    Run the model it self
    set the number of epochs
    set the number of batch_size
    """

    def __init__(self, project_path, type,  epochs=300, batch_size=350):
        self.project_path = project_path
        self.type = type
        self.epochs = epochs
        self.batch_size = batch_size

    def execute(self):
        if self.type == 'seq':
            SequentialModel(self.project_path, self.epochs, self.batch_size).run_model(
                self.project_path + Constants.OUTPUT_CORINE_ML_DATA1,
                self.project_path + Constants.OUTPUT_CORINE_ML_DATA2,
                self.project_path + Constants.OUTPUT_CORINE_ML_DATA3,
                self.project_path + Constants.OUTPUT_PREDICTION_CORINE_CSV1,
                True
            )
        elif self.type == 'rf':
            RandomForestModel(self.project_path).run_model(
                self.project_path + Constants.OUTPUT_CORINE_ML_DATA1,
                self.project_path + Constants.OUTPUT_CORINE_ML_DATA2,
                self.project_path + Constants.OUTPUT_CORINE_ML_DATA3,
                self.project_path + Constants.OUTPUT_PREDICTION_CORINE_CSV2,
                True
            )
        else:
            print('This is an error. Such model type doesnt exist');