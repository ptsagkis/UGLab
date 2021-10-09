from ChainJobs.CoastLineJob import CoastLineJob
from ChainJobs.CorineJob import CorineJob
from ChainJobs.DemJob import DemJob
from ChainJobs.GeoStatsJob import GeoStatsJob
from ChainJobs.MlDataTranslateJob import MlDataTranslateJob
from ChainJobs.OsmJob import OsmJob
from Config.Constants import Constants

Constants.PROJECT_PATH = 'C:\\PHD\\UGLab_athens\\'
PROJECT_SHAPE_MBR_ATHENS = Constants.PROJECT_PATH + 'athens_mbr.shp'
INPUT_DEM_FILE_ATHENS = Constants.SOURCE_DATA_PATH + 'eu_dem_v11_E50N10_3857.TIF'


def run_athens_demo():


    # print('start corine job' + Constants.PROJECT_PATH)
    # CorineJob(PROJECT_SHAPE_MBR_ATHENS, Constants.PROJECT_PATH).execute()
    # print('finish corine job')

    # print('start DEM job'+Constants.PROJECT_PATH)
    # DemJobs(
    #     INPUT_DEM_FILE_ATHENS,
    #     PROJECT_SHAPE_MBR_ATHENS,
    #     Constants.PROJECT_PATH
    # ).execute()
    # print('finish DEM job')


    # print('start geostats job' + Constants.PROJECT_PATH)
    # GeoStatsJob(PROJECT_SHAPE_MBR_ATHENS).execute()
    # print('\n finish geostats job')

    # print('start osm job' + Constants.PROJECT_PATH)
    # OsmJob(PROJECT_SHAPE_MBR_ATHENS).execute()
    # print('\n finish osm job')

    # print('start coastline job' + Constants.PROJECT_PATH)
    # CoastLineJob(PROJECT_SHAPE_MBR_ATHENS).execute()
    # print('\n finish coastline job')

    print('start MlDataTranslateJob job' + Constants.PROJECT_PATH)
    MlDataTranslateJob(PROJECT_SHAPE_MBR_ATHENS).execute()
    print('\n finish MlDataTranslateJob job')


run_athens_demo()
