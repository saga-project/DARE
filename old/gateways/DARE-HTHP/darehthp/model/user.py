"""Person model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relation, backref

from darehthp.model.meta import Base


class user(Base):
    __tablename__ = "user"
   # __mapper_args__ = dict(order_by="date desc")

    id= Column(Integer, primary_key = True)
    email = Column(String(200), nullable=False)
    name = Column(String(200), default = "")
    password = Column( String(200), nullable=False)
    organization = Column( String(100), nullable=False)
    submitted_time = Column(String(30), nullable=True)
    salt = Column( String(100), default = "hello")
        
    def __repr__(self):
        return "<user('%s')" % self.name
    

