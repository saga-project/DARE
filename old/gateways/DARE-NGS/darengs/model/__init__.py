"""The application's model objects"""
from darengs.model.meta import Session, Base

from darengs.model.job import job
from darengs.model.jobinfo import jobinfo
from darengs.model.user import user
from darengs.model.tool import tool
from darengs.model.toolinfo import toolinfo
#from darengs.model.toolparam import toolparam
#from darengs.model.tooloperationalinfo import tooloperationalinfo


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""    
    Session.configure(bind=engine)
