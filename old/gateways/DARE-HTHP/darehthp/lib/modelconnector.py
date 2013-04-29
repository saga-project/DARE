#contains various job manipulation techniques
import time
import os
import sys

from sqlalchemy.sql import and_, or_
try:
     job= meta.Session.query(model.job)
except:
    DAREHTHP_HOME = os.path.abspath(os.path.join(os.path.abspath(__file__),"..", "..", ".."))
    sys.path.insert(0,DAREHTHP_HOME)
    from paste.deploy import appconfig
    from pylons import config
    from darehthp.config.ntenvironment import load_environment
    import sqlalchemy
    engine = sqlalchemy.create_engine("sqlite://"+ DAREHTHP_HOME + "/development.db")
    import darehthp.model as model
    import darehthp.model.meta as meta
    conf = appconfig("config:"+ DAREHTHP_HOME +"/hthpdevel.ini", relative_to='.')
    load_environment(conf.global_conf, conf.local_conf)
from modelhelper import *
