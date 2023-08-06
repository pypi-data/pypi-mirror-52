__author__ = "Christian Staufenbiel"
__date__ = "16/09/2019"
__version__ = "0.0.1"

import numpy as np
import pandas as pd
import shlex


class TwissReaderTWISS():
    """ Stores the header and data of a TWISS file stored with .twiss extension """

    def __init__(self, filename, sep=' '):
        """Initializes object
        Parameters
        ----------
        filename : string
            path to file
        sep : string
            seperator used in file
        """
        # Initialize empty datastorage
        self.header = {}
        self.data = pd.DataFrame([])
        # Open file
        s = self.__readfile(filename)
        self.__split_header_data(s, sep=sep)

    def __readfile(self, filename):
        """Reads file with .twiss extension
        Parameters
        ----------
        filename : string
            path to file
        Returns
        -------
        string
            Content of twiss file
        """
        # Try to open file
        try:
            f = open(filename, 'r')
        except FileNotFoundError:
            print('TwissReader: The file {} was not found!'.format(filename))
            raise
        # Read string from file and return
        res = f.read()
        f.close()
        return res

    def __split_header_data(self, s, sep):
        """ Splits string of twiss file to header and data.
        Parameters
        ----------
        s : string
            String of a twiss file
        sep : string
            seperator used in the file

        Returns
        -------
        type
            Description of returned object.
        """
        # split on linebreak
        split = s.split('\n')
        # Find line that starts with an asterisk, as it seperates header and data
        descr_data_idx = -1
        for i, line in enumerate(split):
            try:
                line = line.replace(" ", "")
                if line[0] == '*':
                    descr_data_idx = i
            except:
                pass

        # Raise error if data description line was not found
        if descr_data_idx == -1:
            raise RuntimeError('TwissReader: Could not find data description row! \n  \
                                Row must start with asterisk (*)')
        # Set indices of start and end of header
        header_start_idx = 0
        header_end_idx = descr_data_idx-1

        # Set indices of start and end of data
        data_start_idx = descr_data_idx+2
        data_end_idx = len(split)-2

        # Create header dictionary
        self.header = self.__create_dictionary(split, header_start_idx, header_end_idx, sep=sep)
        # Create pandas dataframe for data
        self.data = self.__create_dataframe(
            split, descr_data_idx, data_start_idx, data_end_idx, sep=sep)

    def __create_dictionary(self, split, start_idx, end_idx, sep):
        """Creates header dictionary from split and given indices
        Parameters
        ----------
        split : list(strings)
            List of rows in TWISS file
        start_idx : int
            Start index for header
        end_idx : int
            End index for header
        sep : string
            Seperator used in the file
        Returns
        -------
        Dictionary
            dict containing the header of the file.
        """
        dict = {}
        # Create range of all header indices
        idxs = np.arange(start_idx, end_idx+1, dtype=int)
        # Iterate over all header indices
        for i in idxs:
            # Remove leading @ character
            split[i] = split[i].replace("@", "")
            # Split line using shlex
            l = shlex.split(split[i])
            # Check length of list
            if len(l) != 3:
                print(len(l))
                raise RuntimeError('TwissReader: Can not form dictionary!')
            # Set key and value
            key = l[0]
            val = l[2]
            # Try to convert to float
            try:
                val = float(val)
            except:
                pass
            # Add key val to dictionary
            dict[key] = val
        return dict

    def __create_dataframe(self, split, data_desc_idx, start_idx, end_idx, sep):
        """Creates a dataframe from the data lines.
        Parameters
        ----------
        split : list(strings)
            Rows of TWISS file.
        data_desc_idx : int
            Index of description row
        start_idx : int
            Index of first data row
        end_idx : int
            Index of last data row
        sep : string
            Seperator used in file
        Returns
        -------
        pandas.DataFrame
            DataFrame containing the data part of the twiss file.
        """
        # Get data description line
        desc = split[data_desc_idx]
        # Delete leading star
        desc = desc[1:]
        # Get column names using the split (from shlex)
        columns = shlex.split(desc)
        # Empty data array
        data = []
        # Iterate over all data indices
        for i in np.arange(start_idx, end_idx+1):
            # Split line using shlex
            line = shlex.split(split[i])
            # Check that length is fitting the length of columns
            if len(line) != len(columns):
                raise RuntimeError('TwissReader: Found line with non matching dimensions!')
            # Try to convert values to float
            for i, val in enumerate(line):
                try:
                    line[i] = float(val)
                except:
                    pass
            # Append rows to data array
            data.append(line)

        # Create dataframe
        data = pd.DataFrame(data, columns=columns)
        data = data.set_index(columns[0])
        # Return dataframe
        return data
