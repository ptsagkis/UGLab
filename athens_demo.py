from ChainJobs.CorineJob import CorineJob
from ChainJobs.DemJob import DemJobs
from Config.Constants import Constants

Constants.PROJECT_PATH = 'C:\\PHD\\UGLab_athens\\'
PROJECT_SHAPE_MBR_ATHENS = Constants.PROJECT_PATH + 'athens_mbr.shp'
INPUT_DEM_FILE_ATHENS = Constants.SOURCE_DATA_PATH + 'eu_dem_v11_E50N10_3857.TIF'


def run_athens_demo():
    # print('start cropping'+Constants.PROJECT_PATH)
    # CropCorine(PROJECT_SHAPE_MBR_ATHENS, Constants.PROJECT_PATH).run_crop_corine()
    # print('finish cropping')

    # print('start corine reclass' + Constants.PROJECT_PATH)
    # ReclassCorine(Constants.PROJECT_PATH).run_reclass_corine()
    # print('finish corine reclass')

    print('start corine utils'+Constants.PROJECT_PATH)
    CorineJob(PROJECT_SHAPE_MBR_ATHENS, Constants.PROJECT_PATH).execute()
    print('finish corine utils')

    # print('start DEM utilities'+Constants.PROJECT_PATH)
    # DemJobs(
    #     INPUT_DEM_FILE_ATHENS,
    #     PROJECT_SHAPE_MBR_ATHENS,
    #     Constants.PROJECT_PATH
    # ).execute()
    # print('finish DEM utilities')

run_athens_demo()
