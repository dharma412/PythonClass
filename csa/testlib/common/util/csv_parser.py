#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/common/util/csv_parser.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $


from common.util.utilcommon import UtilCommon

from sal.containers.csv_file import CSVFile

import csv


class CSVParser(UtilCommon):

    def get_keyword_names(self):
        return ['csv_parser_get_data',
                'csv_parser_get_record',
                'csv_parser_get_records_count',
                'csv_parser_get_field_names',
                'csv_parser_query',
                'csv_parser_get_column']

    def csv_parser_query(self, path, query, flatten=False):
        """Provide ability for manipulating data from csv file
        with SLQ queries. SQLite syntax is supported. But it is limited by
        the fact that any actions could be made only on one table.
        The only difference from SQL is that table name should be
        types as %CSV% template in query. Format of this record is mandatory.

        *Parameters*:
        - `path`: Path to CSV file.
        - `query`: SQLLite query string. For more information please refer to
        http://www.sqlite.org/lang.html. See http://sqlite.org/lang_datefunc.html
        for more information about integrated SQLite datetime functions.
        - `flatten`: whether to change results presentation from list of
        dictionaries to list of tuples. ${False} by default

        *Return*:
        - Empty list if there are no results, which correspond to this query.
        List of dictionaries if `flatten` is set to ${False}. Each dictionary will
        contain field names as keys and row values as correposnding values.
        List of tuples if `flatten` is set to ${True}. Each tuple will contain
        corresponding row values. *IMPORTANT:* This keyword is trying to
        guess table column types by their values and convert them appropriately.

        *Examples*:
        | ${query}= | Catenate |
        | ... | SELECT "Spam Detected", "Virus Detected" FROM %CSV% |
        | ... | WHERE datetime("Begin Timestamp", "unixepoch") |
        | ... | BETWEEN "2013-09-10" AND "2013-09-12" |
        | @{result} | CSV Parser Query | /tmp/report.csv | ${query} |
        | Should Not Be Empty | ${result} |
        | Log List | ${result} |
        """
        controller = CSVFile(path)
        return controller.query(query)

    def csv_parser_get_field_names(self, path):
        """Return a list of available field names.

        *Parameters*:
        - `path`: the path to an existing CSV file

        *Return*:
        - List of strings

        *Examples*:
        | @{fields}= | CSV Parser Get Field Names | /tmp/report.csv |
        | List Should Contain | ${fields} | Begin Timestamp |
        """
        controller = CSVFile(path)
        return controller.get_field_names()

    def csv_parser_get_data(self, path):
        """Get all available records in form of dictionary.

        *Parameters*:
        - `path`: the path to an existing CSV file

        *Return*:
        - Dictionary. Keys are field names and values are lists of corresponding
        column cells. All list values are represented as strings.

        *Examples*:
        | ${data_dict}= | CSV Parser Get Data | /tmp/report.csv |
        | Log Dictionary | ${data_dict} |
        """
        controller = CSVFile(path)
        return controller.get_data()

    def csv_parser_get_record(self, path, line_number):
        """Get a record in form of dictionary.

        *Parameters*:
        - `path`: the path to an existing CSV file
        - `line_number`: number of line in CSV file. Numbering starts from 1

        *Exceptions:*
        - `ValueError`: if `line_number` is greater than overall CSV records
        count

        *Return*:
        - List. All list values are represented as strings.

        *Examples*:
        | ${records_count}= | CSV Parser Get Records Count | /tmp/report.csv |
        | ${data}= | Run Keyword If | 2 <= ${records_count} |
        | ... | CSV Parser Get Record | /tmp/report.csv | 2 |
        | Log | ${data} |
        """
        controller = CSVFile(path)
        return controller.get_record(int(line_number))

    def csv_parser_get_records_count(self, path):
        """Return a number of records that are available
        in the CSV file.

        *Parameters*:
        - `path`: the path to an existing CSV file

        *Return*:
        - Integer

        *Examples*:
        | ${cnt}= | CSV Parser Get Records Count | /tmp/report.csv |
        """
        controller = CSVFile(path)
        return controller.get_records_count()

    def csv_parser_get_column(self, path, column_number):
        """Return the columns out of the .csv file

        *Parameters*:
        - `path`: the path to an existing CSV file
        - `column_number`: number of column to be parsed
        *Return*:
        - List

        *Examples*:
        | ${cnt}= | CSV Parser Get Column | /tmp/report.csv |

        """
        controller = CSVFile(path)
        return controller.get_column(path, column_number)
