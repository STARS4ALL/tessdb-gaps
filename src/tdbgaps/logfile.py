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
import itertools

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

# -----------------
# Utility functions
# -----------------

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def extract_db_info(matchobj):
    return {
        'tstamp': datetime.datetime.strptime(matchobj.group(1), TSTAMP_SESSION_FMT),
        'total' : int(matchobj.group(2)),
        'ok'    : int(matchobj.group(3)),
        'nok'   : int(matchobj.group(4)),
    }


def load_lines(path):
    log.info(f"Parsing {path}")
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


def update_parsed_file(connection, iterable):
    cursor = connection.cursor()
    cursor.executemany(
        '''
        INSERT INTO log_dbase_stats_t(filepath, lineno, tstamp, total, ok, nok)
        VALUES (:filepath, :lineno, :tstamp, :total, :ok, :nok)
        ''',
        iterable
    )
    connection.commit()

def stats_iterator(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(tstamp) FROM dbase_intervals_t")
    t = cursor.fetchone()[0]
    if t is not None:
        log.info(f"Fetching entries > {t}")
        cursor.execute(
            '''
            SELECT tstamp,total FROM log_dbase_stats_t 
            WHERE tstamp > (SELECT MAX(tstamp) FROM dbase_intervals_t)
            ORDER BY tstamp ASC
            '''
        )
    else:
        log.info("Empty interval table")
        cursor.execute(
            '''
            SELECT tstamp,total FROM log_dbase_stats_t 
            ORDER BY tstamp ASC
            '''
        )
    return cursor

def update_intervals(connection, iterable):
    cursor = connection.cursor()
    cursor.executemany(
        '''
        INSERT INTO dbase_intervals_t(tstamp, duration, delta)
        VALUES (:tstamp, :duration, :delta)
        ''',
        iterable
    )
    connection.commit()


def intervals_iterator(connection):
    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT tstamp, duration, delta FROM dbase_intervals_t
        ORDER BY tstamp ASC
        '''
    )
    return cursor

def calculate_gap(iterable):
    begin = False
    end   = False
    for tstamp, duration, delta in iterable:
        if delta < 0:
            begin = True
            start_tstamp = datetime.datetime.strptime(tstamp,'%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=duration)
        elif delta > 0:
            end = True
            end_tstamp = datetime.datetime.strptime(tstamp,'%Y-%m-%d %H:%M:%S')
        if begin and end:
            begin = False
            end   = False
            if end_tstamp - start_tstamp >= datetime.timedelta(days=1):
                log.info(f"Detected a gap from T = {start_tstamp} to T = {end_tstamp} ({end_tstamp - start_tstamp})")

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
        updated = list()
        for f in difference:
            updated.extend(list(map_lines(filter_lines(load_lines(f)))))
        update_parsed_file(connection, updated)
    else:
        log.info("No new log fles to parse")


def gaps(connection, options):
    log.info("Analyzing database gaps")
    gap_list = list()
    for item in pairwise(stats_iterator(connection)):
        n0 = item[0][1]
        n1 = item[1][1]
        if n0 > 0 and n1 > 0:
            continue
        t0 = datetime.datetime.strptime(item[0][0],'%Y-%m-%d %H:%M:%S')
        t1 = datetime.datetime.strptime(item[1][0],'%Y-%m-%d %H:%M:%S')
        duration = (t1-t0).total_seconds()
        delta = n1 - n0
        gap_list.append(
            {'tstamp': t0, 'duration': duration, 'delta': delta}
        )
    if not gap_list:
        log.info("No new intervals to analyze")
    update_intervals(connection, gap_list)
    calculate_gap(intervals_iterator(connection))
        