#!/bin/bash
  set -e
  LOGFILE=/var/log/gunicorn/dare.log
  LOGDIR=$(dirname $LOGFILE)
  NUM_WORKERS=3
  # user/group to run as
  USER=dare
  GROUP=dare
  cd /opt/DARE/DARE-BIGJOB/
  source /opt/dare-virtual-env/bjdareenv/bin/activate
  test -d $LOGDIR || mkdir -p $LOGDIR
  exec python manage.py run_gunicorn -b 0.0.0.0:8080 -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE