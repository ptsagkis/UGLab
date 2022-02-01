import csv
from Config.Constants import Constants
from DataHandler.Vector.VectorUtils import VectorUtils
from Services.SpinnerThread import SpinnerThread
from Services.Progress import Progress
from osgeo import ogr


class Geostats:
    """
    Class to support the geostats dataset from https://ec.europa.eu/eurostat
    Download data from:
    https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/population-distribution-demography/geostat
    Extract the following files in your disk.
    Grid_ETRS89_LAEA_1K_ref_GEOSTAT_2006.shp
    Grid_ETRS89_LAEA_1K-ref_GEOSTAT_POP_2011_V2_0_1.shp
    GEOSTAT_grid_EU_POP_2006_1K_V1_1_1.csv
    GEOSTAT_grid_POP_1K_2011_V2_0_1.csv
    """

    def __init__(self, project_path):
        self.shape1 = project_path + Constants.OUTPUT_POP_2006
        self.shape2 = project_path + Constants.OUTPUT_POP_2011
        self.shape3 = project_path + Constants.OUTPUT_POP_2018

    def create_pop_grid_changes(self, shape_out, field1, field2, input_csv1, input_csv2):
        """
        Using the downloaded data and this method create a pop grid
        covering the study area and holding pops for 2006 + 2011 + change %
        :param shape_out: --> study_area_pop_changes output shapefile
        :param field1: --> field of shapefile1 holding pop count
        :param field2: --> field of shapefile2 holding pop count
        :param input_csv1: --> GEOSTAT_grid_EU_POP_2006_1K_V1_1_1.csv
        :param input_csv2: --> GEOSTAT_grid_POP_1K_2011_V2_0_1.csv
        :return:
        """
        driver = ogr.GetDriverByName('ESRI Shapefile')
        in1_shape = driver.Open(self.shape1, 0)
        in1_layer = in1_shape.GetLayer()

        driver = ogr.GetDriverByName('ESRI Shapefile')
        in2_shape = driver.Open(self.shape2, 0)
        in2_layer = in2_shape.GetLayer()

        driver = ogr.GetDriverByName('ESRI Shapefile')
        in3_shape = driver.Open(self.shape3, 0)
        in3_layer = in3_shape.GetLayer()


        driver_out = ogr.GetDriverByName('ESRI Shapefile')
        ds = driver_out.CreateDataSource(shape_out)
        output_layer = ds.CreateLayer('POP STATS', srs=in1_layer.GetSpatialRef(),
                                      geom_type=in1_layer.GetLayerDefn().GetGeomType())
        ogr_id_field = ogr.FieldDefn('GRID_ID', ogr.OFTString)
        ogr_id_field.SetWidth(254)
        output_layer.CreateField(ogr_id_field)
        pop_2006_field = ogr.FieldDefn('POP06', ogr.OFTInteger)
        pop_2011_field = ogr.FieldDefn('POP11', ogr.OFTInteger)
        pop_2018_field = ogr.FieldDefn('POP18', ogr.OFTInteger)
        pop_change_field_06_11 = ogr.FieldDefn('POP_06_11', ogr.OFTReal)
        pop_change_field_11_18 = ogr.FieldDefn('POP_11_18', ogr.OFTReal)
        output_layer.CreateField(pop_2006_field)
        output_layer.CreateField(pop_2011_field)
        output_layer.CreateField(pop_2018_field)
        output_layer.CreateField(pop_change_field_06_11)
        output_layer.CreateField(pop_change_field_11_18)

        existingids = []
        pbar = Progress()

        counter = 0
        max_f = in1_layer.GetFeatureCount()

        for feat1 in in1_layer:
            feature_out = ogr.Feature(output_layer.GetLayerDefn())
            cur1_val = feat1.GetField(field1)
            existingids.append(cur1_val)
            feature_out.SetGeometry(feat1.GetGeometryRef())
            feature_out.SetField('GRID_ID', cur1_val)
            output_layer.CreateFeature(feature_out)
            counter = counter + 1
            pbar.progress(counter, max_f, 'Geostats pop 2006: ', 'Progress:')

        counter = 0
        max_f = in2_layer.GetFeatureCount()

        for feat2 in in2_layer:
            cur2_val = feat2.GetField(field2)
            feature_out = ogr.Feature(output_layer.GetLayerDefn())
            if cur2_val not in existingids:
                existingids.append(cur2_val)
                feature_out.SetField('GRID_ID', cur2_val)
                feature_out.SetGeometry(feat2.GetGeometryRef())
                output_layer.CreateFeature(feature_out)
            counter = counter + 1
            pbar.progress(counter, max_f, 'Geostats pop 2011: ', 'Progress:')

        counter = 0
        max_f = in3_layer.GetFeatureCount()

        for feat3 in in3_layer:
            cur3_val = feat3.GetField(field2)
            feature_out = ogr.Feature(output_layer.GetLayerDefn())
            if cur3_val not in existingids:
                existingids.append(cur3_val)
                feature_out.SetField('GRID_ID', cur3_val)
                feature_out.SetGeometry(feat3.GetGeometryRef())
                output_layer.CreateFeature(feature_out)
            counter = counter + 1
            pbar.progress(counter, max_f, 'Geostats pop 2018: ', 'Progress:')

        spinner_thread = SpinnerThread()
        print("\n reading population csv file...")
        spinner_thread.start()
        rows_2006 = self._filter_csv_file(input_csv1, existingids, 0)
        rows_2011 = self._filter_csv_file(input_csv2, existingids, 1)
        spinner_thread.stop()

        counter = 0
        max_f = output_layer.GetFeatureCount()
        for feat in output_layer:
            val1 = self._get_pop_from_gid(rows_2006, feat.GetField(0), 0, 1)
            val2 = self._get_pop_from_gid(rows_2011, feat.GetField(0), 1, 0)
            val3 = float(VectorUtils.get_attribute_value_on_overlap(
                self.shape3,
                [feat.GetGeometryRef().Centroid().GetX(), feat.GetGeometryRef().Centroid().GetY()],
                Constants.INPUT_GRID_2018_FIELD
            ))
            feat.SetField('POP06', val1)
            output_layer.SetFeature(feat)
            feat.SetField('POP11', val2)
            output_layer.SetFeature(feat)
            feat.SetField('POP18', val3)
            output_layer.SetFeature(feat)
            if val1 == 0:
                if val2 == 0:
                    feat.SetField('POP_06_11', 0)
                else:
                    feat.SetField('POP_06_11', 100)
            else:
                feat.SetField('POP_06_11', ((int(val2) / int(val1)) - 1) * 100)

            if val2 == 0:
                if val3 == 0:
                    feat.SetField('POP_11_18', 0)
                else:
                    feat.SetField('POP_11_18', 100)
            else:
                feat.SetField('POP_11_18', ((int(val3) / int(val2)) - 1) * 100)
            output_layer.SetFeature(feat)
            counter = counter + 1
            pbar.progress(counter, max_f, 'Geostats pop change creation: ', 'Progress:')
        ds = None
        out_shape = None

    @staticmethod
    def _get_pop_from_gid(rows, gid, csv_col_idx, csv_col_pop):
        ret_val = 0
        for row in rows:
            if gid == row[csv_col_idx]:
                ret_val = row[csv_col_pop]
        return ret_val

    @staticmethod
    def _filter_csv_file(input_csv, listids, gid_idx):
        reader = csv.reader(open(input_csv), delimiter=';')
        filtered = filter(lambda p: p[gid_idx] in listids, reader)
        return list(filtered)
