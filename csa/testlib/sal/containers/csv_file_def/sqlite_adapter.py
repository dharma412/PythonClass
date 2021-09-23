#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/sal/containers/csv_file_def/sqlite_adapter.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import re
import uuid

TABLE_NAME_PATTERN = '%CSV%'


def _guess_sqlite_value_type(field_name, value):
    is_int = lambda value: \
        re.match(r'^[-+]?[0-9]+$', value) is not None
    is_float = lambda value: \
        re.match(r'^[-+]?[0-9]*\.[0-9]+$', value) is not None

    if is_int(value):
        return 'INTEGER'
    elif is_float(value):
        return 'REAL'
    else:
        return 'TEXT'


def _dict_factory(cursor, row):
    """http://docs.python.org/2/library/sqlite3.html"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _get_fixed_raw_data(headers, raw_data_lines):
    """Ironport CSV reports sometimes don't meet RFC requirements.
    So we have to fix this issue manually"""
    fixed_data = []
    headers_len = len(headers)
    for line in raw_data_lines:
        if len(line) == headers_len:
            fixed_data.append(line)
        elif len(line) > headers_len:
            fixed_data.append(line[:headers_len])
        else:
            fixed_line = line[:]
            fixed_line.extend([''] * (headers_len - len(fixed_line)))
            fixed_data.append(line)
    return fixed_data


def _get_column_types_mapping(headers, raw_table_data):
    mapping = {}
    for idx, header_name in enumerate(headers):
        str_value = raw_table_data[0][idx] if raw_table_data else ''
        mapping[header_name] = _guess_sqlite_value_type(header_name,
                                                        str_value)
    return mapping


def _create_table(connection, table_name, headers, raw_table_data):
    if not headers:
        return
    query = 'CREATE TABLE {table_name} ({fields})'
    fields_mapping = _get_column_types_mapping(headers, raw_table_data)
    fields = map(lambda header: \
                     '"{0}" {1}'.format(header, fields_mapping[header]),
                 headers)
    query = query.format(table_name=table_name, fields=','.join(fields))
    connection.cursor().execute(query)
    connection.commit()
    if not raw_table_data:
        return
    query = 'INSERT INTO {table_name} ({fields}) VALUES ({values_mask})'.format(
        table_name=table_name,
        fields=','.join(map('"{0}"'.format, headers)),
        values_mask=','.join('?' * len(headers)))
    connection.cursor().executemany(query, tuple(map(tuple, raw_table_data)))
    connection.commit()


def query_csv_as_sqlite_table(headers, raw_data_lines, query, flatten=False):
    import sqlite3
    connection = sqlite3.connect(":memory:", sqlite3.PARSE_COLNAMES)
    if not flatten:
        connection.row_factory = _dict_factory
    cursor = connection.cursor()
    try:
        table_name = 't{0}'.format(unicode(uuid.uuid4()).replace('-', ''))
        raw_table_data = _get_fixed_raw_data(headers, raw_data_lines)
        _create_table(connection, table_name, headers, raw_table_data)
        cursor.execute(query.replace(TABLE_NAME_PATTERN, table_name))
        return cursor.fetchall()
    finally:
        if headers:
            query = 'DROP TABLE IF EXISTS {0}'.format(table_name)
            cursor.execute(query)
            connection.commit()
        cursor.close()
        connection.close()
