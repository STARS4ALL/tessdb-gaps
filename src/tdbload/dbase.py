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

import os
import csv
import logging
import datetime


import jinja2

#--------------
# local imports
# -------------

from tdbload import INSERT_TPL, LOADER_TPL

class AmbiguousNameToMACError(Exception):
    '''Ambiguity in name to mac mapping'''
    def __str__(self):
        s = self.__doc__
        if self.args:
            s = ' {0}: {1}'.format(s, str(self.args[0]))
        s = '{0}.'.format(s)
        return s

class AmbiguousTessId(Exception):
    '''Ambiguity in TESS identifier'''
    def __str__(self):
        s = self.__doc__
        if self.args:
            s = ' {0}: {1}'.format(s, str(self.args))
        s = '{0}.'.format(s)
        return s

class NoTessError(Exception):
    '''No TESS found with name'''
    def __str__(self):
        s = self.__doc__
        if self.args:
            s = ' {0}: {1}'.format(s, str(self.args[0]))
        s = '{0}.'.format(s)
        return s

# ----------------
# Module constants
# ----------------

log = logging.getLogger("tdbload")


def lookup_mac(connection, row):
    cursor = connection.cursor()
    sql = '''
    SELECT name, mac_address, valid_state, valid_since, valid_until
    FROM name_to_mac_t
    WHERE name = :name
    AND :time BETWEEN valid_since AND valid_until
    '''
    cursor.execute(sql,row)
    result = cursor.fetchall()
    if len(result) > 1:
        raise AmbiguousNameToMACError(result)
    elif len(result) == 0:
        raise NoTessError(row['name'])
    row['mac_address']      = result[0][1]
    row['name_valid_state'] = result[0][2]
    row['name_valid_since'] = result[0][3]
    row['name_valid_until'] = result[0][4]
    return row


def lookup_tess(connection, row):
    cursor = connection.cursor()
    sql = '''
    SELECT tess_id, valid_state, valid_since, valid_until, location_id
    FROM tess_t
    WHERE mac_address = :mac_address
    AND :time BETWEEN valid_since AND valid_until
    '''
    cursor.execute(sql,row)
    result = cursor.fetchall()
    if len(result) > 1:
        raise AmbiguousTessId(row['name'], row['mac_address'], *result)
    row['tess_id']             = result[0][0]
    row['tess_id_valid_state'] = result[0][1]
    row['tess_id_valid_since'] = result[0][2]
    row['tess_id_valid_until'] = result[0][3]
    row['location_id']         = result[0][4]
    return row


def lookup_location(connection, row):
    cursor = connection.cursor()
    sql = '''
    SELECT site
    FROM location_t
    WHERE location_id = :location_id
    '''
    cursor.execute(sql,row)
    result = cursor.fetchone()
    row['site_name'] = result[0]
    return row


def fix_ids(row):
    # Too many microseconds sometimes
    row['time'] = row['time'][:20] + row['time'][20:26]
    try:
        tstamp = (datetime.datetime.strptime(row['time'], "%Y-%m-%dT%H:%M:%S.%f") + datetime.timedelta(seconds=0.5)).replace(microsecond=0)
    except ValueError as e:
        tstamp = (datetime.datetime.strptime(row['time'], "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(seconds=0.5)).replace(microsecond=0)
    date_id = tstamp.year*10000 + tstamp.month*100 + tstamp.day
    time_id = tstamp.hour*10000 + tstamp.minute*100 + tstamp.second
    row['date_id']  = date_id 
    row['time_id']  = time_id
    row['units_id'] = 2
    return row

def missing_fields(row):
    _ = row['name']
    _ = row['freq']
    _ = row['mag']
    _ = row['seq']
    _ = row['tamb']
    _ = row['tsky']
    _ = row['wdBm']
    return row


def process_row(connection, row):
    row = fix_ids(row)
    row = missing_fields(row)
    row = lookup_mac(connection, row)
    row = lookup_tess(connection, row)
    row = lookup_location(connection, row)
    return row 


def render(template_path, context):
    if not os.path.exists(template_path):
        raise IOError("No Jinja2 template file found at {0}. Exiting ...".format(template_path))
    path, filename = os.path.split(template_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

# -----------------------------------------------------------------------------------------------

def lookup_database(connection, input_file):
    photometers = dict()
    with open(input_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            name = row['name']
            rows = photometers.get(name, list())
            try:
                row = process_row(connection, row)
            except KeyError as e:
                log.error(f"Missing essential datum in CSV file: {e}")
                continue
            except NoTessError as e:
                log.error(f"When looking name->MAC{e}")
            except Exception as e:
                log.error(e)
                continue
            rows.append(row)
            photometers[name] = rows
    return photometers


def sort_measurements(photometers):
    def key(row):
        return row['time']
    for name, rows in photometers.items():
        log.info(f"[{name}] sorting by timestamp measurements")
        rows.sort(key=key)
    return photometers


def generate_sql(photometers, database_path, output_dir):
    for name, rows in photometers.items():
        context = dict()
        context['measurements'] = rows
        output = render(INSERT_TPL, context)
        full_path = os.path.join(output_dir, name + '.sql')
        log.info(f"Writting SQL file {full_path}")
        with open(full_path,'w') as sqlfile:
            sqlfile.write(output)
    context = dict()
    context['database_path'] = database_path
    output = render(LOADER_TPL, context)
    full_path = os.path.join(output_dir, 'loader.sh')
    with open(full_path,'w') as script:
            script.write(output)

# ------------
# Entry points
# ------------

def generate(connection, options):
    name, ext = os.path.splitext(os.path.basename(options.input_file))
    subdir = os.path.join(os.path.dirname(options.input_file), name)
    os.makedirs(subdir, exist_ok=True)
    log.info(f"Processing measurements from {options.input_file} into {subdir} ")
    photometers = lookup_database(connection, options.input_file)
    photometers = sort_measurements(photometers)
    generate_sql(photometers, options.dbase, subdir)