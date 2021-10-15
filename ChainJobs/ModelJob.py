from Config.Constants import Constants
from Model.SequentialModel import SequentialModel


class ModelJob:
    """
    Run the model it self
    set the number of epochs
    set the number of batch_size
    """

    def __init__(self, project_path, epochs, batch_size):
        self.project_path = project_path
        self.epochs = epochs
        self.batch_size = batch_size

    def execute(self):
        SequentialModel(self.project_path, self.epochs, self.batch_size).run_model(
            self.project_path + Constants.OUTPUT_CORINE_ML_DATA1,
            self.project_path + Constants.OUTPUT_CORINE_ML_DATA2,
            self.project_path + Constants.OUTPUT_CORINE_ML_DATA3,
            self.project_path + Constants.OUTPUT_PREDICTION_CORINE_CSV1,
            True
        )