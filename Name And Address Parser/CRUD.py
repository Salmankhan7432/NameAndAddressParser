# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:59:53 2023

@author: Salman Khan
"""

# main.py
import json
from DB_Operations import DB_Operations


def add_data_to_database(database_url, data_to_add):
    db_operations = DB_Operations(database_url)
    db_operations.add_data(data_to_add)
def read_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    database_url = 'sqlite:///KnowledgeBase_Test.db'
    dictionary_file_path = 'JSONMappingDefault.json'
    # data_to_add = read_data_from_file(dictionary_file_path)
    data_to_add = {'NWFWW,TN': {'1': 'Street Number', '2': 'Street Name', '3': 'Street Suffix', '4': 'City Name', '5': 'City Name', '6': 'State Name', '7': 'Zip Code'}}

    add_data_to_database(database_url, data_to_add)
