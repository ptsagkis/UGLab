import time

from Config.Constants import Constants
from DataHandler.ML.Translate import Translate


class MlDataTranslateJob:
    """
    execute the OSM necessary actions
    reclass cropped files
    """

    def __init__(self, project_shape_mbr):
        self.PROJECT_SHAPE_MBR = project_shape_mbr

    @staticmethod
    def execute():
        Translate().spatial_to_ml(
            Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[0],
            Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_1[0],
            Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[1],
            Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_1[1],
            Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[2],
            Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_1[2],
            Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2[3],
            Constants.OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_1[3],
            Constants.STREET_NETWORK,
            Constants.SUB_CENTERS,
            Constants.OUTPUT_COASTLINE,
            Constants.OUTPUT_POP_CHANGES,
            Constants.OUTPUT_POP_CHANGES_FIELD,
            Constants.OUTPUT_DEM_CROPPED,
            Constants.OUTPUT_SLOPE,
            Constants.OUTPUT_HILLSHADE,
            Constants.OUTPUT_ASPECT,
            Constants.OUTPUT_CORINE_ML_DATA1,
            Constants.OUTPUT_CORINE_ML_DATA2,
            Constants.OUTPUT_CORINE_ML_DATA3

        )