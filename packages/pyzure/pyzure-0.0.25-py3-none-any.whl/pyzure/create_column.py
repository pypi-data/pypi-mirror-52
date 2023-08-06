import logging

import pyzure
from pyzure.execute import execute_query
import pandas as pd

from pyzure.create_table import find_sample_value
from pyzure.create_table import def_type
from pyzure.send.common import get_table_info


def create_column(instance, data, column_name):
    table_name = data["table_name"]
    rows = data["rows"]
    columns_name = data["columns_name"]
    df = pd.DataFrame(rows, columns=columns_name)
    example = find_sample_value(df, column_name, columns_name.index(column_name))
    type_ = def_type(column_name, example)
    query = """
    alter table %s
    add "%s" %s
    default NULL;
    """ % (table_name, column_name, type_)
    logging.info(query)
    execute_query(instance, query)
    return 0


def create_columns(instance, data):
    table_name = data["table_name"]
    rows = data["rows"]
    columns_name = data["columns_name"]
    infos = get_table_info(instance, table_name)
    all_column_in_table = [e['column_name'] for e in infos]
    df = pd.DataFrame(rows, columns=columns_name)
    queries = []
    for column_name in columns_name:
        if column_name not in all_column_in_table:
            example = find_sample_value(df, column_name, columns_name.index(column_name))
            type_ = def_type(column_name, example)
            query = """
            alter table %s
            add "%s" %s
            default NULL
            """ % (table_name, column_name, type_)
            queries.append(query)
    if queries:
        query = ' '.join(queries)
        logging.info(query)
        execute_query(instance, query)
    return 0


def extend_column(instance, data):
    table_name = data["table_name"]
    rows = data["rows"]
    columns_name = data["columns_name"]
    df = pd.DataFrame(rows, columns=columns_name)
    table_info = get_table_info(instance, table_name)
    for c in columns_name:
        example = find_sample_value(df, c, columns_name.index(c))
        if isinstance(example, str):
            if len(example) >= 255:
                for r in table_info:
                    if r['column_name'] == c:
                        type_ = "TEXT"
                        query = """ALTER TABLE %(table_name)s ALTER COLUMN "%(column_name)s" %(type_)s""" % {
                            "table_name": table_name,
                            "column_name": r['column_name'],
                            "type_": type_
                        }
                        execute_query(instance, query)
    return 0
