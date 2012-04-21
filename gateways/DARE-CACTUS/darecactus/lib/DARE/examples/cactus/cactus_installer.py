#!/usr/bin/env python
import os
import sys

CACTUS_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
CACTUS_INST_TEST_PATH = os.path.join(CACTUS_ROOT_PATH, 'Cactus', 'exe', 'cactus_sim')

test_cactus_installation = os.path.isfile(CACTUS_INST_TEST_PATH)
if not test_cactus_installation:
    SIM_PATH = os.path.join(CACTUS_ROOT_PATH, 'Cactus','simfactory','bin', 'sim')
    os.system(SIM_PATH+ ' build')
