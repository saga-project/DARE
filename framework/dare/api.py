#!/usr/bin/env python

__author__    = "Sharath Maddineni"
__email__     = "smaddineni@cct.lsu.edu"
__copyright__ = "Copyright 2011, Sharath Maddineni"
__license__   = "MIT"

class ComputeUnitStates(object):
    Unknown = 0
    New = 1
    Running = 2
    Done = 3
    Canceled = 4
    Failed = 5

class ComputePilotStates(object):
    Unknown = 0
    New = 1
    Running = 2
    Done = 3
    Canceled = 4
    Failed = 5
    Queue = 6

class DataPilotStates(object):
    Unknown = 0
    New = 1
    Running = 2
    Done = 3
    Canceled = 4
    Failed = 5


    
class DataUnitStates(object):
    Unknown = 0
    New = 1
    Running = 2
    Done = 3
    Canceled = 4
    Failed = 5

