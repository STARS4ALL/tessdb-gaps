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
import sys
import glob
import uuid
import datetime
import sqlite3
import sys

# -------------------
# Third party imports
# -------------------


#--------------
# local imports
# -------------

from tdbgaps.dbase import SQL_SCHEMA, SQL_INITIAL_DATA_DIR, SQL_UPDATES_DATA_DIR, NAMESPACE, log 
from tdbgaps.dbase.utils import create_database, create_schema, read_database_version, make_database_uuid

# ----------------
# Module constants
# ----------------

SQL_TEST_STRING = "SELECT COUNT(*) FROM config_t"

# --------------
# Module Classes
# --------------

class DatabaseService:
    '''Imitating a database service, a la Twisted but without Twisted'''

    # Service name
    name = 'Database Service'

    def __init__(self, path, create_only=False, *args, **kargs):
        self.path = path
        self.create_only = create_only
        self.connection = None

    # ------------
    # Service API
    # ------------

    def startService(self):
        connection, new_database_flag = create_database(self.path)
        if new_database_flag:
            log.info(f"Created new database file at {self.path}")
        just_created, file_list = create_schema(connection, SQL_SCHEMA, SQL_INITIAL_DATA_DIR, SQL_UPDATES_DATA_DIR, SQL_TEST_STRING)
        if just_created:
            for sql_file in file_list:
                log.info(f"Populating data model from {os.path.basename(sql_file)}")
        else:
            for sql_file in file_list:
                log.info(f"Applying updates to data model from {os.path.basename(sql_file)}")
        version = read_database_version(connection)
        guid    = make_database_uuid(connection)
        log.info(f"Starting {self.name} on {self.path}, version = {version}, UUID = {guid}")
        connection.commit()
        self.connection = connection
       
    def stopService(self):
        log.info(f"Stopping {self.name} on {self.path}")
        self.connection.commit()
        self.connection.close()

    # ---------------
    # OPERATIONAL API
    # ---------------

    def getInitialConfig(self, section):
        config = read_configuration(self.connection)
        g = filter(lambda i: True if i[0] == section else False, config)
        return dict(map(lambda i: (i[1], i[2]) ,g))
