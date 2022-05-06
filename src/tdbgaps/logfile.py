# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright (c) 2021
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

#--------------------
# System wide imports
# -------------------

import re
import os
import glob
import datetime
import logging

# -------------
# Local imports
# -------------


# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger("tdbgaps")



TSTAMP_SESSION_FMT = '%Y-%m-%dT%H:%M:%S'
MQTT_EXPR = re.compile(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\+0000 \[\w+#info\] MQTT Stats \[Total, Reads, Register, Discard\] = \[(\d+), (\d+), (\d+), (\d+)\]')
DB_EXPR   = re.compile(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\+0000 \[\w+#info\] DB Stats Readings \[Total, OK, NOK\] = \((\d+), (\d+), (\d+)\)')


# -----------------------
# Module global variables
# -----------------------


def extract_db_info(matchobj):
    return {
        'tstamp': datetime.datetime.strptime(matchobj.group(1), TSTAMP_SESSION_FMT),
        'total' : int(matchobj.group(2)),
        'ok'    : int(matchobj.group(3)),
        'nok'   : int(matchobj.group(4)),
    }


def load_lines(path):
    log.info(f"Opening {path}")
    with open(path) as f:
        for i, line in enumerate(f, start=1):
            yield (path, i, line)

def filter_lines(extended_lines):
    def f(item):
        matchobj = DB_EXPR.search(item[2])
        return matchobj
    return filter(f, extended_lines)

def map_lines(filtered_lines):
    def f(item):
        matchobj = DB_EXPR.search(item[2])
        return {
            'filepath': item[0],
            'lineno': item[1],
            'tstamp': datetime.datetime.strptime(matchobj.group(1), TSTAMP_SESSION_FMT),
            'total' : int(matchobj.group(2)),
            'ok'    : int(matchobj.group(3)),
            'nok'   : int(matchobj.group(4)),
        }
    return map(f, filtered_lines)


def parsed_files_iterator(connection):
    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT DISTINCT filepath FROM log_dbase_stats_t;
        '''
    )
    return cursor


def update_parsed_files(connection, iterable):
    cursor = connection.cursor()
    cursor.executemany(
        '''
        INSERT INTO log_dbase_stats_t(filepath,lineno,tstamp,total,ok,nok)
        VALUES (:filepath,:lineno,:tstamp,:total,:ok,:nok)
        ''',
        iterable
    )
    connection.commit()



# =================
# Public module API
# =================

def parse(connection, options):
    if options.base_dir is not None:
        path = os.path.join(options.base_dir, "tessdb.log-????????")
    else:
        path = options.input_file
    file_list = glob.iglob(path)
    parsed_list = (result[0] for result in parsed_files_iterator(connection))
    difference = set(file_list) - set(parsed_list)
    if difference:
        for f in difference:
            updated = list(map_lines(filter_lines(load_lines(f))))
        update_parsed_files(connection, updated)
    else:
        log.info("No new log fles to parse")
        