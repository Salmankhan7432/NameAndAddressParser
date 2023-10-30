# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:09:42 2023

@author: skhan2
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Define the base for declarative models
Base = declarative_base()

# Create a SQLite database in memory (you can change this to your desired database)
engine = create_engine('sqlite:///KnowledgeBase1.db')

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define the Mask Table (Table 1)
class MaskTable(Base):
    __tablename__ = 'maskTable'
    id = Column(Integer, primary_key=True)
    mask = Column(String)
    index = Column(Integer, unique=True)
    
    mapping_json = relationship('MappingJSON', back_populates='mask', cascade='all, delete-orphan', single_parent=True)

# Define the Component Table (Table 2)
class ComponentTable(Base):
    __tablename__ = 'componentTable'
    id = Column(Integer, primary_key=True)
    component = Column(String)
    index = Column(Integer, unique=True)
    description = Column(String)
    
    mapping_json = relationship('MappingJSON', back_populates='component', cascade='all, delete-orphan', single_parent=True)

# Define the Mask Component Index table (Table 3)
class MappingJSON(Base):
    __tablename__ = 'mappingJSON'
    id = Column(Integer, primary_key=True)
    mask_index = Column(Integer, ForeignKey('maskTable.index'))
    component_index = Column(Integer, ForeignKey('componentTable.index'))
    component_value = Column(Integer)

    # Define the relationships
    mask = relationship('MaskTable', foreign_keys=[mask_index], back_populates='mapping_json')
    component = relationship('ComponentTable', foreign_keys=[component_index], back_populates='mapping_json')

# Create the tables in the database
Base.metadata.create_all(engine)

# # Add data to Table 1
# data_table1 = [
#     ("NWFFWWTN", 1),
#     ("NWFFWWTW", 2)
# ]

# for mask, index in data_table1:
#     entry = MaskTable(mask=mask, index=index)
#     session.add(entry)

# # Add data to Table 2
# data_table2 = [
#     ("USAD_SNO", 1, "Street Number"),
#     ("USAD_SNM", 2, "Street Name"),
#     ("USAD_SFX", 3, "Street Suffix"),
#     ("USAD_CTY", 4, "City"),
#     ("USAD_STA", 5, "State"),
#     ("USAD_ZIP", 6, "Zip Code")
# ]

# for component, index, description in data_table2:
#     entry = ComponentTable(component=component, index=index, description=description)
#     session.add(entry)

# # Add data to Table 3
# data_table3 = [
#     (1, 1, 1),
#     (1, 2, 2),
#     (1, 3, 3),
#     (1, 4, 4),
#     (1, 5, 5),
#     (1, 6, 6),
#     (2, 1, 1),
#     (2, 1, 2),
#     (2, 1, 3),
#     (2, 4, 4),
#     (2, 5, 5),
#     (2, 6, 6),
#     (2, 7, 7)
# ]

# for mask_index, component_index, component_value in data_table3:
#     entry = MappingJSON(mask_index=mask_index, component_index=component_index, component_value=component_value)
#     session.add(entry)

# # Commit the changes to the database
# session.commit()

