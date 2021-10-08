class Constants:
    # generic app config
    # PYTHON_LOC = 'C:\\Users\\Acer\\AppData\\Local\\Programs\\Python\\Python37\\python.exe'
    # GDAL_CALC_SCRIPT_LOC = 'C:\\Users\\Acer\\AppData\\Local\\Programs\\Python\\Python37\\Scripts\\gdal_calc.py'
    # GDAL_SCRIPTS_PATH = 'C:\\Users\\Acer\\AppData\\Local\\Programs\\Python\\Python37\\Scripts'
    # PYTHON_LOC = 'C:\\Users\\Acer\\AppData\\Local\\Programs\\Python\\Python37\\python.exe'
    # GDAL_CALC_SCRIPT_LOC = 'C:\\Users\\Acer\\AppData\\Local\\Programs\\Python\\Python37\\Scripts\\gdal_calc.py'
    PROJECT_PATH = 'C:\\PHD\\UGLab_athens\\'
    # this is where source data exist
    SOURCE_DATA_PATH = 'E:\\backup_files\\PHD_\\data\\'
    SOURCE_CORINE_FILES = [
        'C:\\PHD\\corine\\U2006_CLC2000_V2020_20u1.tif',
        'C:\\PHD\\corine\\U2012_CLC2006_V2020_20u1.tif',
        'C:\\PHD\\corine\\U2018_CLC2012_V2020_20u1.tif',
        'C:\\PHD\\corine\\U2018_CLC2018_V2020_20u1.tif'
    ]
    PROJECT_EPSG = '3857'
    # PROJECT_PIXEL_METERS = 100
    ML_RESULTS_DIR = PROJECT_PATH + 'ml_data\\'
    MODEL_CHECKPOINT_FILE = PROJECT_PATH + 'ml_data\\weights_corine.hdf5'

    # PROJECT_SHAPE_MBR = 'C:\\PHD\\UGLab_test_project\\MUNICH_MBR.shp'
    # PROJECT_SHAPE_MBR_BARCHELONA = 'C:\\PHD\\UGLab_barchelona\\BARCHELONA_MBR.shp'
    # PROJECT_SHAPE_MBR_GRAZ = PROJECT_PATH + 'graz_mbr.shp'
    # PROJECT_SHAPE_MBR_MANCHESTER = PROJECT_PATH + 'manchester_mbr.shp'
    # PROJECT_SHAPE_MBR_AMSTERDAM = PROJECT_PATH + 'amsterdam_mbr.shp'
    # PROJECT_SHAPE_MBR_MILANO = PROJECT_PATH + 'milano_mbr.shp'
    # PROJECT_SHAPE_MBR_BERLIN = PROJECT_PATH + 'berlin_mbr.shp'
    # PROJECT_SHAPE_MBR_BRUSSELS = PROJECT_PATH + 'brussels_mbr.shp'
    # PROJECT_SHAPE_MBR_PARIS = PROJECT_PATH + 'paris_mbr.shp'
    # PROJECT_SHAPE_MBR_COPENHAGEN = PROJECT_PATH + 'copenhagen_mbr.shp'
    # PROJECT_SHAPE_MBR_STOCKHOLM = PROJECT_PATH + 'stockholm_mbr.shp'
    # PROJECT_SHAPE_MBR_ATHENS = PROJECT_PATH + 'athens_mbr.shp'
    # PROJECT_SHAPE_MBR_WIEN = PROJECT_PATH + 'wien_mbr.shp'
    # PROJECT_SHAPE_MBR_ROMA = PROJECT_PATH + 'roma_mbr.shp'
    # PROJECT_SHAPE_MBR_THESSALONIKI = PROJECT_PATH + 'thessaloniki_mbr.shp'
    # PROJECT_SHAPE_MBR_LARISSA = PROJECT_PATH + 'larissa_mbr.shp'
    # PROJECT_SHAPE_MBR_PATRA = PROJECT_PATH + 'patra_mbr.shp'
    # PROJECT_SHAPE_MBR_HRAKLEIO = PROJECT_PATH + 'hrakleio_mbr.shp'

    # HYPSOGRAPHY
    # INPUT_DEM_FILE = SOURCE_DATA_PATH + 'eu_dem_v11_E40N20_3857.TIF'
    # INPUT_DEM_FILE_BARCHELONA = SOURCE_DATA_PATH + 'eu_dem_v11_E30N20_3857.TIF'
    # INPUT_DEM_FILE_GRAZ = SOURCE_DATA_PATH + 'eu_dem_v11_E40N20_3857.TIF'
    # INPUT_DEM_FILE_MANCHESTER = SOURCE_DATA_PATH + 'eu_dem_v11_E30N30_3857.TIF'
    # INPUT_DEM_FILE_AMSTERDAM = SOURCE_DATA_PATH + 'eu_dem_v11_E30N30_3857.TIF'
    # INPUT_DEM_FILE_MILANO = SOURCE_DATA_PATH + 'eu_dem_v11_E40N20_3857.TIF'
    # INPUT_DEM_FILE_BERLIN = SOURCE_DATA_PATH + 'eu_dem_v11_E40N30_3857.TIF'
    # INPUT_DEM_FILE_BRUSSELS = SOURCE_DATA_PATH + 'eu_dem_v11_E30N30_3857.TIF'
    # INPUT_DEM_FILE_PARIS = SOURCE_DATA_PATH + 'eu_dem_v11_E30N20_3857.TIF'
    # INPUT_DEM_FILE_COPENHAGEN = SOURCE_DATA_PATH + 'eu_dem_v11_E40N30_3857.TIF'
    # INPUT_DEM_FILE_STOCKHOLM = SOURCE_DATA_PATH + 'eu_dem_v11_E40N40_3857.TIF'
    # INPUT_DEM_FILE_ATHENS = SOURCE_DATA_PATH + 'eu_dem_v11_E50N10_3857.TIF'
    # INPUT_DEM_FILE_WIEN = SOURCE_DATA_PATH + 'eu_dem_v11_E40N20_3857.TIF'
    # INPUT_DEM_FILE_ROMA = SOURCE_DATA_PATH + 'eu_dem_v11_E40N20_3857.TIF'
    # INPUT_DEM_FILE_THESSALONIKI = SOURCE_DATA_PATH + 'eu_dem_v11_E50N20_3857.TIF'
    # INPUT_DEM_FILE_LARISSA = SOURCE_DATA_PATH + 'eu_dem_v11_E50N10_3857.TIF'
    # INPUT_DEM_FILE_PATRA = SOURCE_DATA_PATH + 'eu_dem_v11_E50N10_3857.TIF'
    # INPUT_DEM_FILE_HRAKLEIO = SOURCE_DATA_PATH + 'eu_dem_v11_E50N10_3857.TIF'
    ####################################################################################
    #################### DATA PREPARATION RELATED CONFIG ###############################
    #################### DONT MAKE CHANGES THIS POINT FORWARD ##########################
    ##################### unless you know what you are doing ##########################
    ####################################################################################
    # CORINE Dataset
    OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_1 = [
        PROJECT_PATH + 'CORINE_2000_c1.tif',
        PROJECT_PATH + 'CORINE_2006_c1.tif',
        PROJECT_PATH + 'CORINE_2012_c1.tif',
        PROJECT_PATH + 'CORINE_2018_c1.tif'
    ]
    OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2 = [
        PROJECT_PATH + 'CORINE_2000_c2.tif',
        PROJECT_PATH + 'CORINE_2006_c2.tif',
        PROJECT_PATH + 'CORINE_2012_c2.tif',
        PROJECT_PATH + 'CORINE_2018_c2.tif'
    ]
    # DEM utils
    OUTPUT_DEM_CROPPED = PROJECT_PATH + 'DEM.TIF'
    OUTPUT_HILLSHADE = PROJECT_PATH + 'DEM_hillshade.TIF'
    OUTPUT_SLOPE = PROJECT_PATH + 'DEM_slope.TIF'
    OUTPUT_ASPECT = PROJECT_PATH + 'DEM_aspect.TIF'

    # GEOSTATS POP CHANGES
    INPUT_POPS_SHP_2006 = SOURCE_DATA_PATH + 'Grid_ETRS89_LAEA_1K_ref_GEOSTAT_2006.shp'
    INPUT_POPS_SHP_2011 = SOURCE_DATA_PATH + 'Grid_ETRS89_LAEA_1K-ref_GEOSTAT_POP_2011_V2_0_1.shp'
    INPUT_POPS_CSV_2006 = SOURCE_DATA_PATH + 'GEOSTAT_grid_EU_POP_2006_1K_V1_1_1.csv'
    INPUT_POPS_CSV_2011 = SOURCE_DATA_PATH + 'GEOSTAT_grid_POP_1K_2011_V2_0_1.csv'
    OUTPUT_POP_2006 = PROJECT_PATH + 'EU_POP_2006_GRID.shp'
    OUTPUT_POP_2011 = PROJECT_PATH + 'EU_POP_2011_GRID.shp'
    OUTPUT_POP_CHANGES = PROJECT_PATH + 'EU_POP_GRID_FINAL.shp'
    INPUT_GRID_CSV_2006_FIELD = 'GRD_INSPIR'
    INPUT_GRID_CSV_2011_FIELD = 'GRD_ID'

    # OSM DATA
    STREET_NETWORK = PROJECT_PATH + 'STREETS_NET_RESAMPLE.shp'
    SUB_CENTERS = PROJECT_PATH + 'SUB_CENTERS.shp'

    # COASTLINE
    INPUT_COASTLINE = SOURCE_DATA_PATH + 'EUHYDRO_Coastline_EEA39_v013_3857.shp'
    OUTPUT_COASTLINE = PROJECT_PATH + 'COASTLINE.shp'

    # ANALYSIS RESULTS - CHANGES AMONG STEPS
    OUTPUT_CHANGES_MATRIX_C1_STEP_1_2 = PROJECT_PATH + 'changes_matrix_c1_1_2.csv'
    OUTPUT_CHANGES_MATRIX_C1_STEP_2_3 = PROJECT_PATH + 'changes_matrix_c1_2_3.csv'
    OUTPUT_CHANGES_MATRIX_C2_STEP_1_2 = PROJECT_PATH + 'changes_matrix_c2_1_2.csv'
    OUTPUT_CHANGES_MATRIX_C2_STEP_2_3 = PROJECT_PATH + 'changes_matrix_c2_2_3.csv'

    # DATA SCIENCE - MACHINE LEARNING DATA TRANSLATOR CORINE
    OUTPUT_CORINE_ML_DATA1 = PROJECT_PATH + 'corine_mldata1.csv'
    OUTPUT_CORINE_ML_DATA2 = PROJECT_PATH + 'corine_mldata2.csv'
    OUTPUT_CORINE_ML_DATA3 = PROJECT_PATH + 'corine_mldata3.csv'

    # MODEL OUTPUTS CORINE
    OUTPUT_PREDICTION_CORINE_CSV1 = PROJECT_PATH + 'ml_data\\predict1_corine.csv'
    OUTPUT_PREDICTION_CORINE_CSV2 = PROJECT_PATH + 'ml_data\\predict2_corine.csv'
