from DataHandler.Raster.DemUtils import DemUtils
from DataHandler.Raster.RasterUtils import RasterUtils
from Config.Constants import Constants


class DemJobs:

    def __init__(self, INPUT_DEM_FILE_ATHENS, PROJECT_SHAPE_MBR, PROJECT_PATH):
        self.PROJECT_SHAPE_MBR = PROJECT_SHAPE_MBR
        self.PROJECT_PATH = PROJECT_PATH
        self.INPUT_DEM_FILE_ATHENS = INPUT_DEM_FILE_ATHENS

    def execute(self):
        RasterUtils.crop_reproject_raster(
            self.INPUT_DEM_FILE_ATHENS,  # dem in
            Constants.OUTPUT_DEM_CROPPED,  # dem out
            self.PROJECT_SHAPE_MBR,
            Constants.PROJECT_EPSG
        )

        DemUtils.create_dem_product(
            Constants.OUTPUT_SLOPE,
            Constants.OUTPUT_DEM_CROPPED,
            'slope'
        )
        DemUtils.create_dem_product(
            Constants.OUTPUT_ASPECT,
            Constants.OUTPUT_DEM_CROPPED,
            'aspect'
        )
        DemUtils.create_dem_product(
            Constants.OUTPUT_HILLSHADE,
            Constants.OUTPUT_DEM_CROPPED,
            'hillshade'
        )
