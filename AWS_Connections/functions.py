###############
### imports ###
###############

import json
import pandas as pd
from sqlalchemy import create_engine

##############################
### SQL wrapping functions ###
##############################

def get_columns(schema, table, engine):
    """Returns all available column names in the schema.table specified."""    
    query = pd.read_sql_query('SELECT TOP 1 * FROM '+schema+"."+table+';', engine)
    return query.columns

# Currently, start_date and end_date are requriements for pulling down data
# Thought is that extremely large datasets should not be pulled in just one query on a notebook
# TODO: be adjusted to allow end_date to not be provided and be assumed to be current date
def get_data(schema, table, start_date, end_date, engine, columns="", filters="", like=""):
    """Gets all data in the table provided, so long as it fits the filters and like attributes.
    Returns a tuple"""
    params_list = []
    params_list.append(start_date)
    params_list.append(end_date)
    
    # Select all columns, unless a list of columns has been passed as a parameter
    if columns != "":
        columns_as_string = ', '.join(columns)
    else: columns_as_string = "*"
    
    if filters != "":
        filters_query_list = []
    
        # Because there is already a filter requirement listed first (start_date and end_date)
        # The string concat can begin with the word AND
        for i in filters:
            filters_query_list.append(' AND '+i+' IN ('+'%s,'*(len(filters[i])-1)+'%s)')
            for j in filters[i]:
                params_list.append(j)

        filters_query_string = "".join(filters_query_list)
    else: filters_query_string = ""
    
    if like != "":
        for i in like:
            filters_query_string += ' AND '+i+' LIKE %s'
            params_list.append(like[i])
    
    query = "".join(['SELECT ', columns_as_string, ' FROM ', schema, ".", table, 
                    ' WHERE report_date BETWEEN %s AND %s', filters_query_string, ';'])
    
    print('\nThe query string is: ' + query)
    data = pd.DataFrame()

    # Chunk the data as a precaution
    for chunk in pd.read_sql_query(query, engine, params=params_list, chunksize=10000):
        data = data.append(chunk, ignore_index = True)

    return data


def get_schemas(engine):
    """Returns available schemas in the database."""
    schemas = pd.read_sql_query('select nspname from pg_namespace', engine)
    non_temp_schemas = schemas[~schemas['nspname'].str.contains('temp')]['nspname']
    return non_temp_schemas
    
    

def get_distinct_values(schema, table, column, engine):
    """Return only unique values in the column."""
    query = pd.read_sql_query('SELECT DISTINCT '+column+' FROM '+schema+"."+table+';', engine)
    return query