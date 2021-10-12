from Config.Constants import Constants
from DataHandler.Vector.VectorUtils import VectorUtils


class CoastLineJob:

    def __init__(self, project_path, project_shape_mbr):
        self.PROJECT_SHAPE_MBR = project_shape_mbr
        self.PROJECT_PATH = project_path

    def execute(self):
        VectorUtils.filter_features_with_shape_extent(
            Constants.INPUT_COASTLINE,
            self.PROJECT_PATH + Constants.OUTPUT_COASTLINE,
            self.PROJECT_SHAPE_MBR,  # file to get the mbr from
            True
        )