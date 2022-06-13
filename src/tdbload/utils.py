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
import logging
import datetime
import itertools

#--------------------
# Third party imports
# -------------------

import tabulate

# -------------
# Local imports
# -------------

# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger("tdbgaps")

def paging(iterable, headers, size=None, page=10):
    '''
    Pages query output from database and displays in tabular format
    '''
    db_iterable = hasattr(iterable, 'fetchmany')
    while True:
        if db_iterable:
            result = iterable.fetchmany(page)
        else:
            result = list(itertools.islice(iterable, page))
        if len(result) == 0:
            break
        if size is not None:
            size -= page
            if size < 0:
                result = result[:size]  # trim the last rows up to size requested
                print(tabulate.tabulate(result, headers=headers, tablefmt='grid'))
                break
            elif size == 0:
                break
        print(tabulate.tabulate(result, headers=headers, tablefmt='grid'))
        if len(result) < page:
            break
        input("Press Enter to continue [Ctrl-C to abort] ...")
    


def isfile(path):
    if os.path.isfile(path):
        return path
    raise IOError(f"{path} is not a valid file path or is not a file")

def isdir(path):
    if os.path.isdir(path):
        return path
    raise IOError(f"{path} is not a valid direrctory path or is not a directory")

def mkbool(boolstr):
    result = None
    if boolstr == 'True':
        result = True
    elif boolstr == 'False':
        result = False
    return result

def mkdate(datestr):
    date = None
    for fmt in ['%Y-%m','%Y-%m-%d','%Y-%m-%dT%H:%M:%S','%Y-%m-%dT%H:%M:%SZ']:
        try:
            date = datetime.datetime.strptime(datestr, fmt)
        except ValueError:
            pass
    return date


