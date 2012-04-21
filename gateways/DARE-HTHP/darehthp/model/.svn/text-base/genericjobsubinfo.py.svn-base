"""job model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relation, backref

from darehthp.model.meta import Base


class genericjobsubinfo(Base):
    __tablename__ = "genericjobsubinfo"
    #__mapper_args__ = dict(order_by="submitted_time desc")

    id             = Column(Integer, primary_key = True)
    submitted_time = Column( String(100), default = "")
    key            = Column(String(50), default = "") 
    value          = Column(String(50), default = "") 
    jobinfoid          = Column( Integer, ForeignKey('jobinfo.id') )
    
    #assign relation to access the realtion backre job.jobinfo or jobinfo.jobs
    jobs = relation('jobinfo', backref=backref('genericjobsubinfo'))

        
    def __init__(self):
        #self.appname = appname
        #self.email = email
        passsss
        
# def __repr__(self):
# pass
  #return '%s')" % self.appname       
#addresses = relationship("Address",
		 #       primaryjoin="and_(User.id==Address.user_id, "
	   #             "Address.email.startswith('tony'))",
		#        backref="user") 
#cascade="all,delete-orphan"
                    #job disc
                    #job_location: local or remote
