from DataHandler.Raster.DemUtils import DemUtils
from DataHandler.Raster.RasterUtils import RasterUtils
from Config.Constants import Constants


class DemJob:
    """
    Produce all the DEM products ['dem','slope','hillshade','aspect']
    """

    def __init__(self, input_dem_file, project_shape_mbr, project_path):
        self.PROJECT_SHAPE_MBR = project_shape_mbr
        self.PROJECT_PATH = project_path
        self.INPUT_DEM_FILE = input_dem_file

    def execute(self):
        RasterUtils.crop_reproject_raster(
            self.INPUT_DEM_FILE,  # dem in
            self.PROJECT_PATH + Constants.OUTPUT_DEM_CROPPED,  # dem out
            self.PROJECT_SHAPE_MBR,
            Constants.PROJECT_EPSG
        )

        DemUtils.create_dem_product(
            self.PROJECT_PATH + Constants.OUTPUT_SLOPE,
            self.PROJECT_PATH + Constants.OUTPUT_DEM_CROPPED,
            'slope'
        )
        DemUtils.create_dem_product(
            self.PROJECT_PATH + Constants.OUTPUT_ASPECT,
            self.PROJECT_PATH + Constants.OUTPUT_DEM_CROPPED,
            'aspect'
        )
        DemUtils.create_dem_product(
            self.PROJECT_PATH + Constants.OUTPUT_HILLSHADE,
            self.PROJECT_PATH + Constants.OUTPUT_DEM_CROPPED,
            'hillshade'
        )
