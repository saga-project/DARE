"""The application's model objects"""
from darehthp.model.meta import Session, Base

from darehthp.model.job import job
from darehthp.model.jobinfo import jobinfo
from darehthp.model.jobmeta import jobmeta

from darehthp.model.user import user
from darehthp.model.tool import tool
from darehthp.model.toolinfo import toolinfo

# for generic job submission
#from darehthp.model.genericjobsubinfo import genericjobsubinfo
#from darehthp.model.genericjobinfo import genericjobinfo

#from darehthp.model.toolparam import toolparam
#from darehthp.model.tooloperationalinfo import tooloperationalinfo


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
