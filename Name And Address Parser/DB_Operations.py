# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:46:17 2023

@author: skhan2
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORM import MaskTable, ComponentTable, MappingJSON  # Replace with the actual file containing your model definitions

def open_database(database_url):
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def get_Mask_data(session):
    return session.query(MaskTable).all()

def get_Component_data(session):
    return session.query(ComponentTable).all()

def get_MappingJSON_data(session):
    return session.query(MappingJSON).all()
