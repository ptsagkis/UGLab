from Config.Constants import Constants
from DataHandler.Vector.VectorUtils import VectorUtils


class CoastLineJob:

    def __init__(self, project_shape_mbr):
        self.PROJECT_SHAPE_MBR = project_shape_mbr

    def execute(self):
        VectorUtils.filter_features_with_shape_extent(
            Constants.INPUT_COASTLINE,
            Constants.OUTPUT_COASTLINE,
            self.PROJECT_SHAPE_MBR,  # file to get the mbr from
            True
        )