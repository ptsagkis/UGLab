from Config.Constants import Constants
from Model.SequentialModel import SequentialModel


class ModelJob:
    """
    Run the model after all
    """

    def __init__(self, epochs, batch_size):
        self.epochs = epochs
        self.batch_size = batch_size

    def execute(self):
        SequentialModel(self.epochs, self.batch_size).run_model(
            Constants.OUTPUT_CORINE_ML_DATA1,
            Constants.OUTPUT_CORINE_ML_DATA2,
            Constants.OUTPUT_CORINE_ML_DATA3,
            Constants.OUTPUT_PREDICTION_CORINE_CSV1,
            True
        )