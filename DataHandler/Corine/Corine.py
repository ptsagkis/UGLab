import gdal
import numpy as np


class Corine:
    """
    A class to support the reclassification process for the corine dataset

    self.newClasses1
    code	description
    1	High dense urban – already urban so attracts urban
    2	Low dense urban - already urban so attracts urban
    3	Industrial
    4	Transport
    5	Agriculture – free to urbanize
    6	Forest – free to urbanize
    7	Water
    8	Sea / Oceans – no change to urbanize but may attract urbanization

    self.newClasses1
    code	description
    0	No-Urban
    1	Urban

    """

    def __init__(self):
        self.corineClasses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                              15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                              30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48]

        self.newClasses1 = [1, 2, 3, 4, 4, 4, 3, 3, 3, 2, 2, 5, 5, 5,
                       5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6,
                       6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, -9999]

        self.newClasses2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -9999]

    def raster_reclass(self, file, files_out):
        """
        CORINE DATASET
        Reclass supplied raster
        Values to reclass are hardcoded inside filter property
        """
        new_classes = [self.newClasses1, self.newClasses2]
        # do some check ... just in case
        if len(self.corineClasses) != len(self.corineClasses):
            raise Exception('Reclass list should have equal length: {}'.format(len(self.corineClasses)))
        driver = gdal.GetDriverByName('GTiff')
        raster = gdal.Open(file)
        band = raster.GetRasterBand(1)
        counter = 0
        for newCls in new_classes:
            pixels = band.ReadAsArray()
            class_index = 0
            for old_class in self.corineClasses:
                pixels[np.where(pixels == old_class)] = newCls[class_index]
                class_index = class_index + 1

            raster_out = driver.Create(files_out[counter], raster.RasterXSize, raster.RasterYSize, 1, gdal.GDT_Float32)
            raster_out.SetGeoTransform(raster.GetGeoTransform())
            raster_out.SetProjection(raster.GetProjectionRef())
            raster_out.GetRasterBand(1).WriteArray(pixels)
            raster_out.FlushCache()
            counter = counter + 1
        raster.FlushCache()
