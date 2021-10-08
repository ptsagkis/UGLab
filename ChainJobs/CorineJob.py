from DataHandler.Corine.Corine import Corine
from DataHandler.Raster.RasterUtils import RasterUtils
from Config.Constants import Constants


class CorineJob:
    """
    crop corine to study area mbr
    reclass cropped files
    """

    def __init__(self, project_shape_mbr, project_path):
        self.PROJECT_SHAPE_MBR = project_shape_mbr
        self.PROJECT_PATH = project_path

    def execute(self):
        self.crop_corine(self.PROJECT_PATH, self.PROJECT_SHAPE_MBR)
        self.reclass_corine(self.PROJECT_PATH)

    @staticmethod
    def crop_corine(project_path, project_shape_mbr):
        RasterUtils.crop_reproject_raster(
            Constants.SOURCE_CORINE_FILES[0],
            project_path + 'corine_2000.tif',
            project_shape_mbr,
            Constants.PROJECT_EPSG
        )

        RasterUtils.crop_reproject_raster(
            Constants.SOURCE_CORINE_FILES[1],
            project_path + 'corine_2006.tif',
            project_shape_mbr,
            Constants.PROJECT_EPSG
        )

        RasterUtils.crop_reproject_raster(
            Constants.SOURCE_CORINE_FILES[2],
            project_path + 'corine_2012.tif',
            project_shape_mbr,
            Constants.PROJECT_EPSG
        )

        RasterUtils.crop_reproject_raster(
            Constants.SOURCE_CORINE_FILES[3],
            project_path + 'corine_2018.tif',
            project_shape_mbr,
            Constants.PROJECT_EPSG
        )

    @staticmethod
    def reclass_corine(project_path):
        corine = Corine()
        corine.raster_reclass(
            project_path + 'corine_2000.tif',
            [project_path + 'corine_2000_c1.tif', project_path + 'corine_2000_c2.tif']
        )

        corine.raster_reclass(
            project_path + 'corine_2006.tif',
            [project_path + 'corine_2006_c1.tif', project_path + 'corine_2006_c2.tif']
        )

        corine.raster_reclass(
            project_path + 'corine_2012.tif',
            [project_path + 'corine_2012_c1.tif', project_path + 'corine_2012_c2.tif']
        )

        corine.raster_reclass(
            project_path + 'corine_2018.tif',
            [project_path + 'corine_2018_c1.tif', project_path + 'corine_2018_c2.tif']
        )