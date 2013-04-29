#!/usr/bin/env python
__author__ = "Sharath Maddineni"
__copyright_ = "Copyright 2011-2012, Sharath Maddineni"
__license__ = "MIT"


#import logging

#logging.basicConfig(level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p',
#                    format='%(asctime)s - %(name)s \
#                    - %(levelname)s - %(message)s')

#darelogger = logging.getLogger(name='DARE')

class DareLogger():
    def debug(self, p):
        print "DARE-Debug-%s" % p

    def info(self, p):
        print "DARE-info-%s" % p

    def error(self, p):
        print "DARE-error-%s" % p

darelogger = DareLogger()
