# -*- coding: utf-8 -*-
import pyodbc

from pyzure import execute

azure_types = [
    "BIT",
    "INT",
    "BIGINT",
    "NUMERIC",
    "DATE",
    "DATETIME",
    "CHAR",
    "VARCHAR",
    "TEXT",

]


def existing_test(instance, table_name):
    try:
        query = "SELECT COUNT(*) FROM " + table_name
        execute.execute_query(instance, query)
        return True
    except pyodbc.ProgrammingError:
        return False


def detect_type(instance, example, name):
    try:
        query = "SELECT CAST('%s' as DATETIME)" % example
        execute.execute_query(instance, query)
        return "DATETIME"

    except pyodbc.Error:
        pass

    if type(example) == str:
        return "VARCHAR(256)"
    elif type(example) == int:
        if example > 2147483646:
            return "BIGINT"
        else:
            return "INTEGER"
    elif type(example) == float:
        return "FLOAT"
    else:
        r = input("Cannot find type for %s \nPlease define it in 'types' dictionnary argument or type here\n" % name)
        if not r:
            exit()
        else:
            return r


def def_type(instance, name, example, types=None):
    print('Define type of %s...' % name)
    if not types:
        return detect_type(instance, example, name)

    try:
        result = types[name]
        if result.split('(')[0] not in azure_types:
            boolean = input('%s is apparently not in Azure Types, do you want to continue (y or n) ?\n' % result)
            if boolean.lower() in ('y', 'yes'):
                return result
            else:
                exit()
        else:
            return result
    except KeyError:
        return detect_type(instance, example, name)


def find_sample_value(rows, i):
    for row in rows:
        value = row[i]
        if value is not None:
            return value
    return None


def format_create_table(instance, data, primary_key, types=None):
    table_name = data["table_name"]
    columns_name = data["columns_name"]
    rows = data["rows"]
    params = {}
    for i in range(len(columns_name)):
        name = columns_name[i]
        example = find_sample_value(rows, i)
        col = dict()
        col["example"] = example
        col["type"] = def_type(instance, name, example, types)
        params[name] = col

    query = """"""
    query = query + "CREATE TABLE " + table_name + " ("
    col = list(params.keys())
    for i in range(len(col)):
        k = col[i]
        if (i == len(col) - 1) and (primary_key is None):
            query = query + "\n     " + k + ' ' + params[k]["type"] + ' ' + 'NULL ' + " --example:" + str(
                params[k]["example"]) + ''
        else:
            query = query + "\n     " + k + ' ' + params[k]["type"] + ' ' + 'NULL ,' + " --example:" + str(
                params[k]["example"]) + ''
    if primary_key is not None:
        query = query + '\n     ' + "PRIMARY KEY " + str(primary_key)
    else:
        query = query[:-1]
    query = query + "\n ) SELECT 1"
    print(query)
    return query


def set_primary_key(primary_key, data):
    if primary_key == ():
        primary_key = []
        prop = input("Do you really want not to set primary keys ? \n" +
                     "Columns names are : " + str(data["columns_name"]) + "\n" +
                     "You can write it down primary keys here separated by comma \n")
        if prop != '':
            for element in prop.split(","):
                columns_name = list(map(lambda x: x.lower(), data["columns_name"]))
                for_test = element.lower().strip()
                if for_test in columns_name:
                    primary_key.append(for_test)
                else:
                    print("%s not in columns_name" % for_test)
        else:
            return None
        print("Wait...")
    if type(primary_key) == str:
        primary_key = "(" + str(primary_key) + ")"
    elif len(primary_key) > 1:
        pk = '(' + primary_key[0]
        for p in primary_key[1:]:
            pk = pk + ',' + p
        pk = pk + ')'
        primary_key = pk
    else:
        primary_key = '(' + primary_key[0] + ')'
    return primary_key


def create_table(instance, data, primary_key=(), types=None):
    primary_key = set_primary_key(primary_key, data)
    query = format_create_table(instance, data, primary_key, types)

    def ex_query(q, create_schema=False):
        return execute.execute_query(instance, q, create_schema=create_schema)

    boolean = input(
        "You can modify the query with 'primary_key' and 'types' arguments \n" +
        "Do you really want to execute this query (y or n) ? \n"
    )
    if boolean.lower() in ('y', 'yes'):
        try:
            ex_query(query)
        except pyodbc.ProgrammingError as e:
            e = str(e)
            if "schema" in e:
                query_schema = "CREATE SCHEMA " + data['table_name'].split(".")[0]
                print(query_schema)
                ex_query(query_schema, create_schema=True)
                ex_query(query)
            elif "object" in e:
                boolean = input("Do you really want to drop table %s (y or n) ? \n" % data['table_name'])
                if boolean.lower() in ('y', 'yes'):
                    ex_query("DROP TABLE " + data['table_name'] + " SELECT 1")
                    ex_query(query)
                else:
                    exit()
            else:
                print(e)
    else:
        exit()


def test():
    data = {
        "table_name": 'testsch.test',
        "columns_name": ["nom", "prenom", "age", "date"],
        "rows": [["pif", "pif", 12, "2017-02-23"]]
    }
    primary_key = ()

    types = {
        'nom': 'VARCHAR(12)',
    }
    create_table('MH_TEST', data, primary_key, types)
