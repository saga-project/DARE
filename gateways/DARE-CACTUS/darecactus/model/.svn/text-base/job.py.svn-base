"""job queue model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relation, backref

from darecactus.model.meta import Base

#this table should contain the information about the jobs that are in the queue and they
#will be deleted once the get to the status as done

class job(Base):
    __tablename__ = "job"
    #__mapper_args__ = dict(order_by="submitted_time desc")

    id= Column(Integer, primary_key = True)
    status = Column(String(200), default = "")
    submitted_time = Column( String(100), default = "")
    type = Column(String(100),default = "" )    
    detail_status = Column(String(100),default = "" ) 
    dareprocess_id = Column(String(100),default = "" ) 
    userid = Column(Integer, ForeignKey('user.id'))
    users = relation('user', backref=backref('jobs', order_by=id))
