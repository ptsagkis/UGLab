import requests
import Services.Progress as progress_bar
from DataHandler.Vector.Reproject import Reproject
from DataHandler.Vector.VectorUtils import VectorUtils
import numpy as np
from osgeo import ogr, osr


class OsmUtils:
    """
    Place here any OSM related methods
    We use the overpass api to query OSM data
    Following cases has been covered
    1. For the street network
    2. For urban sub-centers
    3. For amenities

    node[place~"city|town|village|hamlet|suburb"]
    """

    def __init__(self):
        self.OVERPASS_EPSG = 4326

        self.ROAD_TYPES = {
            'motorway': 1,
            'motorway_link': 1,
            'trunk': 2,
            'trunk_link': 2,
            'primary': 3,
            'primary_link': 3,
            'secondary': 4,
            'secondary_link': 4,
            'tertiary': 5,
            'tertiary_link': 5,
            'unclassified': 6,
            'residential': 7,
        }
        self.ROADS_QUERY = '|'.join(self.ROAD_TYPES.keys())

        self.SUB_CENTER_TYPES = {
            'city': 1,
            'town': 2,
            'village': 3,
            'hamlet': 4,
            'suburb': 2
        }
        self.SUB_CENTER_QUERY = '|'.join(self.SUB_CENTER_TYPES.keys())

    def download_urban_subcenters(self, shape_mbr, shape_out):
        """
        Download and parse area subcenters
        :param shape_mbr:
        :param shape_out: POINTS with SUB_CENTER_TYPES
        :return:
        """
        mbr_prj = VectorUtils.get_proj_from_shape(shape_mbr)
        x_min, x_max, y_min, y_max = self._get_osm_mbr_from_shape(shape_mbr)
        mbr_string = str(x_min) + ',' + str(y_min) + ',' + str(x_max) + ',' + str(y_max)
        print('Downloading OSM places data for mbr_extent ....... :' + mbr_string)
        overpass_url = 'http://overpass-api.de/api/interpreter'
        overpass_query = '[out:json];node[place~"^(' + self.SUB_CENTER_QUERY + ')$"](' + mbr_string + ');(._;>;);out meta;'
        response = requests.get(overpass_url, params={'data': overpass_query})
        nodes = self._parse_overpass_urban_subcenters_response(response)
        print('DataHandler(sub centers) downloaded!.' + str(nodes) + 'Preparing data......')
        driver = ogr.GetDriverByName('ESRI Shapefile')
        ds = driver.CreateDataSource(shape_out)
        output_layer = ds.CreateLayer('SUB_CENTERS', srs=mbr_prj, geom_type=ogr.wkbPoint)
        field_type = ogr.FieldDefn('type', ogr.OFTInteger)
        field_type.SetWidth(2)
        output_layer.CreateField(field_type)
        counter = 0
        max_f = len(nodes)
        prog_bar = progress_bar.Progress()
        for node in nodes:
            counter = counter + 1
            prog_bar.progress(counter, max_f, 'Convert OSM (place) data to shapefile: ', 'Progress:')
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(node[1], node[2])
            feature_out = ogr.Feature(output_layer.GetLayerDefn())
            feature_out.SetField('type', self.SUB_CENTER_TYPES[node[0]])
            feature_out.SetGeometry(
                Reproject.reproject_geometry(point, self._get_overpass_spatial_ref(), mbr_prj))
            output_layer.CreateFeature(feature_out)

    def download_streets(self, shape_mbr, shape_out):
        """
        Download and parse
        :param shape_mbr: Just any shapefile whose mbr will be used to filter osm data
        and its spatial ref for the output spatial ref
        :param shape_out: the output shapefile POLYLINES
        :return: void
        """
        mbr_prj = VectorUtils.get_proj_from_shape(shape_mbr)
        x_min, x_max, y_min, y_max = self._get_osm_mbr_from_shape(shape_mbr)
        mbr_string = str(x_min) + ',' + str(y_min) + ',' + str(x_max) + ',' + str(y_max)
        print('Downloading OSM street data for mbr_extent ....... :' + mbr_string)
        overpass_url = 'http://overpass-api.de/api/interpreter'
        overpass_query = '[out:json];way[highway][highway~"^(' + self.ROADS_QUERY + ')$"](' + mbr_string + ');(._;>;);out meta;'
        print('overpass_query' + overpass_query)
        response = requests.get(overpass_url, params={'data': overpass_query})
        print('DataHandler downloaded!.' + str(response) + 'Preparing data......')
        nodes, ways = self._parse_overpass_streets_response(response)
        # output layer
        driver = ogr.GetDriverByName('ESRI Shapefile')
        ds = driver.CreateDataSource(shape_out)
        output_layer = ds.CreateLayer('STREET_NET', srs=mbr_prj, geom_type=ogr.wkbLineString)
        field_type = ogr.FieldDefn('type', ogr.OFTInteger)
        field_type.SetWidth(2)
        output_layer.CreateField(field_type)
        self._build_street_net(output_layer, ways, nodes, mbr_prj)

    @staticmethod
    def _parse_overpass_urban_subcenters_response(response):
        """
        parse the overpass response
        return places as nodes
        :param response:
        :return:
        """
        data = response.json()
        nodes = []
        for element in data['elements']:
            if element['type'] == 'node':
                nodes.append([
                    element['tags']['place'],
                    element['lat'],
                    element['lon']
                ])
        return nodes

    @staticmethod
    def _parse_overpass_streets_response(response):
        """
        parse the overpass response
        return nodes and ways found
        :param response:
        :return:
        """
        data = response.json()
        nodes = []
        ways = []
        for element in data['elements']:
            if element['type'] == 'node':
                nodes.append([
                    element['id'],
                    element['lat'],
                    element['lon']
                ])
            if element['type'] == 'way':
                ways.append({'nodes': element['nodes'], 'type': element['tags']['highway']})
        return [nodes, ways]

    @staticmethod
    def _get_line_from_way(way, nodes):
        """
        Get the way and all the possible nodes.
        Filter nodes using those included in the way branch
        Build the line using the filtered nodes
        :param way:
        :param nodes:
        :return: ogr.wkbLineString
        """
        node_ids = way['nodes']
        filtered_nodes = []
        for nd_id in node_ids:
            filtered_nodes.append(nodes[nodes[:, 0] == nd_id])
        line = ogr.Geometry(type=ogr.wkbLineString)
        for node in filtered_nodes:
            line.AddPoint(node[0][1], node[0][2])
        return line

    @staticmethod
    def _build_street_net(output_layer, ways, nodes, mbr_prj):
        """
        Build lines from ways and nodes
        Display a progress bar for process
        This is a long process.
        :param output_layer:
        :param ways:
        :param nodes:
        :param mbr_prj:
        :return:
        """
        # convert node list to np array to speed up things
        np_nodes = np.array(nodes)
        counter = 0
        max_f = len(ways)
        prog_bar = progress_bar.Progress()
        # build the lines
        for way in ways:
            counter = counter + 1
            prog_bar.progress(counter, max_f, 'Convert OSM (streets) data to shapefile: ', 'Progress:')
            line = OsmUtils._get_line_from_way(way, np_nodes)
            feature_out = ogr.Feature(output_layer.GetLayerDefn())
            feature_out.SetField('type', OsmUtils.ROAD_TYPES[way['type']])
            feature_out.SetGeometry(
                Reproject.reproject_geometry(line, OsmUtils._get_overpass_spatial_ref(), mbr_prj).Simplify(10)
            )
            output_layer.CreateFeature(feature_out)

    @staticmethod
    def _get_osm_mbr_from_shape(shape_mbr):
        """
        Get the supplied shp mbr and convert it
        to geometry + reproject to epsg:4326
        :param shape_mbr:
        :return:
        """
        driver = ogr.GetDriverByName('ESRI Shapefile')
        mbr_shp = driver.Open(shape_mbr, 0)
        mbr_layer = mbr_shp.GetLayer()
        mbr_prj = mbr_layer.GetSpatialRef()
        mbr_extent = mbr_layer.GetExtent()
        mbr_geom = VectorUtils.extent_to_geom(mbr_extent)
        output_spatial_ref = OsmUtils._get_overpass_spatial_ref()
        return Reproject.reproject_geometry(mbr_geom, mbr_prj, output_spatial_ref).GetEnvelope()

    @staticmethod
    def _get_overpass_spatial_ref():
        """
        Get the spatial ref from epsg code --> @OVERPASS_EPSG 4326
        :return:
        """
        output_spatial_ref = osr.SpatialReference()
        output_spatial_ref.ImportFromEPSG(__class__().OVERPASS_EPSG)
        return output_spatial_ref
