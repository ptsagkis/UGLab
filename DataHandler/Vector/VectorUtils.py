import ogr
import rtree
import Services.Progress as progress_bar
from DataHandler.Vector.Reproject import Reproject


class VectorUtils:
    """
    Support vector related actions
    """

    @staticmethod
    def filter_features_with_shape_extent(shape_in, shape_out, shape_mbr, intersect=False):
        """
        Filter features from shapein using the mbr of 3d argument


        :param shape_in: all features
        :param shape_out: new layer with filtered features
        :param shape_mbr: the filtering geometry. SRS of this layer will be used for the output
        :param intersect: Boolean. create the geom intersection or not
        :return:
        """
        driver = ogr.GetDriverByName('ESRI Shapefile')
        mbr_shp = driver.Open(shape_mbr, 0)
        mbr_layer = mbr_shp.GetLayer()
        mbr_extent = mbr_layer.GetExtent()
        mbr_geom = VectorUtils.extent_to_geom(mbr_extent)
        mbr_prj = mbr_layer.GetSpatialRef()

        in_shapes = driver.Open(shape_in, 0)
        in_layer = in_shapes.GetLayer()
        in_prj = in_layer.GetSpatialRef()
        if in_prj != mbr_prj:
            mbr_geom = Reproject.reproject_geometry(VectorUtils.extent_to_geom(mbr_extent), mbr_prj, in_prj)
        filtered_feats = VectorUtils.filter_feats_with_geom(shape_in, mbr_geom)
        # create the output layer
        ds = driver.CreateDataSource(shape_out)
        output_layer = ds.CreateLayer('', srs=mbr_prj, geom_type=in_layer.GetLayerDefn().GetGeomType())
        # get the first feature and copy all field names
        first_feature = in_layer.GetFeature(0)
        # paste these fields to the output file
        output_layer = VectorUtils.copy_feature_fields_to_layer(first_feature, output_layer)
        feature_out = ogr.Feature(output_layer.GetLayerDefn())
        counter = 0
        max_f = len(filtered_feats)
        pbar = progress_bar.Progress()
        for feature in filtered_feats:
            counter = counter + 1
            pbar.progress(counter, max_f, 'Filter Vector DataHandler: ', 'Progress:')
            for i in range(0, in_layer.GetLayerDefn().GetFieldCount()):
                feature_out.SetField(in_layer.GetLayerDefn().GetFieldDefn(i).GetNameRef(), feature.GetField(i))

            if in_prj == mbr_prj:
                cur_geom = feature.GetGeometryRef()
            else:
                cur_geom = Reproject.reproject_geometry(
                    feature.GetGeometryRef(),
                    in_layer.GetSpatialRef(),
                    mbr_prj)
            if intersect:
                intersection = cur_geom.Intersection(mbr_geom)
                feature_out.SetGeometry(intersection)
            else:
                feature_out.SetGeometry(cur_geom)
            output_layer.CreateFeature(feature_out)

    @staticmethod
    def filter_feats_with_geom(shp_path, geom):
        """
        Get all the features within the supplied geom
        :param shp_path:
        :param geom: geometry object
        :return: list of features
        """
        driver = ogr.GetDriverByName('ESRI Shapefile')
        features_shp = driver.Open(shp_path, 0)
        layer = features_shp.GetLayer()
        layer.SetSpatialFilter(geom)
        features = []
        for feature in layer:
            features.append(feature)
        return features

    @staticmethod
    def extent_to_geom(extent):
        """
        Convert an extent to a proper geometry polygon
        :param extent:
        :return: polygon
        """
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(extent[0], extent[2])
        ring.AddPoint(extent[1], extent[2])
        ring.AddPoint(extent[1], extent[3])
        ring.AddPoint(extent[0], extent[3])
        ring.AddPoint(extent[0], extent[2])
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)
        return poly

    @staticmethod
    def copy_feature_fields_to_layer(feature, layer):
        """
        :param feature:
        :param layer:
        :return:
        """
        [layer.CreateField(feature.GetFieldDefnRef(i)) for i in range(feature.GetFieldCount())]
        return layer

    @staticmethod
    def get_proj_from_shape(filepath):
        """
        Return the projection reference system out of the supplied file passed
        """
        shp = ogr.GetDriverByName('ESRI Shapefile').Open(filepath, 0)
        return shp.GetLayer().GetSpatialRef()

    @staticmethod
    def get_extent_from_shape(filepath):
        """
        Just return the MBR for the supplied shapefile path
        :param filepath:
        :return:
        """
        driver = ogr.GetDriverByName('ESRI Shapefile')
        mbr_shp = driver.Open(filepath, 0)
        mbr_layer = mbr_shp.GetLayer()
        return mbr_layer.GetExtent()

    @staticmethod
    def get_distance_to_nearest(x, y, shp_path, index_enable=False, deep=1):
        """
        Get the distance bewteen x,y point and closest shapefile shape
        :param x:
        :param y:
        :param shp_path:
        :param index_enable:
        :param deep:
        :return:
        """
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(x, y)
        # Create spatial reference
        out_srs = ogr.osr.SpatialReference()
        out_srs.ImportFromEPSG(3857)
        # Assign to geometry
        point.AssignSpatialReference(out_srs)
        driver = ogr.GetDriverByName('ESRI Shapefile')
        fetauresShp = driver.Open(shp_path, 0)
        fetauresLyr = fetauresShp.GetLayer()
        # if coast line holds no feature. This is for continental countries
        if fetauresLyr.GetFeatureCount() == 0:
            return 0
        else:
            if index_enable == True:
                filteredFetauresLyr = VectorUtils.filter_features_at_point(fetauresLyr, point, deep)
                dist = VectorUtils.get_minimum_dist(point, filteredFetauresLyr)
            else:
                dist = VectorUtils.get_minimum_dist(point, fetauresLyr)
        return dist

    @staticmethod
    def filter_features_at_point(layer, point, deep):
        """
        Method to filter features within the bbox constructed from point and pixel size
        incrementation until we find at least 1 feature.
        :param meters_increment: increment meters until one found
        :param layer: layer with features
        :param point: point to use in order to build the envelope
        :return:
        """
        meters = 500
        minX, maxX, minY, maxY = point.GetEnvelope()
        xmin, ymin = minX - (meters * deep), minY - (meters * deep)
        xmax, ymax = maxX + (meters * deep), maxY + (meters * deep)
        layer.SetSpatialFilterRect(xmin, ymin, xmax, ymax)
        while layer.GetFeatureCount() == 0:
            # increment the multiplier of deep
            VectorUtils.filter_features_at_point(layer, point, deep+1)
        return layer

    @staticmethod
    def get_minimum_dist(point, filtered_feats):
        """
        get the minimum distance between layer features and supplied point
        :param point: ogr geometry Point
        :param filterdLines: ogr layer
        :return: distance to nearest
        """
        dists = []
        for feat in filtered_feats:
            dists.append(point.Distance(feat.GetGeometryRef()))
        return sorted(dists)[0]

    @staticmethod
    def get_distance_to_nearest_rtree(x, y, index, featslyr):
        """
        Get the distance bewteen x,y point and closest shapefile shape
        :param x:
        :param y:
        :param index:
        :param featslyr:
        :return:
        """
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(x, y)
        # Create spatial reference
        out_srs = ogr.osr.SpatialReference()
        out_srs.ImportFromEPSG(3857)
        # Assign to geometry
        point.AssignSpatialReference(out_srs)
        feats = VectorUtils.get_features_at_envelope(point, index, featslyr)
        dist = VectorUtils.get_minimum_dist(point, feats)
        return dist


    @staticmethod
    def get_rtree_index_from_shp(shp_lyr):
        """
        pass a layer get its Rtree index back
        :param layer:
        :return:
        """
        index = rtree.index.Index(interleaved=False)
        for fid in range(0, shp_lyr.GetFeatureCount()):
            feature = shp_lyr.GetFeature(fid)
            geometry1 = feature.GetGeometryRef()
            xmin, xmax, ymin, ymax = geometry1.GetEnvelope()
            index.insert(fid, (xmin, xmax, ymin, ymax))
        return index

    @staticmethod
    def get_features_at_envelope(point, index, featslyr, multiplier=1):
        distance = 500.0 * multiplier
        xmin, xmax, ymin, ymax = point.GetEnvelope()
        search_envelope = (xmin - distance, xmax + distance, ymin - distance, ymax + distance)
        feats = []
        for fid in list(index.intersection(search_envelope)):
            feats.append(featslyr.GetFeature(fid))
        while len(feats) == 0:
            feats = VectorUtils.get_features_at_envelope(point, index, featslyr, multiplier+1)
        return feats

    @staticmethod
    def get_attribute_value_on_overlap(shp_path, geopoint, value_field, no_found_val=-100):
        """
        Get the field value for the geometry overlapping the supplied point
        :param geopoint:
        :param shp_path:
        :param point:
        :param value_field:
        :return:
        """
        driver = ogr.GetDriverByName('ESRI Shapefile')
        fetaures_shp = driver.Open(shp_path, 0)
        layer = fetaures_shp.GetLayer()
        # create point geometry
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(geopoint[0], geopoint[1])
        layer.SetSpatialFilter(point)
        retVal = no_found_val
        if layer.GetFeatureCount() > 0:
            feat = layer.GetNextFeature()
            retVal = feat.GetFieldAsString(value_field)
        return retVal
