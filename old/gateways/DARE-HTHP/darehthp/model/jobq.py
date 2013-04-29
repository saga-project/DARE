"""job queue model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relation, backref

from darehthp.model.meta import Base

#this table should contain the information about the jobs that are in the queue and they
#will be deleted once the get to the status as done

class jobq(Base):
    __tablename__ = "jobq"
    #__mapper_args__ = dict(order_by="submitted_time desc")

    id= Column(Integer, primary_key = True)
    qstatus = Column(String(200), default = "")
    submitted_time = Column( String(100), default = "")
    type = Column(String(100),default = "" )
    
    jobid = Column( Integer, ForeignKey('job.id') )    
    job = relation('job', backref=backref('jobqs', order_by=id))