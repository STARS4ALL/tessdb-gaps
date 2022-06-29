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
import sys
import logging
# Access Jinja2 templaies withing the package
from pkg_resources import resource_filename

#--------------
# local imports
# -------------

from tdbgaps._version import get_versions

# ----------------
# Module constants
# ----------------

__version__ = get_versions()['version']
INSERT_TPL = resource_filename(__name__, os.path.join('templates', 'location.sql.j2'))
INPUT_FILENAME = 'Fotometros TESS-W - Despliegue.csv'

del get_versions
