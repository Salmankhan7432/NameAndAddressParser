# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 00:17:34 2022

@author: onais
"""


import re
from tqdm import tqdm
import pandas as pd
import json 
#hg
DF=[]
ii=0
count = 0
FinalList=[]
# Strips the newline character
DF=pd.DataFrame()
C=1
CC=1
JsonData={}
AllName_Key_Value_As_MASK_Comp={}
USNAME_Conversion_Dict={"1":"Prefix Title","2":"Given Name", "3":"Surname","4" :"Generational Suffix", "5":"Suffix Title"}

i=1
List_Index_Mask={}
with open('NameExceptionFile.json','r+',encoding='utf-8') as d:
    FirstPhaseLisCopyt=json.load(d)
    FirstPhaseList=FirstPhaseLisCopyt
    AddOrRemove=False
    MaskComparision={}
    for Key, Value in FirstPhaseLisCopyt.items():
        for Key1,Key2 in MaskComparision.items():
            if(Key==Key1):
                FirstPhaseList.pop(Key)
    Break=False
    for Key,Value in list(FirstPhaseList.items()):
        MaskI=1
        USNAME_Mapping={"Prefix Title":[],"Given Name":[], "Surname":[],"Generational Suffix":[],"Suffix Title":[]}
        Name=""
        for k in Value:
            for m,n in k.items():
                Name+=" "+n
    
        for k in Value:
            for k1,v1 in USNAME_Conversion_Dict.items():
                print(v1,"=",k1)
            print("Name For Reference")
            print(Name)
            print(k,"---> (Enter Index of Component)")
            temp=(input(""))
            if temp not in USNAME_Conversion_Dict.keys():
                Break=True
                break
            USNAME_Mapping[USNAME_Conversion_Dict[temp]].append(MaskI)
            MaskI+=1
        dict={k: v for k, v in USNAME_Mapping.items() if v}
        dictData={}
        dictData[Key]=dict
        Count_Of_Masks=0
        if Break:
            break
        with open('JSONMappingNameDefault.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
            Count_Of_Masks=len(data)+1
            # with open('StatisticsName.json', 'r+', encoding='utf-8') as g:
            #     Stat = json.load(g)
            #     Stat["Total_Mask_Count"]=Count_Of_Masks
            #     try:
            #         temp=Stat["Masks_Count"][Key]
            #         print(temp)
            #         Stat["Masks_Count"][Key]=temp+1
            #     except:
            #         Stat["Masks_Count"][Key]=1
            #     g.seek(0)
            #     json.dump(Stat,g,indent=4)
            #     g.truncate
            data[Key] =dict # <--- add `id` value.
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f)
            f.truncate()# remove remaining part
        FirstPhaseList.pop(Key)
        d.seek(0)        # <--- should reset file position to the beginning.
        json.dump(FirstPhaseList, d,indent=4)
        d.truncate()# remove re
    


        # print("Mask Generated is ",Mask_1)
    # print("Index\tMaskToken\t\tName Token")
    # i=1
    # for k in FirstPhaseList:
    #     for key,value in k.items():
    #         print(i,"\t\t",key,"\t\t\t\t",value) 
    #     i+=1