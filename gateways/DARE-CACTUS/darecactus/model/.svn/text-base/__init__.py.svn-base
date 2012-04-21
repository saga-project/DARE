"""The application's model objects"""
from darecactus.model.meta import Session, Base

from darecactus.model.job import job
from darecactus.model.jobinfo import jobinfo
from darecactus.model.user import user
from darecactus.model.thornlist import thornlist
from darecactus.model.paramlist import paramlist

#from darecactus.model.toolparam import toolparam
#from darecactus.model.tooloperationalinfo import tooloperationalinfo


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""    
    Session.configure(bind=engine)
