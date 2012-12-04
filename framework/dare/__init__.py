#!/usr/bin/env python
__author__ = "Sharath Maddineni"
__copyright_ = "Copyright 2011-2012, Sharath Maddineni"
__license__ = "MIT"


import os
import ConfigParser

from .helpers.misc import darelogger

version = "latest"

try:
    version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'VERSION')
    version = open(version_file).read().strip()
    darelogger.info("Loading DARE version: " + version)

except IOError:
    darelogger.error("Cannot read the verison file %s" % version_file)


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
COORDINATION_URL = str(cfgdict.get('coordination_url', "redis://gw68.quarry.iu.teragrid.org:2525"))

darelogger.info("Bigjob COORDINATION_URL: %s " % COORDINATION_URL)
