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
import collections

import jinja2

from locale import atof, setlocale, LC_NUMERIC
setlocale(LC_NUMERIC, '') 

#--------------
# local imports
# -------------

from tdblocation import INSERT_TPL, INPUT_FILENAME

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

class NoTessWithMACError(Exception):
    '''No TESS found with MAC'''
    def __str__(self):
        s = self.__doc__
        if self.args:
            s = ' {0}: {1}'.format(s, str(self.args))
        s = '{0}.'.format(s)
        return s

# ----------------
# Module constants
# ----------------

log = logging.getLogger("tdblocat")

# # ----------------------------------------------------

def non_empty_place(item):
    return True if item['Nombre lugar'].strip() else False

def location_dict(item):
    result = {
        'id':         item.get('#'),
        'site':      item.get('Nombre lugar').strip(), 
        'longitude': item.get('Longitud'), 
        'latitude':  item.get('Latitud'), 
        'elevation': item.get('MSNM'), 
        'location':  item.get('Población'), 
        'zipcode':   'Unknown', 
        'province':  'Unknown', 
        'state':     'Unknown',
        'country':   item.get('País'),
        'timezone':  item.get('Timezone'), 
        'contact_name':  item.get('Observador'), 
        'contact_email': item.get('Mail observador'), 
        'organization':  item.get('Organización'),
    }
    try:
        result['longitude'] = atof(result['longitude'])  if result['longitude'].strip() else "'Unknown'"
        result['latitude']  = atof(result['latitude'])   if result['latitude'].strip()  else "'Unknown'"
        result['elevation'] = atof(result['elevation'])  if result['elevation'].strip() else "'Unknown'"
        result['location'] = result['location'].strip()  if result['location'] else 'Unknown'
        result['country']  = result['country'].strip()   if result['country']  else 'Unknown'
        result['timezone'] = result['timezone'].strip()  if result['timezone'] else 'Etc/UTC'
        result['contact_name']  = result['contact_name'].strip()  if result['contact_name']  else 'Unknown'
        result['contact_email'] = result['contact_email'].strip() if result['contact_email'] else 'Unknown'
        result['organization']  = result['organization'].strip()  if result['organization']  else 'Unknown'
    except Exception as e:
        log.error(f"{e} in {result}")
        return None
    return result

def non_empty_dict(item):
    return True if item else False

def render(template_path, context):
    if not os.path.exists(template_path):
        raise IOError("No Jinja2 template file found at {0}. Exiting ...".format(template_path))
    path, filename = os.path.split(template_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)


def generate_sql(locations, output_dir):
    context = dict()
    context['locations'] = locations
    output = render(INSERT_TPL, context)
    full_path = os.path.join(output_dir, 'locations.sql')
    log.info(f"Writting SQL file {full_path}")
    with open(full_path,'w') as sqlfile:
        sqlfile.write(output)

def handle_site_name(name):
    components = name.split(' ')
    if len(components) > 1:
        pass
        #name = name.title()
    return name

def unique_locations(locations):
    result = dict()
    for item in locations:
        key = handle_site_name(item['site'])
        duplicates = result.get(key,[])
        duplicates.append(item)
        if key != '-':
            result[key] = duplicates
    for key, values in result.items():
        N = len(values)
        csv_rows = [item['id'] for item in values]
        if N > 1:
            log.info(f"{N} Duplicates for {key}, CSV rows {csv_rows}")
    return [values[0] for key, values in result.items()]
        
# ------------
# Entry points
# ------------

def generate(connection, options):
    fullname = os.path.join(options.input_dir, INPUT_FILENAME)
    log.info(f"Processing measurements from {fullname}")
    with open(fullname, newline='') as csvfile:
        reader = csv.DictReader(csvfile, restkey='basura')
        g1 = filter(non_empty_place, reader)
        g2 = map(location_dict, g1)
        locations = list(filter(non_empty_dict, g2))
    locations = unique_locations(locations)
    log.info(f"Found {len(locations)} unique locations")
    generate_sql(locations, options.input_dir)
      
