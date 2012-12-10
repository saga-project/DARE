#!/usr/bin/env python
__author__ = "Sharath Maddineni"
__copyright_ = "Copyright 2011-2012, Sharath Maddineni"
__license__ = "MIT"

__version_info__ = ('0', '8', '0174')
__version__ = '.'.join(__version_info__)

import os
import ConfigParser

from .helpers.misc import darelogger

darelogger.info("Loading DARE version: " + __version__)

try:
    _conf_file = os.path.expanduser('~/.darerc')
except:
    darelogger.error("Cannot find home directory")

if not os.path.exists(_conf_file):
    _conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dare.conf')

darelogger.info("Loading settings in %s" % _conf_file)

cfgparser = ConfigParser.ConfigParser()
cfgparser.read(_conf_file)
cfgdict = cfgparser.defaults()
COORDINATION_URL = str(cfgdict.get('coordination_url'))

darelogger.info("Bigjob COORDINATION_URL: %s " % COORDINATION_URL)
