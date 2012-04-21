"""Person model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relation, backref

from darehthp.model.meta import Base

#this tool basically contains the information about the tool locality

class toolinfo(Base):
    __tablename__ = "toolinfo"
    #__mapper_args__ = dict(order_by="submitted_time desc")

    id= Column(Integer, primary_key = True)
    name = Column(String(200), default = "")
    submitted_time = Column( String(100), default = "1" )    
    sysytemarchitecture = Column( String(100), default = "1" )
    
    # type-> basically to define the path on a machine or uploading the executable
    type = Column( String(100), default = "1" )
    toolpath = Column( String(100), default = "1" )
    
    toolid = Column( Integer, ForeignKey('tool.id') )    
    tools = relation('tool', backref=backref('toolinfos', order_by=id))


