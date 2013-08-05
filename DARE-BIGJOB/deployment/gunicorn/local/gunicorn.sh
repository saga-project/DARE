#!/bin/bash
  set -e
  LOGFILE=/var/log/gunicorn/dare.log
  LOGDIR=$(dirname $LOGFILE)
  NUM_WORKERS=1
  # user/group to run as
  USER=Sharath
  GROUP=staff
  cd /Users/Sharath/workspace/projects/DARE/DARE-BIGJOB/
  source bjdareenv/bin/activate
  test -d $LOGDIR || mkdir -p $LOGDIR
  exec python managedev.py run_gunicorn -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE 
