import os
import numpy as np


class FileUtils:
    """
    Some static methods to support file/ folder delete and creation
    """
    @staticmethod
    def create_dir(path):
        """
        Create a directory if it doesnt exist
        :param path:
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def delete_file(path):
        """
        delete the file for the passed filepath
        :param path:
        :return:
        """
        if os.path.exists(path):
            os.remove(path)
        else:
            print("The file to delete does not exist")

    @staticmethod
    def save_nparray_to_csv(data, path):
        """
        save a 2d array into csv excel format
        :param data:
        :param path:
        :return:
        """
        np.savetxt(path, data, delimiter=',', fmt='%s')

    @staticmethod
    def save_dictionary_to_csv(data, path):
        """
        save the supplied dictionary on csv format
        :param data:
        :param path:
        :return:
        """
        with open(path, 'w') as f:
            for key in data.keys():
                f.write("%s,%s\n" % (key, data[key]))