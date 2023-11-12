# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:46:17 2023

@author: Salman Khan
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import json
from ORM import MaskTable, ComponentTable, MappingJSON


class DB_Operations:
    def __init__(self, database_url):
        self.database_url = database_url
        self.engine = create_engine(database_url)

    def open_database(self):
        return self.engine
    
    def check_mask_exists(self, mask):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            mask_record = session.query(MaskTable).filter_by(mask=mask).first()
            if mask_record: 
                return bool(mask_record)
            else:
                pass# print("Mask Not Found")
        finally:
            session.close()
    
    def get_data_for_mask(self, mask):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            mask_record = session.query(MaskTable).filter_by(mask=mask).first()
    
            if mask_record:
                data_records = session.query(MappingJSON).filter_by(mask_index=mask_record.mask).order_by(MappingJSON.component_value).all()

                result_dict = {}
                # for record in data_records:
                #     result_dict[record.component_value] = record.component_index
                for record in data_records:
                    if record.component_index not in result_dict:
                        result_dict[record.component_index] = [record.component_value]
                    else:
                        result_dict[record.component_index].append(record.component_value)

                # print(result_dict)
                return result_dict
            else:
                print('{mask} not found in MaskTable')
        finally:
            session.close()



    
    def get_Mask_data(self):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            return session.query(MaskTable).all()

        finally:
            session.close()

    def get_Component_data(self):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            return session.query(ComponentTable).all()

        finally:
            session.close()

    def get_MappingJSON_data(self):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            return session.query(MappingJSON).all()

        finally:
            session.close()
    

    def add_data(self, data):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()

            for mask, components in data.items():
                mask_record = session.query(MaskTable).filter_by(mask=mask).first()
                if not mask_record:
                    mask_record = MaskTable(mask=mask)
                    session.add(mask_record)
                    session.commit()

                mask_id = mask_record.mask

                for component, values in components.items():
                    component_record = session.query(ComponentTable).filter_by(component=component).first()
                    if not component_record:
                        component_record = ComponentTable(
                            component=component,
                            description=input(f"Give a description for {component}:")
                        )
                        session.add(component_record)
                        session.commit()

                    for value in values:
                        mapping_json_record = MappingJSON(
                            mask_index=f"{mask_id}",
                            component_index=component_record.component,
                            component_value=value
                        )
                        session.add(mapping_json_record)

            session.commit()

        except IntegrityError as e:
            error_info = e.orig.args[0]
            if 'UNIQUE constraint failed' in error_info:
                print("Error: Duplicate entry. The combination of mask, component, and value must be unique.")
                duplicate_data = []
                for mask, components in data.items():
                    duplicate_data.append({mask: components})
                with open('duplicate_data.json', 'a') as file:
                    json.dump(duplicate_data, file)
                    file.write('\n')
                print("Duplicate Dictionaries are added to the file")
            else:
                print(f"Error: {e}")

        finally:
            session.close()

