"""job model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relation, backref

from darehthp.model.meta import Base


class jobinfo(Base):
    __tablename__ = "jobinfo"
    #__mapper_args__ = dict(order_by="submitted_time desc")

    id             = Column(Integer, primary_key = True)
    description    = Column(String(200), default = "")
    submitted_time = Column( String(100), default = "")
    key            = Column(String(50), default = "")
    value          = Column(String(50), default = "")
    jobmetaid          = Column( Integer, ForeignKey('jobmeta.id') )

    #assign relation to access the realtion backre job.jobinfo or jobinfo.jobs
    jobmetas = relation('jobmeta', backref=backref('jobinfo'))



    def __init__(self):
        pass

