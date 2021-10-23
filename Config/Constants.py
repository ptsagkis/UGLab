class Constants:


    # generic app config
    # this is where source data exist
    SOURCE_DATA_PATH = '_uglab_source_demo_data/'
    SOURCE_CORINE_FILES = [
        SOURCE_DATA_PATH + 'U2006_CLC2000_V2020_20u1.tif',
        SOURCE_DATA_PATH + 'U2012_CLC2006_V2020_20u1.tif',
        SOURCE_DATA_PATH + 'U2018_CLC2012_V2020_20u1.tif',
        SOURCE_DATA_PATH + 'U2018_CLC2018_V2020_20u1.tif'
    ]
    PROJECT_EPSG = '3857'
    ML_RESULTS_DIR = 'ml_data/'
    MODEL_CHECKPOINT_FILE = 'ml_data/weights_corine.hdf5'


    ####################################################################################
    #################### DATA PREPARATION RELATED CONFIG ###############################
    #################### DONT MAKE CHANGES THIS POINT FORWARD ##########################
    ##################### unless you know what you are doing ###########################Z
    ####################################################################################
    # CORINE Dataset
    OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_1 = [
        'corine_2000_c1.tif',
        'corine_2006_c1.tif',
        'corine_2012_c1.tif',
        'corine_2018_c1.tif'
    ]
    OUTPUT_RECLASS_RASTER_CORINE_STEPS_CODE_2 = [
        'corine_2000_c2.tif',
        'corine_2006_c2.tif',
        'corine_2012_c2.tif',
        'corine_2018_c2.tif'
    ]
    # DEM utils
    OUTPUT_DEM_CROPPED = 'DEM.TIF'
    OUTPUT_HILLSHADE = 'DEM_hillshade.TIF'
    OUTPUT_SLOPE = 'DEM_slope.TIF'
    OUTPUT_ASPECT = 'DEM_aspect.TIF'

    # GEOSTATS POP CHANGES
    INPUT_POPS_SHP_2006 = SOURCE_DATA_PATH + 'Grid_ETRS89_LAEA_1K_ref_GEOSTAT_2006.shp'
    INPUT_POPS_SHP_2011 = SOURCE_DATA_PATH + 'Grid_ETRS89_LAEA_1K-ref_GEOSTAT_POP_2011_V2_0_1.shp'
    INPUT_POPS_CSV_2006 = SOURCE_DATA_PATH + 'GEOSTAT_grid_EU_POP_2006_1K_V1_1_1.csv'
    INPUT_POPS_CSV_2011 = SOURCE_DATA_PATH + 'GEOSTAT_grid_POP_1K_2011_V2_0_1.csv'
    OUTPUT_POP_2006 = 'POP_2006_GRID.shp'
    OUTPUT_POP_2011 = 'POP_2011_GRID.shp'
    OUTPUT_POP_CHANGES = 'POP_GRID_FINAL.shp'
    OUTPUT_POP_CHANGES_FIELD = 'POP_CHANGE'
    INPUT_GRID_CSV_2006_FIELD = 'GRD_INSPIR'
    INPUT_GRID_CSV_2011_FIELD = 'GRD_ID'

    # OSM DATA
    STREET_NETWORK = 'STREETS_NET.shp'
    SUB_CENTERS = 'SUB_CENTERS.shp'

    # COASTLINE
    INPUT_COASTLINE = SOURCE_DATA_PATH + 'EUHYDRO_Coastline_EEA39_v013.shp'
    OUTPUT_COASTLINE = 'COASTLINE.shp'

    # ANALYSIS RESULTS - CHANGES AMONG STEPS
    OUTPUT_CHANGES_MATRIX_C1_STEP_1_2 = 'changes_matrix_c1_1_2.csv'
    OUTPUT_CHANGES_MATRIX_C1_STEP_2_3 = 'changes_matrix_c1_2_3.csv'
    OUTPUT_CHANGES_MATRIX_C2_STEP_1_2 = 'changes_matrix_c2_1_2.csv'
    OUTPUT_CHANGES_MATRIX_C2_STEP_2_3 = 'changes_matrix_c2_2_3.csv'

    # DATA SCIENCE - MACHINE LEARNING DATA TRANSLATOR CORINE
    OUTPUT_CORINE_ML_DATA1 = 'corine_mldata1.csv'
    OUTPUT_CORINE_ML_DATA2 = 'corine_mldata2.csv'
    OUTPUT_CORINE_ML_DATA3 = 'corine_mldata3.csv'

    # MODEL OUTPUTS CORINE
    OUTPUT_PREDICTION_CORINE_CSV1 = 'ml_data\\predict1_corine.csv'
    OUTPUT_PREDICTION_CORINE_CSV2 = 'ml_data\\predict2_corine.csv'
