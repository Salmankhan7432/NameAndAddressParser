# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:59:53 2023

@author: Salman Khan
"""

# main.py
import json
from DB_Operations import DB_Operations
from ORM import User,UserRole,MaskTable, ComponentTable, MappingJSON, ExceptionTable, MapCreationTable

def add_data_to_database(database_url, data_to_add):
    db_operations = DB_Operations(database_url)
    def add_data(self, data_to_add):
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
                    for components , values in components.items():
                        try:
                            component_record = session.query(ComponentTable).filter_by(component=components).first()
                            
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
def read_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    database_url = 'sqlite:///KnowledgeBase_Test.db'
    dictionary_file_path = 'JSONMappingDefault.json'
    data_to_add = read_data_from_file(dictionary_file_path)
    # data_to_add = {'NWFWW,TN': {'1': 'Street Number', '2': 'Street Name', '3': 'Street Suffix', '4': 'City Name', '5': 'City Name', '6': 'State Name', '7': 'Zip Code'}}

    add_data_to_database(database_url, data_to_add)
