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

import sys
import argparse
import os.path
import logging
#import logging.handlers
import traceback
import importlib
import sqlite3

# -------------
# Local imports
# -------------

from tdbgaps import  __version__
from tdbload.utils import mkdate, mkbool, isdir, isfile


# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger("tdbload")

# -----------------------
# Module global functions
# -----------------------

def configureLogging(options):
    if options.verbose:
        level = logging.DEBUG
    elif options.quiet:
        level = logging.WARN
    else:
        level = logging.INFO
    
    log.setLevel(level)
    # Log formatter
    #fmt = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
    fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    # create console handler and set level to debug
    if not options.no_console:
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        ch.setLevel(level)
        log.addHandler(ch)
    # Create a file handler
    if options.log_file:
        #fh = logging.handlers.WatchedFileHandler(options.log_file)
        fh = logging.FileHandler(options.log_file)
        fh.setFormatter(fmt)
        fh.setLevel(level)
        log.addHandler(fh)


def python2_warning():
    if sys.version_info[0] < 3:
        log.warning("This software des not run under Python 2 !")


def setup(options):
    python2_warning()
    

def open_database(dbase_path):
    if not os.path.exists(dbase_path):
       raise IOError("No SQLite3 Database file found at {0}. Exiting ...".format(dbase_path))
    logging.info("Opening database {0}".format(dbase_path))
    return sqlite3.connect(dbase_path)

# =================== #
# THE ARGUMENT PARSER #
# =================== #

def createParser():
    # create the top-level parser
    name = os.path.split(os.path.dirname(sys.argv[0]))[-1]
    parser = argparse.ArgumentParser(prog=name, description="TESSDB LOAD OBSERVATIONS TOOL")

    # Global options
    parser.add_argument('--version', action='version', version='{0} {1}'.format(name, __version__))
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')
    group.add_argument('-q', '--quiet',   action='store_true', help='Quiet output.')
    parser.add_argument('-nk','--no-console', action='store_true', help='Do not log to console.')
    parser.add_argument('-l', '--log-file', type=str, default=None, help='Optional log file')
   

    # --------------------------
    # Create first level parsers
    # --------------------------

    subparser = parser.add_subparsers(dest='command')

    parser_dbase  = subparser.add_parser('dbase',  help='dbase command')

    # ---------------------------------------
    # Create second level parsers for 'dbase'
    # ---------------------------------------

    subparser = parser_dbase.add_subparsers(dest='subcommand')
    dbgen = subparser.add_parser('generate',  help="Generate SQL file ready to be imported")
    dbgen.add_argument('-d', '--dbase',       type=isfile, required=True, help='path to the tess.db database')
    dbgen.add_argument('-i', '--input-file',  type=isfile, required=True, help='path to raw observations in CSV format')
    dbgen.add_argument('-o', '--output-file', type=str,    required=True, help='path to SQL output file')
 

    return parser

# ================ #
# MAIN ENTRY POINT #
# ================ #

def main():
    '''
    Utility entry point
    '''
    try:
        options = createParser().parse_args(sys.argv[1:])
        configureLogging(options)
        setup(options)
        name = os.path.split(os.path.dirname(sys.argv[0]))[-1]
        log.info(f"============== {name} {__version__} ==============")
        connection = open_database(options.dbase)
        package = f"{name}"
        command  = f"{options.command}"
        subcommand = f"{options.subcommand}"
        try: 
            command = importlib.import_module(command, package=package)
        except ModuleNotFoundError: # when debugging module in git source tree ...
            command  = f".{options.command}"
            command = importlib.import_module(command, package=package)
        getattr(command, subcommand)(connection, options)
    except KeyboardInterrupt as e:
        log.critical("[%s] Interrupted by user ", __name__)
    except Exception as e:
        log.critical("[%s] Fatal error => %s", __name__, str(e) )
        traceback.print_exc()
    finally:
        pass

main()
