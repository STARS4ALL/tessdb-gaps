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
import logging
# Access SQL scripts withing the package
from pkg_resources import resource_filename

#--------------
# local imports
# -------------

# ----------------
# Module constants
# ----------------

NAMESPACE = 'dbase'


# DATABASE RESOURCES
SQL_SCHEMA           = resource_filename(__name__, os.path.join('sql', 'schema.sql'))
SQL_INITIAL_DATA_DIR = resource_filename(__name__, os.path.join('sql', 'initial' ))
SQL_UPDATES_DATA_DIR = resource_filename(__name__, os.path.join('sql', 'updates' ))

# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger("tdbgaps")
