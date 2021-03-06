from osgeo import gdal
import ogr
import numpy as np
import scipy
from Services.FileUtils import FileUtils


class RasterUtils:
    """
    Generic static methods for raster support
    """

    @staticmethod
    def crop_raster_to_shape(in_img, out_img, crop_shp, buffer=0):
        """
        Crop raster using the supplied shapefile
        Add a buffer if needed is the buffer param
        :param in_img:
        :param out_img:
        :param crop_shp:
        :param buffer: @default 0
        :return:
        """
        driver = ogr.GetDriverByName('ESRI Shapefile')
        input_file = driver.Open(crop_shp, 0)
        input_layer = input_file.GetLayer()
        x_min, x_max, y_min, y_max = input_layer.GetExtent()
        spatial_ref = input_layer.GetSpatialRef()
        auth_code = spatial_ref.GetAuthorityCode(None)
        auth_name = spatial_ref.GetAuthorityName(None)
        ds = gdal.Open(in_img)
        gdal.Translate(out_img, ds, projWinSRS=auth_name + ':' + auth_code,
                       projWin=[x_min - buffer, y_max + buffer, x_max + buffer, y_min - buffer])
        # ds = None

    @staticmethod
    def geocoords_from_pix(geotrans, x, y):
        """
        :param geotrans: dataset.GetGeoTransform()
        :param x: x image idx (width)
        :param y: y image ids (height_
        :return:
        """
        posX = geotrans[0] + x * geotrans[1] + y * geotrans[2]
        posY = geotrans[3] + x * geotrans[4] + y * geotrans[5]
        return posX + (geotrans[1] / 2), posY + (geotrans[5] / 2)

    @staticmethod
    def get_raster_array_from_image(raster, band_idx):
        """
        pass the image and the band you want to grab
        get it back a 2d array
        :param band_idx: 
        :param raster:
        :return:
        """
        dataset = gdal.Open(raster)
        band = dataset.GetRasterBand(band_idx)
        raster_arr = band.ReadAsArray()
        return raster_arr

    @staticmethod
    def get_raster_value_at_geopoint(raster_in, point):
        """
        get the raster value supplied geopoint falls in
        :param raster_in:
        :param point:
        :return:
        """
        dataset = gdal.Open(raster_in)
        gt = dataset.GetGeoTransform()
        rb = dataset.GetRasterBand(1)
        mx, my = point[0], point[1]  # coord in map units
        # Convert from map to pixel coordinates.
        # Only works for geotransforms with no rotation.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
        return rb.ReadAsArray(px, py, 1, 1)[0][0]


    @staticmethod
    def get_neighbors_values(rast, radius, row, col):
        """
        Get the footprint of the supplied pixel position.
        For the case of radius 1
        1 2 3
        4 x 5
        6 7 8
        :param raster_arr: the raster image to get values from
        :param position: the pixel position (height/width)
        :param radius: the depth of pixel collection
        radius value of 1 leads to a 3x3 matrix.
        radius value of 2 leads to a 5x5 matrix.
        .....
        etc.
        :return:
        """
        matrix = scipy.array(rast)
        indices = tuple(scipy.transpose(scipy.atleast_2d([row,col])))
        arr_shape = scipy.shape(matrix)
        dist = scipy.ones(arr_shape)
        dist[indices] = 0
        dist = scipy.ndimage.distance_transform_cdt(dist, metric='chessboard')
        nb_indices = []
        for level in range(radius):
            nb_indices.extend(scipy.transpose(scipy.nonzero(dist == level+1)))
        return list(map(int, [matrix[tuple(ind)] for ind in nb_indices]))


    @staticmethod
    def count_value_on_matrix(matrix, value):
        """
        Count
        :param matrix:
        :param value:
        :return:
        """
        return matrix.count(value)

    @staticmethod
    def reproject_raster(filein, fileout, epsg_code):
        """
        just pure raster reprojection
        :param filein:
        :param fileout:
        :param epsg_code:
        :return:
        """
        warp = gdal.Warp(fileout, filein, dstSRS='EPSG:' + epsg_code)
        warp = None  # Closes the files

    @staticmethod
    def crop_reproject_raster(in_raster, out_raster, cutline_shape, epsg_code):
        """
        crop the supplied raster using shape
        reproject the cropped raster
        :param in_raster:
        :param out_raster:
        :param cutline_shape:
        :param epsg_code:
        :return:
        """
        warp = gdal.Warp(out_raster, in_raster, cutlineDSName=cutline_shape, cropToCutline=True,
                         dstSRS='EPSG:' + epsg_code)
        warp = None  # Closes the files

    @staticmethod
    def create_raster_from_csv(csvinput, dataIndex, rasterIn, rastOut):
        modelData = np.loadtxt(csvinput, delimiter=';')
        x_coords = modelData[:, 0]
        y_coords = modelData[:, 1]
        predictVals = modelData[:, dataIndex]

        dataset = gdal.Open(rasterIn)
        band = dataset.GetRasterBand(1)
        rasterArr = band.ReadAsArray()

        for i in range(len(x_coords)):
            point = x_coords[i], y_coords[i]
            x_index = RasterUtils.get_index_coord_from_geocoords(rasterIn, point)[1]
            y_index = RasterUtils.get_index_coord_from_geocoords(rasterIn, point)[0]
            if rasterArr[x_index, y_index] == 0 and predictVals[i] == 1:
                rasterArr[x_index, y_index] = 2

            elif rasterArr[x_index, y_index] == 1 and predictVals[i] == 0:
                rasterArr[x_index, y_index] = 3

        driver = gdal.GetDriverByName('GTiff')
        dst_filename = rastOut
        FileUtils.delete_file(dst_filename)
        dst_ds = driver.Create(dst_filename, band.XSize, band.YSize, 1, gdal.GDT_Float64)

        dst_ds.SetGeoTransform(dataset.GetGeoTransform())
        dst_ds.SetProjection(dataset.GetProjectionRef())
        dst_ds.GetRasterBand(1).WriteArray(rasterArr)

    @staticmethod
    def get_index_coord_from_geocoords(rasterIn, point):
        '''

        :param rasterIn:
        :param point:
        :return:
        '''
        dataset = gdal.Open(rasterIn)
        gt = dataset.GetGeoTransform()
        rb = dataset.GetRasterBand(1)
        mx, my = point[0], point[1]  # coord in map units
        # Convert from map to pixel coordinates.
        # Only works for geotransforms with no rotation.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
        return px, py

    @staticmethod
    def raster_changes_matrix(rast1, rast2, output_csv):
        """
        Present a change value matrix into csv format
        For each raster we get the distinct pixel values
        and we map changes from raster1 to raster2 into a 2d matrix
        :param output_csv:
        :param rast1:
        :param rast2:
        :output_csv: the path to save in csv format the 2d changes matrix
        """
        raster_arr1 = RasterUtils.get_raster_array_from_image(rast1, 1)
        unique_vals1 = np.unique(raster_arr1)

        raster_arr2 = RasterUtils.get_raster_array_from_image(rast2, 1)
        unique_vals2 = np.unique(raster_arr2)

        # create the matrix full filled with zeros
        matrix = np.zeros((len(unique_vals1), len(unique_vals2)))
        # populate the matrix with counts of each unique value (change from --> to)
        print('len(raster_arr1)' + str(len(raster_arr1)))
        print('len(raster_arr1)' + str(len(raster_arr1)))
        for y in range(len(raster_arr1)):
            for x in range(len(raster_arr1[y])):
                s1 = np.where(unique_vals1 == raster_arr1[y][x])[0][0]
                s2 = np.where(unique_vals2 == raster_arr2[y][x])[0][0]
                matrix[s1][s2] = matrix[s1][s2] + 1
        # Draw the labels and both axes
        unique_vals1.shape = (len(unique_vals1), 1)
        matrix = np.hstack((unique_vals1, matrix))
        print('unique_vals2', unique_vals2)
        row = np.insert(unique_vals2, 0, -9999)
        matrix = np.vstack([row, matrix])
        np.savetxt(output_csv, matrix.astype(int), delimiter=',', fmt='%s')
