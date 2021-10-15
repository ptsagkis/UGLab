from Config.Constants import Constants
from DataHandler.ML.Translate import Translate


class MlDataTranslateJob:
    """
    Finally translate all the spatial data to tabular data

    """

    def __init__(self, project_path):
        self.PROJECT_PATH = project_path


    def execute(self):
        Translate().spatial_to_ml(
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[0],
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_1[0],
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[1],
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_1[1],
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[2],
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_1[2],
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[3],
            self.PROJECT_PATH + Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_1[3],
            self.PROJECT_PATH + Constants.STREET_NETWORK,
            self.PROJECT_PATH + Constants.SUB_CENTERS,
            self.PROJECT_PATH + Constants.OUTPUT_COASTLINE,
            self.PROJECT_PATH + Constants.OUTPUT_POP_CHANGES,
            Constants.OUTPUT_POP_CHANGES_FIELD,
            self.PROJECT_PATH + Constants.OUTPUT_DEM_CROPPED,
            self.PROJECT_PATH + Constants.OUTPUT_SLOPE,
            self.PROJECT_PATH + Constants.OUTPUT_HILLSHADE,
            self.PROJECT_PATH + Constants.OUTPUT_ASPECT,
            self.PROJECT_PATH + Constants.OUTPUT_CORINE_ML_DATA1,
            self.PROJECT_PATH + Constants.OUTPUT_CORINE_ML_DATA2,
            self.PROJECT_PATH + Constants.OUTPUT_CORINE_ML_DATA3
        )

