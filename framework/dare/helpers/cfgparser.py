#!/usr/bin/env python
__author__ = "Sharath Maddineni"
__copyright_ = "Copyright 2011-2012, Sharath Maddineni"
__license__ = "MIT"


import ConfigParser
import os
import sys
from dare import darelogger


class CfgParser(object):
    def __init__(self, conf_file="/default/conf/file/"):
        self.conf_file = conf_file
        darelogger.info('Loading conf file %s' % conf_file)
        if not os.path.exists(self.conf_file):
            raise RuntimeError("Cannot find %s " % self.conf_file)

        #parse job conf file
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.conf_file)

    def SectionDict(self, section):
        lst = self.config.items(section)
        dct = {}
        for i in range(len(lst)):
            dct[lst[i][0]] = lst[i][1]
        return dct


class CfgWriter(object):
    def __init__(self, conffile):
        self.dare_config = ConfigParser.ConfigParser()
        self.conffile = conffile

    def add_section(self, section_params):
        section_name = section_params.pop("name")
        self.dare_config.add_section(section_name)

        for k, v in section_params.items():
            self.dare_config.set(section_name, k, v)

    def write(self):
        try:
            dare_cfgfile = open(self.conffile, 'w')
            self.dare_config.write(dare_cfgfile)
            dare_cfgfile.close()
        except:
            error = "Could not write DARE config file"
            raise RuntimeError(error)
        return True
