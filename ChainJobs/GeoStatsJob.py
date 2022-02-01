from Config.Constants import Constants
from DataHandler.Vector.Geostats import Geostats
from DataHandler.Vector.VectorUtils import VectorUtils


class GeoStatsJob:
    """
    Create the population data datagrid
    """

    def __init__(self, project_path, project_shape_mbr):
        self.PROJECT_PATH = project_path
        self.PROJECT_SHAPE_MBR = project_shape_mbr

    def execute(self):

        VectorUtils.filter_features_with_shape_extent(
            Constants.INPUT_POPS_SHP_2006,
            self.PROJECT_PATH + Constants.OUTPUT_POP_2006,
            self.PROJECT_SHAPE_MBR  # file to get the mbr from
        )

        VectorUtils.filter_features_with_shape_extent(
            Constants.INPUT_POPS_SHP_2011,
            self.PROJECT_PATH + Constants.OUTPUT_POP_2011,
            self.PROJECT_SHAPE_MBR,  # file to get the mbr from
            False
        )

        VectorUtils.filter_features_with_shape_extent(
            Constants.INPUT_POPS_SHP_2018,
            self.PROJECT_PATH + Constants.OUTPUT_POP_2018,
            self.PROJECT_SHAPE_MBR,  # file to get the mbr from
            False
        )

        Geostats(self.PROJECT_PATH).create_pop_grid_changes(
            self.PROJECT_PATH + Constants.OUTPUT_POP_CHANGES,
            Constants.INPUT_GRID_CSV_2006_FIELD,
            Constants.INPUT_GRID_CSV_2011_FIELD,
            Constants.INPUT_POPS_CSV_2006,
            Constants.INPUT_POPS_CSV_2011
        )
