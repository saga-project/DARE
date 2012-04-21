#contains various job manipulation techniques

import time
import os
import sys

from sqlalchemy.sql import and_, or_

try:
     job= meta.Session.query(model.job)
except:

    DARENGS_HOME = os.path.abspath(os.path.join(os.path.abspath(__file__),"..", "..", ".."))
    sys.path.insert(0,DARENGS_HOME)         
    from paste.deploy import appconfig
    from pylons import config
    from darengs.config.ntenvironment import load_environment   
    import sqlalchemy
    engine = sqlalchemy.create_engine("sqlite://"+ DARENGS_HOME + "/development.db")
    import darengs.model as model
    import darengs.model.meta as meta
    conf = appconfig("config:"+ DARENGS_HOME +"/ngsdevel.ini", relative_to='.')
    load_environment(conf.global_conf, conf.local_conf)
    
from ModelHelper import *
