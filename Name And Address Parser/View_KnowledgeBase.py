# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:57:31 2023

@author: skhan2
"""

from DB_Operations import open_database, get_Mask_data, get_Component_data, get_MappingJSON_data

database_url = 'sqlite:///KnowledgeBase1.db'  # Replace with your actual database URL

session = open_database(database_url)

# Query and print data from Mask Table
mask_data = get_Mask_data(session)
print("Data from Mask Table:")
for row in mask_data:
    print(f"ID: {row.id}, Mask: {row.mask}, Index: {row.index}")

# Query and print data from Component Table
component_data = get_Component_data(session)
print("\nData from Component Table:")
for row in component_data:
    print(f"ID: {row.id}, Component: {row.component},Description: {row.description}, Index: {row.index}" )

# Query and print data from MappingJSON Table
MappingJSON_data = get_MappingJSON_data(session)
print("\nData from MappingJSON Table:")
for row in MappingJSON_data:
    print(f"ID: {row.id}, Mask Index: {row.mask_index}, Component Index: {row.component_index}, Component Value: {row.component_value}")

# Close the session
session.close()