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
    data_to_add = {
        "NWFFSW,WW,TN": {"USAD_SNO": [1], "USAD_SNM": [2], "USAD_SFX": [3, 4], "USAD_ANM": [5], "USAD_ANO": [6], "USAD_CTY": [7, 8], "USAD_STA": [9], "USAD_ZIP": [10]},
        "NDWF,WW,TN": {"USAD_SNO": [1], "USAD_SPR": [2], "USAD_SNM": [3], "USAD_SFX": [4], "USAD_CTY": [5, 6], "USAD_STA": [7], "USAD_ZIP": [8]}
    }

    add_data_to_database(database_url, data_to_add)
