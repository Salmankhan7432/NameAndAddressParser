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
    database_url = 'sqlite:///KnowledgeBase_TestDummy5.db'
    dictionary_file_path = 'JSONMappingDefault.json'
    # data_to_add = read_data_from_file(dictionary_file_path)
    data_to_add = {
        "NWF,WW,TN": {"USAD_SNO": [1], "USAD_SNM": [2], "USAD_SFIX": [3], "USAD_CTY": [4, 5], "USAD_STA": [6], "USAD_ZIP": [7]},
        "NWFWW,TN": {"USAD_SNO": [1], "USAD_SNaM": [2], "USAD_SFX": [3], "USAD_CTY": [4, 5], "USAD_STA": [6], "USAD_ZIP": [7]},
        "NWFWWTN": {"USAD_SNO": [1], "USAD_SNM": [2], "USAD_SFX": [3], "USAD_CTY": [4, 5], "USAD_STAt": [6], "USAD_ZIP": [7]},
        "NW,F,WW,TN": {"USAD_SNO": [1], "USAD_SNM": [2], "USAD_SFIX": [3], "USAD_CTY": [4, 5], "USAD_STA": [6], "USAD_ZIP": [7]},
        "NWF,WW,T,N": {"USAD_SNO": [1], "USAD_SNaM": [2], "USAD_SFX": [3], "USAD_CTY": [4, 5], "USAD_STA": [6], "USAD_ZIP3": [7]},
        "NW,FWWT,N": {"USAD_SNO": [1], "USAD_SNM": [2], "USAD_SFX": [3], "USAD_CTY": [4, 5], "USAD_STAt": [6], "USAD_ZIP": [7]},
        "N,WF,WW,TN": {"USAD_SNO": [1], "USAD_SNM": [2], "USAD_SFX": [3], "USAD_CTY": [4, 5], "USAD_STA": [6], "USAD_ZIP3": [7]},
        "NWFWW,T,N": {"USAD_SNO": [1], "USAD_SNM": [2], "USAD_SFX": [3], "USAD_CTY": [4, 5], "USAD_STA": [6], "USAD_ZIP": [7]},
        "NWFWWT,N": {"USAD_SNO": [1], "USAD_SNM": [2], "USAD_SFX": [3], "USAD_CTY": [4, 5], "USAD_STAt": [6], "USAD_ZIP": [7]}
        }

    add_data_to_database(database_url, data_to_add)
