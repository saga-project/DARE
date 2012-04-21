"""job queue model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Binary
from sqlalchemy.orm import relation, backref
from darecactus.model.meta import Base

#this table should contain the information about thornlist
#will be deleted once the get to the status as done

class thornlist(Base):
    __tablename__ = "thornlist"
    #__mapper_args__ = dict(order_by="submitted_time desc")

    id= Column(Integer, primary_key = True)
    filename = Column(String(200), default = "")
    thornfile = Column(Binary, default= "")
    description = Column(String(200), default = "")    
    submitted_time = Column( String(100), default = "")
    userid = Column(Integer, ForeignKey('user.id'))
    users = relation('user', backref=backref('thornlist', order_by=id))
