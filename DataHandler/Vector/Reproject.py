from osgeo import osr


class Reproject:
    """
    Just static methods to support geometry reprojections
    """

    @staticmethod
    def reproject_geometry(geometry, epsgfrom, epsgto):
        """
        Trasforms a geometry to new projection
        :param epsgfrom:
        :param epsgto:
        :param geometry:
        :return:
        """
        try:
            transform = osr.CoordinateTransformation(epsgfrom, epsgto)
            geometry.Transform(transform)
            return geometry
        except Exception as e:
            print('Reproject Error: %s' % str(e))
            raise e
