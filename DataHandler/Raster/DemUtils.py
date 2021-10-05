from osgeo import gdal


class DemUtils:
    """
    Place here any methods related to dem products
    """
    @staticmethod
    def create_dem_product(target, source, type):
        """
        Create the desired product
        :param target:
        :param source:
        :param type: may be slope, aspect or hillshade
        :return:
        """
        gdal.DEMProcessing(target, source, type)
