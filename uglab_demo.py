from ChainJobs.CoastLineJob import CoastLineJob
from ChainJobs.CorineJob import CorineJob
from ChainJobs.DemJob import DemJob
from ChainJobs.GeoStatsJob import GeoStatsJob
from ChainJobs.MlDataTranslateJob import MlDataTranslateJob
from ChainJobs.ModelJob import ModelJob
from ChainJobs.OsmJob import OsmJob
from ChainJobs.RasterProducerJob import RasterProducerJob
from Config.Constants import Constants

# this is where all produced data will be placed
PROJECT_PATH = '_uglab_demo_project/'
# this is mandatory to start. It is the MBR of your study area. Munich MBR is for demo.
PROJECT_SHAPE_MBR = PROJECT_PATH + 'MUNICH_MBR.shp'
# this is the DEM containing the study area.
# Depending on your area choose and download DEM from --> https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1
INPUT_DEM_FILE = Constants.SOURCE_DATA_PATH + 'eu_dem_v11_E40N20.TIF'


def run_demo():
    print('start corine job')
    CorineJob(PROJECT_PATH, PROJECT_SHAPE_MBR).execute()
    print('finish corine job')

    print('start DEM job'+PROJECT_PATH)
    DemJob(
        INPUT_DEM_FILE,
        PROJECT_SHAPE_MBR,
        PROJECT_PATH
    ).execute()
    print('finish DEM job')

    print('start geostats job')
    GeoStatsJob(PROJECT_PATH, PROJECT_SHAPE_MBR).execute()
    print('\n finish geostats job')

    print('start osm job' )
    OsmJob(PROJECT_PATH, PROJECT_SHAPE_MBR).execute()
    print('\n finish osm job')

    print('start coastline job')
    CoastLineJob(PROJECT_PATH, PROJECT_SHAPE_MBR).execute()
    print('\n finish coastline job')

    print('start MlDataTranslateJob job')
    MlDataTranslateJob(PROJECT_PATH).execute()
    print('\n finish MlDataTranslateJob job')

    print('start running model job')
    ModelJob(PROJECT_PATH, 200, 500).execute()
    print('\n finish running model job')

    print('start running geotif producer job')
    RasterProducerJob(PROJECT_PATH).execute()
    print('\n finish running geotif producer job')


run_demo()
