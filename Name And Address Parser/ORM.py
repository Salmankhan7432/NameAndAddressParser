# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:09:42 2023

@author: Salman Khan
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import PrimaryKeyConstraint

Base = declarative_base()

engine = create_engine('sqlite:///KnowledgeBase_TestDummy5.db')

Session = sessionmaker(bind=engine)
session = Session()

class MaskTable(Base):
    __tablename__ = 'maskTable'
    mask = Column(String, primary_key=True)
    # index = Column(Integer, unique=True)
    
    mapping_json = relationship('MappingJSON', back_populates='mask', cascade='all, delete-orphan', single_parent=True)

class ComponentTable(Base):
    __tablename__ = 'componentTable'
    # id = Column(Integer, primary_key=True)
    component = Column(String, primary_key=True)
    # index = Column(Integer, unique=True)
    description = Column(String)
    
    mapping_json = relationship('MappingJSON', back_populates='component', cascade='all, delete-orphan', single_parent=True)

class MappingJSON(Base):
    __tablename__ = 'mappingJSON'
    # id = Column(Integer, primary_key=True)
    mask_index = Column(String, ForeignKey('maskTable.mask'))
    component_index = Column(String, ForeignKey('componentTable.component'))
    component_value = Column(Integer)

    mask = relationship('MaskTable', foreign_keys=[mask_index], back_populates='mapping_json')
    component = relationship('ComponentTable', foreign_keys=[component_index], back_populates='mapping_json')
    
    __table_args__ = (
        PrimaryKeyConstraint('mask_index','component_value'),
    )
    
    def __eq__(self, other):
        if isinstance(other, MappingJSON):
            return (
                self.mask_index == other.mask_index and
                self.component_index == other.component_index and
                self.component_value == other.component_value
            )
        return NotImplemented
