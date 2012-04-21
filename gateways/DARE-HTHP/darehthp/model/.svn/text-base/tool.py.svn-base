"""Person model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relation, backref

from darehthp.model.meta import Base


class tool(Base):
    __tablename__ = "tool"
    #__mapper_args__ = dict(order_by="submitted_time desc")

    #assuming these tools are independent executables and do not need to worry about paths
    id= Column(Integer, primary_key = True)
    name = Column(String(200), default = "")
    submitted_time = Column( String(100), default = "1" )    
    description = Column( String(100), default = "1" )
    
    # user info who uploads the tool or executable
    userid = Column( Integer, ForeignKey('user.id') )    
    user = relation('user', backref=backref('tools', order_by=id))
       
    
    def __repr__(self):
        return "<Person('%s')" % self.name
    
    def __init__(self, name='', email=''):
        self.name = name
