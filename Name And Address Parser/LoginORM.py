# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 03:07:38 2024

@author: skhan2
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///User_Auth.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

class UserRole(Base):
    __tablename__ = 'rolesTable'
    # id = Column(Integer, primary_key=True)
    RoleName = Column(String, primary_key=True)

    def __repr__(self):
        return f"<UserRole(name='{self.RoleName}')>"

class User(Base):
    __tablename__ = 'usersTable'
    id = Column(Integer, primary_key=True)
    FullName = Column(String)
    UserName = Column(String, unique=True)
    Email = Column(String, unique=True)
    Password = Column(String)
    role = Column(Integer, ForeignKey('rolesTable.RoleName'))
    stats = Column(String)

    roles = relationship("UserRole")

    def __repr__(self):
        return f"<User(username='{self.UserName}', role_id={self.role_id})>"

Base.metadata.create_all(engine)
