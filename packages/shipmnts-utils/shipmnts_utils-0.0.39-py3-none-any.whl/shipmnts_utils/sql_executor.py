from django.db import connection


def execute_select_query(query, output_format='tuple', fetch=None):
    tuple_data, json_data = None, None
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        if fetch and fetch == "one":
            tuple_data = cursor.fetchone()
        else:
            tuple_data = cursor.fetchall()
    finally:
        cursor.close()
        if output_format=='json':
            if tuple_data:
                json_data = list()
                print(tuple_data, 'tuple data')
                for row in tuple_data:
                    row_object = dict()
                    for key in cursor.description:
                        print(key, 'cursordescription')
                        row_object.update({key[0]: value for value in row})
                        print(row_object, 'rowobject')
                    json_data.append(row_object)
            return json_data
        return tuple_data

def execute_update_query(query):
    c = connection.cursor()
    try:
        c.execute(query)
    finally:
        c.close()

