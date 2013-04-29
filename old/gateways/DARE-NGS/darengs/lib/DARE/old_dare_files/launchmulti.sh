#!/bin/sh

BIGJOB_DIR=/home/marksant/proj/bigjob
export PYTHONPATH=${PYTHONPATH}:${BIGJOB_DIR}

python bfast_multi_manyjob.py -j darefiles/jobconf/1-job.conf
