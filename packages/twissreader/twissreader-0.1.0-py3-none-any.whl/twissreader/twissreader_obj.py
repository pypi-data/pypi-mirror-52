"""
This helperclass reads TWISS files format produced by MADX.
The header is returned as a dictionary and the data array
as a pandas dataframe.
"""
__author__ = "Christian Staufenbiel"
__date__ = "04/09/2019"
__version__ = "0.1"

import numpy as np
import pandas as pd
from .twissreader_csv import TwissReaderCSV
from .twissreader_tfs import TwissReaderTFS
from .twissreader_twiss import TwissReaderTWISS


class TwissReader():
    """ Stores the header and data of a TWISS file."""

    def __init__(self, filename, sep=','):
        """Initializing object

        Parameters
        ----------
        filename : string
            Path of Twiss-file to import
        sep : string
            Seperator used in CSV/TWISS file
        """
        # class variables
        self.header = {}
        self.data = pd.DataFrame([])
        # Check the ending
        filetype = filename.split('.')[1]
        if filetype == 'csv':
            tw = TwissReaderCSV(filename, sep=sep)
        elif filetype == 'tfs':
            tw = TwissReaderTFS(filename)
        elif filetype == 'twiss':
            tw = TwissReaderTWISS(filename,sep=sep)
        else:
            raise NotImplementedError('TwissReader: Filetype {} not recognized.'.format(filetype))

        # Copy data and header to this object
        self.data = tw.data
        self.header = tw.header

    def __getitem__(self, key):
        """Returns item with given key. Tries to get from DataFrame, if fails
        from the header dictionary.

        Parameters
        ----------
        key : index key
            possible keys for pandas DataFrame or dictionary

        Returns
        -------
        Item
            Depending on key
        """
        # If there are several keys (tuple) it's probably meant to go in the dataframe
        if isinstance(key, tuple):
            return self.data.loc[key]
        try:
            return self.data[key]
        except:
            pass
        try:
            return self.header[key]
        except:
            raise RuntimeError('Could not find key "{}" in TwissFile.'.format(key))

    def find_element(self, search_string):
        """Searches for an element in Twiss-file of the object.
        Parameters
        ----------
        search_string : string
            Search string. Wildcard % can be used.
        Returns
        -------
        list
            List of strings that contain the search_string.
        """
        keys = search_string.split('%')
        matches = []
        for elem in self.data.index:
            tmp = [key in elem for key in keys]
            if not False in tmp:
                matches.append(elem)
        return matches

    def find_variable(self, search_string):
        """ Searches for a variable in the TwissFile, that is stored for each element.

        Parameters
        ----------
        search_string : string
            Search string. Wildcard % can be used.

        Returns
        -------
        list
            List of strings that containt the search_string.
        """
        keys = search_string.split('%')
        matches = []
        # Search in columns of the dataframe
        for var in self.data.columns:
            tmp = [key in var for key in keys]
            if not False in tmp:
                matches.append(var)
        # Search in header dictionary
        for var in self.header.keys():
            tmp = [key in var for key in keys]
            if not False in tmp:
                matches.append(var)
        # Return found matches
        return matches


if __name__ == '__main__':
    print('running twissreader.py')
