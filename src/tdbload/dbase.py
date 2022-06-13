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

import logging


#--------------
# local imports
# -------------


# ----------------
# Module constants
# ----------------

log = logging.getLogger("tdbload")

# ------------
# Entry points
# ------------

def generate(connection, options):
	log.info(f"Generate with options {str(options)}")