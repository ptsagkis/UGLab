from ChainJobs.CoastLineJob import CoastLineJob
from ChainJobs.CorineJob import CorineJob
from ChainJobs.DemJob import DemJob
from ChainJobs.GeoStatsJob import GeoStatsJob
from ChainJobs.MlDataTranslateJob import MlDataTranslateJob
from ChainJobs.ModelJob import ModelJob
from ChainJobs.OsmJob import OsmJob
from Config.Constants import Constants

PROJECT_PATH = 'C:\\PHD\\UGLab_hrakleio\\'
PROJECT_SHAPE_MBR = PROJECT_PATH + 'hrakleio_mbr.shp'
INPUT_DEM_FILE = Constants.SOURCE_DATA_PATH + 'eu_dem_v11_E50N10_3857.TIF'


def run_hrakleio_demo():
    # print('start corine job')
    # CorineJob(PROJECT_SHAPE_MBR, PROJECT_PATH).execute()
    # print('finish corine job')

    # print('start DEM job'+PROJECT_PATH)
    # DemJob(
    #     INPUT_DEM_FILE,
    #     PROJECT_SHAPE_MBR,
    #     PROJECT_PATH
    # ).execute()
    # print('finish DEM job')

    # print('start geostats job')
    # GeoStatsJob(PROJECT_PATH, PROJECT_SHAPE_MBR).execute()
    # print('\n finish geostats job')

    # print('start osm job' )
    # OsmJob(PROJECT_PATH, PROJECT_SHAPE_MBR).execute()
    # print('\n finish osm job')

    # print('start coastline job')
    # CoastLineJob(PROJECT_PATH, PROJECT_SHAPE_MBR).execute()
    # print('\n finish coastline job')

    print('start MlDataTranslateJob job')
    MlDataTranslateJob(PROJECT_PATH).execute()
    print('\n finish MlDataTranslateJob job')
    #
    # print('start running model job')
    # ModelJob(300, 300).execute()
    # print('\n finish running model job')


run_hrakleio_demo()
