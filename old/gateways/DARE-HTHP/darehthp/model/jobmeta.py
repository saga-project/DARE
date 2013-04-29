"""job model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relation, backref

from darehthp.model.meta import Base


class jobmeta(Base):
    __tablename__ = "jobmeta"
    #__mapper_args__ = dict(order_by="submitted_time desc")

    id             = Column(Integer, primary_key = True)
    description    = Column(String(200), default = "")
    submitted_time = Column( String(100), default = "")
    metatype       = Column(String(200), default = "")
    someid         = Column(String(20), default = "")

    jobid          = Column( Integer, ForeignKey('job.id') )

    #assign relation to access the realtion backref job.jobinfo or jobinfo.jobs
    jobs = relation('job', backref=backref('jobmeta'))



    def __init__(self):
        pass

