import time

from Config.Constants import Constants
from DataHandler.Vector.OsmUtils import OsmUtils


class OsmJob:
    """
    execute the OSM necessary actions
    reclass cropped files
    """

    def __init__(self, project_shape_mbr):
        self.PROJECT_SHAPE_MBR = project_shape_mbr

    def execute(self):
        OsmUtils().download_urban_subcenters(
            self.PROJECT_SHAPE_MBR,
            Constants.SUB_CENTERS
        )
        # wait for 30 sec to avoid http response code 429
        time.sleep(30)
        OsmUtils().download_streets(
            self.PROJECT_SHAPE_MBR,
            Constants.STREET_NETWORK
        )