"""
This helperclass reads TWISS files in TFS format produced by MADX.
See more information in twissreader.py.
"""
__author__ = "Christian Staufenbiel"
__date__ = "03/09/2019"
__version__ = "0.1"

import pandas as pd
import shlex


class TwissReaderTFS():
    """ Stores the header and data of a TWISS file. """

    def __init__(self, filename):
        """Initialize object
        Parameters
        ----------
        filename : string
            Path to twiss file
        """
        # Open file
        s = self.__readfile(filename)
        # Get header dict, and data DataFrame
        self.header, self.data = self.__split_header_data(s)

    def __readfile(self, filename):
        """ Reads content of twiss file

        Parameters
        ----------
        filename : string
            Path to twiss file
        """
        # Try to open file
        try:
            f = open(filename, 'r')
        except FileNotFoundError:
            print('TwissReader: The file {} was not found!'.format(filename))
            raise
        # Read strng from file and return
        res = f.read()
        f.close()
        return res

    def __split_header_data(self, s):
        """ Splits header and data of twiss file and stores as dict / DataFrame
        Parameters
        ----------
        s : list (strings)
            String of twiss file split by each row

        Returns
        -------
        tuple (dictionary, pandas.DataFrame)
            Return dict containing header data and pandas.DataFrame containing
            data of all elements.
        """
        # Split lines
        lines = s.split('\n')

        # Find index of data description, i.e. end of header
        # We assume that the data description row starts with an *
        data_desc_idx = 0
        for i, line in enumerate(lines):
            if len(line) > 0 and line[0] == '*':
                data_desc_idx = i
        if not data_desc_idx:
            raise RuntimeError('TwissReaderTFS: Couldnt find data description line!')

        # Take all header lines and store in the header dictionary
        header = {}
        for line in lines[0:data_desc_idx]:
            if len(line) == 0 or line[0] != '@':
                continue
            # Split at all spaces
            line = shlex.split(line)
            # Remove all empty strings from line list
            line = list(filter(lambda x: x != '', line))
            # Get key and value from the line
            key = line[1]
            val = line[-1].replace('"', '')
            # Try to convert to float if possible
            try:
                val = float(val)
            except:
                pass
            # Add key/val-pair to header
            header[key] = val

        # Get all column names for the dataframe
        line = lines[data_desc_idx]
        # delete star from the data description line
        line = line[1:]
        line = line.split(' ')
        # Delete all empty strings from list -> column names
        columns = list(filter(lambda x: x != '', line))
        # Run trough all data lines and add data to array
        data = []
        for line in lines[data_desc_idx+2:]:
            # Continue on empty lines
            if len(line) == 0:
                continue
            # Remove all " amd split on spaces
            line = line.replace('"', '')
            line = line.split(' ')
            # Delete empty string elements from list
            line = list(filter(lambda x: x != '', line))
            # Try to convert to float
            for i, val in enumerate(line):
                try:
                    line[i] = float(val)
                except:
                    pass
            # append to data
            data.append(line)

        # Create dataframe
        data = pd.DataFrame(data, columns=columns)
        # Set index to elements in MADX
        data = data.set_index(columns[0])
        # Return header dict and data DataFrame
        return header, data
