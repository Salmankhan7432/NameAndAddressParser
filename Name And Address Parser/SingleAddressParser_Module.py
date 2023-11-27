# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 21:33:57 2023

@author: Salman Khan
"""


import re
# from tqdm import tqdm
# import pandas as pd
import json 
# import collections 
#Parsing 1st program
# import re
import os.path
import Rulebased as rulebased
from tkinter import messagebox
import PreprocessingNameAddress as PreProc
from DB_Operations import DB_Operations

from datetime import datetime,timedelta
today=datetime.today()
current_time = datetime.now().time()
time_string = current_time.strftime("%H:%M:%S")
unique = timedelta(microseconds=-1)



file_dir = os.path.dirname(os.path.realpath('__file__'))


from pathlib import Path

root_folder = Path(__file__).parents[1]

ExceptionList = []
def throwException(originalInput,initials):
    rules=rulebased.RuleBasedAddressParser.AddressParser(AddressList)
    ID = str(initials) + "Forced Exception_File " +  "-->01"
    ExceptionDict = {
        "Record ID": ID,
        "INPUT": originalInput,
        str(Mask_1): rules
    }
    # oldExceptionList = ExceptionList.append(ExceptionDict)
    
    if ExceptionList:
        ExceptionList[0]= ExceptionDict
        
    else:
        ExceptionList.append(ExceptionDict)
    
    
    
    Exception_file_name = initials+" " +str(current_time) +"_Forced_ExceptionFile.json"
    Exception_file_name = re.sub(r'[^\w_. -]', '_', Exception_file_name)
    path = 'Exceptions/ForcedExceptions/' + Exception_file_name
    with open(path, 'w', encoding='utf-8') as g:
        
        json.dump(ExceptionList, g, indent=4)
    return
def Address_Parser(line,initials,originalInput):
    global Result, Exception_file_name, FirstPhaseList, Mask_1, AddressList, rules
    Result={}
    db_operations = DB_Operations(database_url='sqlite:///KnowledgeBase_Test.db')
    Exception_=False
    Exception_file_name=""
    fileHandle = open('USAddressWordTable.txt', 'r',encoding="utf8")
    # Strips the newline character
    Observation=0
    Total=0
    Truth_Result={}
    dataFinal={}
    # Address = line
    FirstPhaseList=[]
    # Address=re.sub(',',' , ',line)
    # Address=re.sub(' +', ' ',Address)
    # Address=re.sub('[.]','',Address)
    #Address=re.sub('#','',Address)    
    # Address=Address.upper()
    PackAddress=PreProc.PreProcessingNameAddress().AddresssCleaning(line)
    # AddressList = re.split("\s|\s,\s ", Address)
    AddressList = PackAddress[0]
    AddressList= [item for item in AddressList if item]# != ","]
    #del(AddressList[len(AddressList)-1])
    TrackKey=[]
    Mask=[]
    Combine=""
    LoopCheck=1
    ID = "Single Line Exception_File " + str(initials) + "-->01"
    for A in AddressList:
        FirstPhaseDict={}
        NResult=False
        try:
            Compare=A[0].isdigit()
        except:
            print()
        if A==",":
            Mask.append(Combine)
            Combine=""
            FirstPhaseList.append(",")
            #FirstPhaseList.append("Seperator")
        elif Compare:
            Combine+="N"
            TrackKey.append("N")
            FirstPhaseDict["N"]=A
            FirstPhaseList.append(FirstPhaseDict)
        else:
            for line in fileHandle:
                fields=line.split('|')
                if A==(fields[0]):
                    NResult=True
                    temp=fields[1]
                    Combine+=temp[0]
                    FirstPhaseDict[temp[0]] = A
                    FirstPhaseList.append(FirstPhaseDict)
                    TrackKey.append(temp[0])
            if NResult==False:
                Combine+="W"
                TrackKey.append("W")
                FirstPhaseDict["W"] = A
                FirstPhaseList.append(FirstPhaseDict)
        if LoopCheck==len(AddressList):
            Mask.append(Combine)
        fileHandle.seek(0)
        LoopCheck+=1
    Mask_1=",".join(Mask)
    FirstPhaseList = [FirstPhaseList[b] for b in range(len(FirstPhaseList)) if FirstPhaseList[b] != ","]
    # data={}
    # with open('JSONMappingDefault.json', 'r+', encoding='utf-8') as f:
    #     data = json.load(f)
    Found=False
    FoundDict={}
    # for tk,tv in data.items():
    #     if(tk==Mask_1):
    #         FoundDict[tk]=tv
    #         Found=True
    #         break
    if db_operations.check_mask_exists(Mask_1):
        FoundDict[Mask_1] = db_operations.get_data_for_mask(Mask_1)
        Found = True
    if Found:
        Observation+=1
        Mappings=[]
        uiMappings = []
        for K2,V2 in FoundDict[Mask_1].items():
            FoundDict_KB=FoundDict[Mask_1]
            sorted_Found={k: v for k ,v in sorted(FoundDict_KB.items(), key=lambda item:item[1])}
        dict_found={}
        for k,v in sorted_Found.items():
            for i in v:
                dict_found[i]=k
        nest_list=[]
        print(dict_found)
        mask=Mask_1.replace(",","")
        for i in range(0,len(FirstPhaseList)):
            token=""
            for k,v in FirstPhaseList[i].items():
                token=v
                # print(dict_found[i+1])
                component_description = db_operations.get_component_description(dict_found[i+1])
                # print(component_description)
            uiMappings.append([token,dict_found[i+1],mask[i],component_description])
        # print(uiMappings)
        
        for K2,V2 in sorted_Found.items():
            Temp=""
            Merge_token=""
            for p in V2:
                for K3,V3 in FirstPhaseList[p-1].items():
                   Temp+=" "+V3
                   Temp=Temp.strip()      
                   Merge_token+= ""+K3
                   found = False
                   for entry in Mappings:
                       if entry[0] == K2:
                           
                           entry[1] += K3
                           entry[2] = ""
                           entry[2] += Temp
                           found = True
                           break
                   if not found:
                       Mappings.append([K2, K3, V3])
                       break

        FoundDict_KB=FoundDict[Mask_1]
        sorted_Found={k: v for k ,v in sorted(FoundDict_KB.items(), key=lambda item:item[1])}
                  
        try:
            Result["Input"]= originalInput
            Result["Output"]=uiMappings
            # messagebox.showinfo("Success!",f"{originalInput}\n\nAddress Successfully Parsed!\n\nOutput derived from Active Learning")
        except:
            Result["Input"]= originalInput
            Result["Output"]=uiMappings
            # messagebox.showinfo("Success!",f"{originalInput}\n\nAddress Successfully Parsed!\n\nOutput derived from Active Learning")

        
        
        OutputDict = {
                "Record ID": ID,
                "INPUT": originalInput,
                str(Mask_1): Mappings
            }
        Output_file_name=initials+str(current_time)+"_Output.json"
        Output_file_name=re.sub(r'[^\w_. -]', '_', Output_file_name)
        path= 'Output/Single Line Output/'+Output_file_name
        with open(path,'w', encoding='utf-8') as g:
            g.seek(0)
            # Stat=originalInput,Mappings
            json.dump(OutputDict,g,indent=4)
            g.truncate
        
    else:
        Exception_=True
        rules=rulebased.RuleBasedAddressParser.AddressParser(AddressList)
        # print(rules)
        ExceptionDict = {
            "Record ID": ID,
            "INPUT": originalInput,
            str(Mask_1): rules
        }
        Result["Input"]=originalInput
        Result["Output"]=rules
        for m in Result["Output"]:
            component = m[1]
            component_description = db_operations.get_component_description(component)
            m.append(component_description)
        print(Result["Output"])
        # messagebox.showwarning("Exception!",f"Exception is Created for the Address\n\n{originalInput}\n\nOutput Derived from Rulebased Learning")

        
        if ExceptionList:
            ExceptionList[0] = ExceptionDict
            
        else:
            ExceptionList.append(ExceptionDict)
        Exception_file_name = initials+ " " + str(current_time) + "_ExceptionFile.json"
        Exception_file_name = re.sub(r'[^\w_. -]', '_', Exception_file_name)
        path = 'Exceptions/SingleException/' + Exception_file_name
        with open(path, 'w', encoding='utf-8') as g:
            json.dump(ExceptionList, g, indent=4)
            g.truncate
            
        
       
        
        
    Total+=1
   
    return (Result, Mask_1,Exception_file_name, throwException,Exception_)

# Convert=Address_Parser("5506 A Street 324 2535 64356 3452323 Little, Rock, AR 72205",'initial',"5506 A Street Little Rock AR 72205")
# Result=Convert[0]
# print(Result)
# print(type(Result))

# print("Final Correct Address Parsing Percentage",Count_of_Correct/Total_Count*100)
# print("Address Matching Report")
# print("Total=",Count)
# print("Matched Addresses=",Observation)
# print("Percentage of Matched",(Observation/Count)*100)
        # print("Mask Generated is ",Mask_1)
    # print("Index\tMaskToken\t\tAddress Token")
    # i=1
    # for k in FirstPhaseList:
    #     for key,value in k.items():
    #         print(i,"\t\t",key,"\t\t\t\t",value) 
    #     i+=1