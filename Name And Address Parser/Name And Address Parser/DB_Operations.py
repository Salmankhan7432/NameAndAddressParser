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

    def get_component_description(self, component):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()

            component_record = session.query(ComponentTable).filter_by(component=component).first()

            if component_record:
                return component_record.description
            else:
                return "Not Selected"

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
        Session = sessionmaker(bind=self.engine)
        session = None
        try:
            session = Session()
            for mask, components in data.items():
                try:
                    mask_record = session.query(MaskTable).filter_by(mask=mask).first()
                    if not mask_record:
                        mask_record = MaskTable(mask=mask)
                        session.add(mask_record)
                    session.flush()
    
                    mask_id = mask_record.mask
                    for values , component_description in components.items():
                        try:
                            component_record = session.query(ComponentTable).filter_by(description=component_description).first()
                            if not component_record:
                                pass
                            for value in values:
                                try:
                                    mapping_json_record = session.query(MappingJSON).filter_by(
                                        mask_index=mask_id,
                                        component_value=value
                                        ).first()
                                    if mapping_json_record:
                                        mapping_json_record.component_index=component_record.component
                                        mapping_json_record.component_value = value

                                    else:
                                        mapping_json_record = MappingJSON(
                                            mask_index=mask_id,
                                            component_index=component_record.component,
                                            component_value=value
                                        )
                                        session.add(mapping_json_record)
                                except IntegrityError as e:
                                        session.rollback()
                                        error_info = e.orig.args[0]
                                        if 'UNIQUE constraint failed' in error_info:
                                            print("Error: Duplicate entry. The combination of mask, component, and value must be unique.")
                                        else:   
                                            print(f"Error: {e}")
                                        continue
                        except IntegrityError as e:
                                    session.rollback()
                                    error_info = e.orig.args[0]
                                    if 'UNIQUE constraint failed' in error_info:
                                        print("Error: Duplicate entry. The combination of mask, component, and value must be unique.")
                                    else:   
                                        print(f"Error: {e}")
                                    continue
                except IntegrityError as e:
                            session.rollback()
                            error_info = e.orig.args[0]
                            if 'UNIQUE constraint failed' in error_info:
                                print("Error: Duplicate entry. The combination of mask, component, and value must be unique.")
                            else:   
                                print(f"Error: {e}")
                            continue
                
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
            if session is not None:
                session.close()


    def update_component_descriptions_interactively(self):
            try:
                Session = sessionmaker(bind=self.engine)
                session = Session()

                components = session.query(ComponentTable).all()

                for component in components:
                    current_description = component.description
                    new_description = input(f"Enter new description for component {component.component} (current: {current_description}): ")

                    if new_description:
                        component.description = new_description
                        print(f"Description updated for component {component.component}")
                    else:
                        print(f"Description for component {component.component} unchanged.")

                # Commit the changes
                session.commit()
                print("All changes committed.")

            finally:
                session.close()
    def Delete_records(self, component):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            
            component_record = session.query(ComponentTable).filter_by(component=component).first()
            
            if component_record:
                # Fetch all mask indices associated with the component
                linked_masks = session.query(MappingJSON).filter_by(component=component_record.component).all()
                
                # Delete records in the MappingJSON table first
                for mask in linked_masks:
                    session.query(MappingJSON).filter_by(component_index=component_record.component).delete()
                
                # Fetch masks associated with the component and delete them from MaskTable
                for mask in linked_masks:
                    mask_record = session.query(MaskTable).filter_by(mask=mask.mask).first()
                    if mask_record:
                        session.delete(mask_record)
                
                # Finally, delete the component from ComponentTable
                session.delete(component_record)
                session.commit()
                
        finally:
            session.close()
# database_url = 'sqlite:///KnowledgeBase_TestDummy.db'
# db_operations = DB_Operations(database_url)
# db_operations.Delete_records('USAD_SFX')