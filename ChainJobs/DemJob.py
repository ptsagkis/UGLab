from DataHandler.Raster.DemUtils import DemUtils
from DataHandler.Raster.RasterUtils import RasterUtils
from Config.Constants import Constants


class DemJobs:

    def __init__(self, input_dem_file, project_shape_mbr, project_path):
        self.PROJECT_SHAPE_MBR = project_shape_mbr
        self.PROJECT_PATH = project_path
        self.INPUT_DEM_FILE_ATHENS = input_dem_file

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
