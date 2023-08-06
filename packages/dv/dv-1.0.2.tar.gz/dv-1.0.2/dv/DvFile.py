import os
import re

class AedatFile:
    @classmethod
    def is_aedat4(cls, file_path):
        with open(file_path, 'rb') as f:
            s = f.readline()
            v4 = re.compile('.*#!AER-DAT4.*')
            if v4.match(s):
                return True
        return False

    def __init__(self, file_path):
        if not AedatFile.is_aedat4(file_path):
            raise AssertionError('Not an aedat 4 compatible file')

        self._file = open(file_path, 'rb')

        # TODO: aedat 4 parser


class DvFile:

    def __init__(self, dv_file_directory):
        if not os.path.isdir(dv_file_directory):
            raise AssertionError('Given path is not a DV recording directory')

        streams = [f for f in os.listdir(dv_file_directory) if f.endswith('.aedat') and AedatFile.is_aedat4(f)]

