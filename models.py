import datetime

from database import Base
from sqlalchemy import (Boolean, Column, DateTime, Float, Integer,
                        String)



class BaseInfoMixin:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    
    
    
class User(BaseInfoMixin, Base):
    __tablename__ = 'userdata'
    
    name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    
    login = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    
    age = Column(String, nullable=False)
    
    ip = Column(String)

    def __repr__(self) -> str:
        return f'New user: {self.name} -> #{self.id}'
    