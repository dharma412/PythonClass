#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/containers/csv_file.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import csv

from csv_file_def.sqlite_adapter import query_csv_as_sqlite_table, TABLE_NAME_PATTERN


class CSVFile(object):
    def __init__(self, path):
        self._path = path
        self.reload(path)

    @property
    def path(self):
        return self._path

    def reload(self, path):
        self._field_names = []
        self._lines = []
        with open(path, 'rb') as csvfile:
            dialect_type = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            csvlines = csv.reader(csvfile, dialect=dialect_type)
            self._lines = list(csvlines)
        self._field_names = self._lines[0] if len(self._lines) > 0 else []
        self._lines = self._lines[1:] if len(self._lines) > 1 else []

    def get_field_names(self):
        return self._field_names

    def get_data(self):
        result = {}
        for idx, col_name in enumerate(self._field_names):
            result[col_name] = []
            for line in self._lines:
                if idx < len(line):
                    result[col_name].append(line[idx])
        return result

    def query(self, query, flatten=False):
        return query_csv_as_sqlite_table(self._field_names,
                                         self._lines,
                                         query, flatten)

    def get_records_count(self):
        return len(self._lines)

    def get_record(self, row_number):
        if row_number > len(self._lines):
            raise ValueError('Record #{0} does not exist. ' \
                             'There are only {1} records in file {2}'.format(
                row_number, len(self._lines), self.path))
        return self._lines[row_number - 1]

    def get_column(self, path, column_number):
        columns = []
        with open(path, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ')
            for row in spamreader:
                columns.append(row[0].split(",")[column_number])
        return columns


if __name__ == '__main__':
    import os
    import pprint

    SARF_HOME = os.getenv('SARF_HOME')
    testcsv1_path = os.path.join(SARF_HOME,
                                 'tests/testdata/esa/csv_reports/reputation_filtering.csv')
    testcsv2_path = os.path.join(SARF_HOME,
                                 'tests/testdata/esa/csv_reports/spam_traffic_by_ip.csv')
    for csv_path in (testcsv1_path, testcsv2_path):
        csvfile = CSVFile(csv_path)
        print '======='
        print 'Path: {0}'.format(csvfile.path)
        print 'Field names: {0}'.format(csvfile.get_field_names())
        print 'Raw data: {0}'.format(pprint.pformat(csvfile.get_data()))
        print 'Records count: {0}'.format(csvfile.get_records_count())
        QUERY = 'SELECT * FROM {0}'.format(TABLE_NAME_PATTERN)
        print 'All items query result ({0}):\n{1}'.format(QUERY,
                                                          pprint.pformat(csvfile.query(QUERY)))
        # =======================================================================
        # QUERY = 'SELECT * FROM %CSV% WHERE '\
        #     'datetime("Begin Timestamp", "unixepoch") '\
        #     'BETWEEN "2013-09-10" AND "2013-09-12"'
        # print '[ {0} ] query result:\n{1}'.format(QUERY,
        #                                  pprint.pformat(csvfile.query(QUERY)))
        # =======================================================================
        raw_input('=======\nPress Enter to continue...\n')
