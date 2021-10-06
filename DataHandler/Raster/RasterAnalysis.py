from osgeo import gdal
import numpy as np

import DataHandler.Raster.RasterUtils as rast_utils
import Services.FileUtils as file_utils

class RasterAnalysis:
    """
    A class to record the changes taking place among to time series steps

    """
    @staticmethod
    def raster_changes_matrix(rast1, rast2, output_csv):
        """
        Present a change value matrix into csv format
        For each raster we get the distinct pixel values
        and we map changes from raster1 to raster2 into a 2d matrix
        :param rast1:
        :param rast2:
        :output_csv: the path to save in csv format the 2d changes matrix
        """
        raster_arr1 = rast_utils.RasterUtils.get_raster_array_from_image(rast1, 1)
        unique_vals1 = np.unique(raster_arr1)

        raster_arr2 = rast_utils.RasterUtils.get_raster_array_from_image(rast2, 1)
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
