from DataHandler.Raster.RasterUtils import RasterUtils
from Services.SpinnerThread import SpinnerThread
from Config.Constants import Constants


class RasterProducerJob:
    """
    From the generated tabular data create respective raster files
    """

    def __init__(self, project_path):
        self.PROJECT_PATH = project_path
        self.spinner_thread = SpinnerThread()

    def execute(self):
        self.spinner_thread.start()
        RasterUtils.create_raster_from_csv(
            self.PROJECT_PATH + Constants.OUTPUT_PREDICTION_CORINE_CSV1,
            5,
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[3],
            self.PROJECT_PATH + 'ml_data\\corine_2030_PREDICTED_SEQ.tif'
        )

        RasterUtils.create_raster_from_csv(
            self.PROJECT_PATH + Constants.OUTPUT_PREDICTION_CORINE_CSV1,
            4,
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[1],
            self.PROJECT_PATH + 'ml_data\\corine_2018_PREDICTED_SEQ.tif'
        )

        RasterUtils.create_raster_from_csv(
            self.PROJECT_PATH + Constants.OUTPUT_PREDICTION_CORINE_CSV2,
            5,
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[3],
            self.PROJECT_PATH + 'ml_data\\corine_2030_PREDICTED_RF.tif'
        )

        RasterUtils.create_raster_from_csv(
            self.PROJECT_PATH + Constants.OUTPUT_PREDICTION_CORINE_CSV2,
            4,
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[1],
            self.PROJECT_PATH + 'ml_data\\corine_2018_PREDICTED_RF.tif'
        )

        RasterUtils.create_raster_from_csv(
            self.PROJECT_PATH + Constants.OUTPUT_PREDICTION_CORINE_CSV1,
            3,
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[1],
            self.PROJECT_PATH + 'ml_data\\corine_2018_REAL.tif'
        )
        self.spinner_thread.stop()