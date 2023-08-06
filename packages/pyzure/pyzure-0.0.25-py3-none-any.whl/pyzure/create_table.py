import logging

import datetime
import pandas as pd
import pyodbc

from pyzure.execute import execute_query


def detect_type(example, name):
    try:
        datetime.datetime.strptime(example[:10], "%Y-%m-%d")
        return "DATETIME"
    except:
        pass
    if isinstance(example, str):
        if len(example) >= 255:
            return "TEXT"
    elif isinstance(example, bool):
        return "BOOL"
    elif isinstance(example, int):
        if example > 2147483646:
            return "BIGINT"
        else:
            return "INTEGER"
    elif isinstance(example, float):
        return "FLOAT"
    try:
        float(example)
        if '.' in example:
            return "FLOAT"
        if len(example) < 11:
            return "INTEGER"
        return "VARCHAR(256)"
    except ValueError:
        return "VARCHAR(256)"


def def_type(name, example):
    logging.info('Define type of %s...' % name)
    return detect_type(example, name)


def find_sample_value(df, name, i):
    if df[name].dtype == 'object':
        df[name] = df[name].apply(lambda x: str(x) if x is not None else '')
        return df[name][df[name].map(len) == df[name].map(len).max()].iloc[0]
    else:
        rows = df.values.tolist()
        for row in rows:
            value = row[i]
            if value is not None:
                return value
        return None


def format_create_table(data):
    table_name = data["table_name"]
    columns_name = data["columns_name"]
    rows = data["rows"]
    params = {}
    df = pd.DataFrame(rows, columns=columns_name)

    for i in range(len(columns_name)):
        name = columns_name[i]
        logging.info(name)
        example = find_sample_value(df, name, i)
        col = dict()
        col["example"] = example
        col["type"] = def_type(name, example)
        col["encoding"] = "ENCODE ZSTD "
        params[name] = col

    query = """"""
    query = query + "CREATE TABLE " + table_name + " ("
    col = list(params.keys())
    for i in range(len(col)):
        k = col[i]
        if i == len(col) - 1:
            query = query + "\n     \"" + k + '\" ' + params[k]["type"] + ' ' + 'NULL '
        else:
            query = query + "\n     \"" + k + '\" ' + params[k]["type"] + ' ' + 'NULL ,'
    else:
        query = query[:-1]
    query = query + "\n )"
    logging.info(query)
    return query


def create_table(instance, data):
    query = format_create_table(data)

    def ex_query(q):
        return execute_query(instance, q)

    try:
        ex_query(query)
    except pyodbc.ProgrammingError as e:
        e = str(e)
        logging.info(e)
        if "schema" in e:
            ex_query("CREATE SCHEMA " + data['table_name'].split(".")[0])
            ex_query(query)
