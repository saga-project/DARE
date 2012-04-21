case "$1" in
  start)
    paster serve --daemon --pid-file=paster.pid --log-file=paster.log development.ini start
    ;;
  stop)
    paster serve --daemon --pid-file=paster.pid --log-file=paster.log  development.ini stop
    ;;
  restart)
    paster serve  --daemon --pid-file=paster.pid  --log-file=paster.log development.ini restart

    ;;
  recreatedb)
    paster setup-app development_model.ini 
    ;;

  *)
    echo $"Usage: $0 {start|stop|restart|recreatedb}"
    exit 1
esac

