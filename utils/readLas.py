import os

import pandas as pd
import tempfile


def convert_to_csv(read_path, write_path):
    f1 = open(write_path, "w")

    with open(read_path, "r") as lasFile:
        for line in lasFile:
            if line.startswith('~A') or line.startswith('~a'):
                a = next(lasFile, False)
                while a:
                    f1.write(a)
                    a = next(lasFile, False)


class ReadLas:
    def __init__(self, read_path):
        self.lat = None
        self.long = None
        self.read_path = read_path
        columns = self.version_and_curve_info(self.read_path)
        fd, write_path = tempfile.mkstemp()
        try:
            convert_to_csv(self.read_path, write_path)
        except:
            os.close(fd)
            os.unlink(write_path)
        # converting to csv, write to file, read whole file using read_csv, and delete csv file. Because reading from
        # csv is faster
        convert_to_csv(self.read_path, write_path)
        self.df = pd.read_csv(write_path, sep='\s+', names=columns)
        os.close(fd)
        os.unlink(write_path)
        self.df.set_index(columns[0], inplace=True)
        self.df['lat'] = self.lat
        self.df['long'] = self.long

    def version_and_curve_info(self, read_path):
        with open(read_path, "r") as lasFile:
            section = ''
            columns = []
            for line in lasFile:
                if line.startswith("~"):
                    # reading section header: ~V, ~A etc
                    # will be one from 'v', 'w', 'c', 'p', 'o', 'a'
                    section = line[1: 2].lower()
                elif line.startswith('#'):
                    # line with comment
                    continue
                else:
                    if section == 'v':
                        arrStr = line.split(".", maxsplit=1)
                        if arrStr[0].strip().lower() == "vers":
                            version = arrStr[1].strip().split(":")[0].strip()
                            if not (version == '2.00' or version == '2.0'):
                                raise Exception("Only version 2.0 supported. Version of file = " + version)
                    elif section == 'c':
                        column = line.split('.')[0].strip()
                        columns.append(column)
                    elif section == 'w':
                        column = line.split('.')[0].strip().lower()
                        if column == 'lati':
                            self.lat = float(line.split('.', maxsplit=1)[1].split(':')[0].strip())
                        elif column == 'long':
                            self.long = float(line.split('.', maxsplit=1)[1].split(':')[0].strip())
        return columns

    def get_begin_depth(self):
        return self.df.index.min()

    def get_end_depth(self):
        return self.df.index.max()

    def get_lat_long(self):
        return self.lat, self.long
