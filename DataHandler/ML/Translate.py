import ogr
import csv
import gdal
from DataHandler.Raster.RasterUtils import RasterUtils
from DataHandler.Vector.VectorUtils import VectorUtils
from Services.FileUtils import FileUtils

from Services.Progress import Progress


class Translate:
    """
    This is the final step to create the Machine Learning Dataset
    from the different spatial sources
    """
    @staticmethod
    def spatial_to_ml(
                                           filein_step1_c2,
                                           filein_step1_c1,
                                           filein_step2_c2,
                                           filein_step2_c1,
                                           filein_step3_c2,
                                           filein_step3_c1,
                                           filein_step4_c2,
                                           filein_step4_c1,
                                           road_net_shp,
                                           urban_centers_shp,
                                           coast_line_shp,
                                           pop_shp,
                                           pop_shp_field,
                                           height_dem,
                                           slope_dem,
                                           hillshade_dem,
                                           aspect_dem,
                                           output_csv1,
                                           output_csv2,
                                           output_csv3):
        """

        :param filein_step1_c2: corine reclass code2 2000
        :param filein_step1_c1: corine reclass code1 2000
        :param filein_step2_c2: corine reclass code2 2006
        :param filein_step2_c1: corine reclass code1 2006
        :param filein_step3_c2: corine reclass code2 2012
        :param filein_step3_c1: corine reclass code1 2012
        :param filein_step4_c2: corine reclass code2 2018
        :param filein_step4_c1: corine reclass code1 2018
        :param road_net_shp: road netwrok shapefile
        :param urban_centers_shp: urban centers shapefile
        :param coast_line_shp: cooast line shapefile
        :param pop_shp: population shapefile
        :param pop_shp_field: population shapefile field to get trending value
        :param height_dem: DEM
        :param slope_dem: SLope
        :param hillshade_dem: hillshade
        :param aspect_dem: aspect
        :param output_csv1: csv for the period 2000-2006
        :param output_csv2: csv for the period 2006-2012
        :param output_csv3: csv for the period 2012-2018
        :return:
        """

        raster_arr1_c2 = RasterUtils.get_raster_array_from_image(filein_step1_c2, 1)
        raster_arr1_c1 = RasterUtils.get_raster_array_from_image(filein_step1_c1, 1)
        raster_arr2_c2 = RasterUtils.get_raster_array_from_image(filein_step2_c2, 1)
        raster_arr2_c1 = RasterUtils.get_raster_array_from_image(filein_step2_c1, 1)
        raster_arr3_c2 = RasterUtils.get_raster_array_from_image(filein_step3_c2, 1)
        raster_arr3_c1 = RasterUtils.get_raster_array_from_image(filein_step3_c1, 1)
        raster_arr4_c2 = RasterUtils.get_raster_array_from_image(filein_step4_c2, 1)
        raster_arr4_c1 = RasterUtils.get_raster_array_from_image(filein_step4_c1, 1)
        FileUtils.delete_file(output_csv1)
        FileUtils.delete_file(output_csv2)
        FileUtils.delete_file(output_csv3)

        # get the GeoTransform from first image for later usage
        dataset = gdal.Open(filein_step1_c2)
        geotrans = dataset.GetGeoTransform()

        # get the street features
        driver = ogr.GetDriverByName('ESRI Shapefile')
        streets_shp = driver.Open(road_net_shp, 0)
        streets_layer = streets_shp.GetLayer()
        # create Rtree spatial index to speed up road network dists
        road_net_rtree = VectorUtils.get_rtree_index_from_shp(streets_layer)

        # use a progress bar to monitor
        prog_bar = Progress()
        counter = 0
        max_f = len(raster_arr1_c2)

        for y in range(len(raster_arr1_c2)):
            counter = counter + 1
            prog_bar.progress(counter, max_f, 'Converting spatial data to tabular: ', 'Progress:')
            for x in range(len(raster_arr1_c2[y])):
                if raster_arr1_c2[y][x] != -9999 and raster_arr2_c2[y][x] != -9999 and raster_arr3_c2[y][x] != -9999 and \
                        raster_arr4_c2[y][x] != -9999 \
                        and raster_arr1_c1[y][x] != 0 and raster_arr1_c1[y][x] != 0 and raster_arr3_c1[y][x] != 0:
                    # get the coords
                    geopoint = RasterUtils.geocoords_from_pix(geotrans, x, y)
                    # get the distance to closest road. Use the spatial index @road_net_rtree to speed up things
                    dist_road_net = VectorUtils.get_distance_to_nearest_rtree(
                        geopoint[0],
                        geopoint[1],
                        road_net_rtree,
                        streets_layer)
                    # the distance the closest urban center
                    dist_urban_center = VectorUtils.get_distance_to_nearest(
                        geopoint[0],
                        geopoint[1],
                        urban_centers_shp)
                    # the distance to coast line
                    dist_coast_line = VectorUtils.get_distance_to_nearest(
                        geopoint[0],
                        geopoint[1],
                        coast_line_shp, False)
                    # height val
                    height_val = RasterUtils.get_raster_value_at_geopoint(
                        height_dem,
                        geopoint
                    )
                    # slope val
                    slope_val = RasterUtils.get_raster_value_at_geopoint(
                        slope_dem,
                        geopoint
                    )
                    # hillshade val
                    hillshade_val = RasterUtils.get_raster_value_at_geopoint(
                        hillshade_dem,
                        geopoint
                    )
                    # aspect val
                    aspect_val = RasterUtils.get_raster_value_at_geopoint(
                        aspect_dem,
                        geopoint
                    )
                    # population change val
                    pop_val = float(VectorUtils.get_attribute_value_on_overlap(
                        pop_shp,
                        geopoint,
                        pop_shp_field
                    ))
                    # surrounding environment in terms of land use
                    count_definitions = [1, 2, 3, 4, 5, 6, 7, 8]
                    count_vals1 = []
                    neigh_vals1 = RasterUtils.get_neighbor_values(raster_arr1_c1, [y, x], 1)
                    count_vals2 = []
                    neigh_vals2 = RasterUtils.get_neighbor_values(raster_arr2_c1, [y, x], 1)
                    count_vals3 = []
                    neigh_vals3 = RasterUtils.get_neighbor_values(raster_arr3_c1, [y, x], 1)
                    count_vals4 = []
                    neigh_vals4 = RasterUtils.get_neighbor_values(raster_arr4_c1, [y, x], 1)

                    for val in count_definitions:
                        count_val1 = RasterUtils.count_value_on_matrix(neigh_vals1, val)
                        count_vals1.append(count_val1)
                        count_val2 = RasterUtils.count_value_on_matrix(neigh_vals2, val)
                        count_vals2.append(count_val2)
                        count_val3 = RasterUtils.count_value_on_matrix(neigh_vals3, val)
                        count_vals3.append(count_val3)
                        count_val4 = RasterUtils.count_value_on_matrix(neigh_vals4, val)
                        count_vals4.append(count_val4)

                    data_row1 = [
                                    round(geopoint[0], 2),
                                    round(geopoint[1], 2),
                                    round(int(dist_road_net)),
                                    round(int(dist_urban_center)),
                                    round(int(dist_coast_line)),
                                    round(int(height_val)),
                                    round(int(slope_val)),
                                    round(int(hillshade_val)),
                                    round(int(aspect_val)),
                                    round(int(pop_val))
                                ] + count_vals1 + [raster_arr1_c1[y][x], raster_arr1_c2[y][x],
                                                   int(raster_arr3_c2[y][x])]

                    data_row2 = [
                                    round(geopoint[0], 2),
                                    round(geopoint[1], 2),
                                    round(int(dist_road_net)),
                                    round(int(dist_urban_center)),
                                    round(int(dist_coast_line)),
                                    round(int(height_val)),
                                    round(int(slope_val)),
                                    round(int(hillshade_val)),
                                    round(int(aspect_val)),
                                    round(int(pop_val))
                                ] + count_vals2 + [raster_arr2_c1[y][x], raster_arr2_c2[y][x],
                                                   int(raster_arr4_c2[y][x])]

                    data_row3 = [
                                    round(geopoint[0], 2),
                                    round(geopoint[1], 2),
                                    round(int(dist_road_net)),
                                    round(int(dist_urban_center)),
                                    round(int(dist_coast_line)),
                                    round(int(height_val)),
                                    round(int(slope_val)),
                                    round(int(hillshade_val)),
                                    round(int(aspect_val)),
                                    round(int(pop_val))
                                ] + count_vals3 + [raster_arr4_c1[y][x], raster_arr4_c2[y][x]]

                    # Open file in append mode
                    with open(output_csv1, 'a+', newline='') as pix_file1, \
                            open(output_csv2, 'a+', newline='') as pix_file2, \
                            open(output_csv3, 'a+', newline='') as pix_file3:
                        pixel_writer1 = csv.writer(pix_file1, delimiter=';', quotechar='"',
                                                   quoting=csv.QUOTE_MINIMAL)
                        pixel_writer2 = csv.writer(pix_file2, delimiter=';', quotechar='"',
                                                   quoting=csv.QUOTE_MINIMAL)
                        pixel_writer3 = csv.writer(pix_file3, delimiter=';', quotechar='"',
                                                   quoting=csv.QUOTE_MINIMAL)
                        # finally write pixel values to the csv files
                        pixel_writer1.writerow(data_row1)
                        pixel_writer2.writerow(data_row2)
                        pixel_writer3.writerow(data_row3)
