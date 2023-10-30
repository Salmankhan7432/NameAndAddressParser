
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 13:32:17 2022

@author: onais
"""
import re
import collections 
import json 
#Parsing 1st program

def ExtractNames(line):
    fileHandle = open('NamesWordTable.txt', 'r')
    # Strips the newline character
    FinalMappings={}
    Names_Conversion_Dict={"1":"Prefix Title","2":"Given Name", "3":"Surname","4" :"Generational Suffix", "5":"Suffix Title"}    
    FirstPhaseList=[]
    Name=re.sub(',',' , ',line)
    Name=re.sub(' +', ' ',Name)
    Name=re.sub(' +', ' ',Name)
    Name=re.sub('[.]','',Name)
    Name=Name.upper()
    NameList = re.split("\s|\s,\s ", Name)
    NameList = ' '.join(NameList).split()
    print(NameList)
    TrackKey=[]
    Mask=[]
    Combine=""
    LoopCheck=1
    for A in NameList:
        FirstPhaseDict={}
        NResult=False
        if A==",":
            O=0
            Mask.append(Combine)
            Combine=""
            FirstPhaseList.append(",")
            #FirstPhaseList.append("Seperator")
        elif A==" ":
            continue
        elif A!="," and len(A)==1:
            Combine+="I"
            TrackKey.append("I")
            FirstPhaseDict["I"] = A
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
                    break
            if NResult==False:
                Combine+="W"
                TrackKey.append("W")
                FirstPhaseDict["W"] = A
                FirstPhaseList.append(FirstPhaseDict)
        if LoopCheck==len(NameList):
            Mask.append(Combine)
        fileHandle.seek(0)
        LoopCheck+=1
    Mask_1=",".join(Mask)
    FirstPhaseList = [FirstPhaseList[b] for b in range(len(FirstPhaseList)) if FirstPhaseList[b] != ","]
    data={}
    with open('JSONMappingNameDefault.json', 'r+', encoding='utf-8') as f:
        data = json.load(f)
    Found=False
    FoundDict={}
    for tk,tv in data.items():
        if(tk==Mask_1):
            FoundDict[tk]=tv
            Found=True
            break
    FoundExcept=False
    with open('NameExceptionFile.json', 'r+', encoding='utf-8') as g:
        Stat = json.load(g)
        if Mask_1 in Stat.keys():
            FoundExcept=True
    Mappings={}
    print(Found)
    print(Mask_1)
    if Found:
        for K2,V2 in FoundDict[Mask_1].items():
            Temp=""
            for p in V2:
                for K3,V3 in FirstPhaseList[p-1].items():
                   Temp+=" "+V3
                   Temp=Temp.strip()
                   Mappings[K2]=Temp
        FinalMappings["Output"]=Mappings
    elif not FoundExcept:  
        with open('NameExceptionFile.json', 'r+', encoding='utf-8') as g:
            Stat = json.load(g)
            Stat[Mask_1]=FirstPhaseList
            g.seek(0)
            json.dump(Stat,g,indent=4)
            g.truncate   
    print(FinalMappings)
    return FinalMappings


