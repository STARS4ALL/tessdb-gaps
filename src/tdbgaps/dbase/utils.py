# ----------------------------------------------------------------------
# Copyright (c) 2022
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

#--------------------
# System wide imports
# -------------------

import os
import os.path
import uuid
import glob
import sqlite3

# -------------------
# Third party imports
# -------------------

#--------------
# local imports
# -------------

# ----------------
# Module constants
# ----------------

VERSION_QUERY = "SELECT value from config_t WHERE section ='database' AND property = 'version'"

# -----------------------
# Module global variables
# -----------------------

# ------------------------
# Module Utility Functions
# ------------------------

def _filter_factory(connection):
    cursor = connection.cursor()
    cursor.execute(VERSION_QUERY)
    result = cursor.fetchone()
    if not result:
        raise NotImplementedError(VERSION_QUERY)
    version = int(result[0])
    return lambda path: int(os.path.basename(path)[:2]) > version


# -------------------------
# Module exported functions
# -------------------------

def create_database(dbase_path):
    '''Creates a Database file if not exists and returns a connection'''
    new_database = False
    output_dir = os.path.dirname(dbase_path)
    if not output_dir:
        output_dir = os.getcwd()
    os.makedirs(output_dir, exist_ok=True)
    if not os.path.exists(dbase_path):
        with open(dbase_path, 'w') as f:
            pass
        new_database = True
    return sqlite3.connect(dbase_path), new_database


def create_schema(connection, schema_path, initial_data_dir_path, updates_data_dir, query=VERSION_QUERY):
    created = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except Exception:
        created = False
    if not created:
        with open(schema_path) as f: 
            lines = f.readlines() 
        script = ''.join(lines)
        connection.executescript(script)
        #log.info("Created data model from {0}".format(os.path.basename(schema_path)))
        file_list = glob.glob(os.path.join(initial_data_dir_path, '*.sql'))
        for sql_file in file_list:
            #log.info("Populating data model from {0}".format(os.path.basename(sql_file)))
            with open(sql_file) as f: 
                lines = f.readlines() 
            script = ''.join(lines)
            connection.executescript(script)
    else:
        filter_func = _filter_factory(connection)
        file_list = sorted(glob.glob(os.path.join(updates_data_dir, '*.sql')))
        file_list = list(filter(filter_func,file_list))
        for sql_file in file_list:
            #log.info("Applying updates to data model from {0}".format(os.path.basename(sql_file)))
            with open(sql_file) as f: 
                lines = f.readlines() 
            script = ''.join(lines)
            connection.executescript(script)
    connection.commit()
    return not created, file_list

def read_property(connection, section, proper):
    cursor = connection.cursor()
    row = {'section': section, 'property': proper}
    cursor.execute("SELECT value FROM config_t WHERE section = :section AND property = :property", row)
    return cursor.fetchone()[0]

def update_property(connection, section, proper, value):
    cursor = connection.cursor()
    row = {'section': section, 'property': proper, 'value': value}
    cursor.execute("UPDATE config_t SET value = :value WHERE section = :section AND property = :property", row)
    connection.commit()

def display_section(iterable):
    headers = ("Section", "Propèrty", "Value")
    paging(iterable, headers)

def read_section(connection, section):
    row = {'section': section,}
    cursor = connection.cursor()
    cursor.execute('SELECT section, property, value FROM config_t WHERE section = :section', row)
    return cursor

def read_database_version(connection):
    cursor = connection.cursor()
    query = 'SELECT value FROM config_t WHERE section = "database" AND property = "version";'
    cursor.execute(query)
    version = cursor.fetchone()[0]
    return version

def write_database_uuid(connection):
    guid = str(uuid.uuid4())
    cursor = connection.cursor()
    param = {'section': 'database','property':'uuid','value': guid}
    cursor.execute(
        '''
        INSERT INTO config_t(section,property,value) 
        VALUES(:section,:property,:value)
        ''',
        param
    )
    connection.commit()
    return guid

def make_database_uuid(connection):
    cursor = connection.cursor()
    query = 'SELECT value FROM config_t WHERE section = "database" AND property = "uuid";'
    cursor.execute(query)
    guid = cursor.fetchone()
    if guid:
        try:
            uuid.UUID(guid[0])  # Validate UUID
        except ValueError:
            guid = write_database_uuid(connection)
        else:
            guid = guid[0]
    else:
        guid = write_database_uuid(connection)
    return guid


def read_configuration(connection):
     cursor = connection.cursor()
     cursor.execute("SELECT section, property, value FROM config_t ORDER BY section")
     return cursor.fetchall()

__all__ = [
    "create_database",
    "create_schema",
    "read_property",
    "update_property",
    "read_section",
    "display_section",
]
