case "$1" in
  start)
    paster serve --daemon --pid-file=paster.pid --reload --log-file=paster.log hthpdevel.ini start
    ;;
  stop)
    paster serve --daemon --pid-file=paster.pid --log-file=paster.log  hthpdevel.ini stop
    ;;
  restart)
    paster serve  --daemon --pid-file=paster.pid  --reload --log-file=paster.log hthpdevel.ini restart
    ;;
  recreatedb)
    paster setup-app development_model.ini 
    ;;

  *)
    echo $"Usage: $0 {start|stop|restart}"
    exit 1
esac

