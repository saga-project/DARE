#contains various job manipulation techniques

import time
import os
import sys
DARECACTUS_HOME = os.path.abspath(os.path.join(os.path.abspath(__file__),"..", "..", ".."))
sys.path.insert(0,DARECACTUS_HOME)  

from sqlalchemy.sql import and_, or_

try:
     job= meta.Session.query(model.job)

except:  
    from paste.deploy import appconfig
    from pylons import config
    from darecactus.config.ntenvironment import load_environment   
    import sqlalchemy
    engine = sqlalchemy.create_engine("sqlite://"+ DARECACTUS_HOME + "/development.db")
    import darecactus.model as model
    import darecactus.model.meta as meta
    conf = appconfig("config:"+ os.path.join(DARECACTUS_HOME, "cactusdevel.ini"), relative_to='.')
    load_environment(conf.global_conf, conf.local_conf)
    
from cactusormhelper import *
from userormhelper import *