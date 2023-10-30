# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 13:32:17 2022

@author: onais
"""
import re
import collections 
import json 
from sklearn.metrics import multilabel_confusion_matrix,confusion_matrix,classification_report
import pandas as pd
#Parsing 1st program

def ExtractNames(File,TruthSet=""):
    FinalMappings={}
    Truth_Result={}
    Result={}
    Detailed_Report=""
    Name_4CAF50=open(File,"r")
    Lines = Name_4CAF50.readlines()
    fileHandle = open('NamesWordTable.txt', 'r')
    # Strips the newline character
    Observation=0
    Total=0
    USAD_Conversion_Dict= {"Prefix Title":1,"Given Name":2, "Surname":3,"Generational Suffix":4, "Suffix Title":5}    
    USAD_CONVERSION_={"1":"Prefix Title","2":"Given Name", "3":"Surname","4" :"Generational Suffix", "5":"Suffix Title"}
    
    
    for line in Lines:
        Total+=1
        Names_Conversion_Dict={"1":"Prefix Title","2":"Given Name", "3":"Surname","4" :"Generational Suffix", "5":"Suffix Title"}    
        Nm=line.split("|")
        line=Nm[1]
        ID=Nm[0]
        FirstPhaseList=[]
        Name=re.sub(',',' , ',line)
        Name=re.sub(' +', ' ',Name)
        Name=re.sub(' +', ' ',Name)
        Name=re.sub('[.]','',Name)
        #Name=re.sub('#','',Name)    
        Name=Name.upper()
        NameList = re.split("\s|\s,\s ", Name)
        NameList = ' '.join(NameList).split()
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
        if Found:
            Truth_Result[ID]=FoundDict[Mask_1]
            Observation+=1
            for K2,V2 in FoundDict[Mask_1].items():
                Temp=""
                for p in V2:
                    for K3,V3 in FirstPhaseList[p-1].items():
                       Temp+=" "+V3
                       Temp=Temp.strip()
                       Mappings[K2]=Temp
            FinalMappings[ID]=Mappings
            
            try:
                Truth_Result[ID]=Mappings
                Result[ID]=Mappings
                
            except:
                Result[ID]=Mappings
                Truth_Result[ID]=Mappings
                
            
            
            
        elif not FoundExcept:  
            with open('NameExceptionFile.json', 'r+', encoding='utf-8') as g:
                Stat = json.load(g)
                Stat[Mask_1]=FirstPhaseList
                g.seek(0)
                json.dump(Stat,g,indent=4)
                g.truncate
    Result={}  
    Count_of_Correct=0
    Total_Count=0
    y_test=[]
    y_predict=[]
    if TruthSet!="":
        with open(TruthSet, 'r+', encoding='utf-8') as g:
            Stat = json.load(g)
            Count_of_Correct=0
            Total_Count=0
            ID=1
            for k in Stat["annotations"]:
                res=""
                for m in k[1].items():
    
                    for j in m[1]:
                        predict=False
                        y_test.append(USAD_Conversion_Dict[j[2]])
                        for k1,v1 in Truth_Result[str(ID)].items():
                            
                            if re.sub('\W+','', v1.strip().upper()) == re.sub('\W+','', k[0][j[0]:j[1]].upper().strip()):
                                y_predict.append(USAD_Conversion_Dict[k1])
                                
                                predict=True
                                break
                        if not predict:
                            #y_predict.append(0)
                            y_test.pop()
                ID+=1
    
        import numpy as np
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        Confusion =  multilabel_confusion_matrix(y_test, y_predict)
        df=classification_report(y_test,y_predict,output_dict=True)
        df_report = pd.DataFrame(df).transpose()
        df_report.reset_index(inplace=True)
        df_report=df_report.replace({"index": USAD_CONVERSION_})
        df_report.to_csv("Metrics.csv")
        
        RTruth=0
        try:
            RTruth=(Count_of_Correct/Total_Count*100)
        except:
            print()
        Detailed_Report+="Output From Active Learning\n\n"
        ActiveLResult = json.dumps(Truth_Result, indent = 4,ensure_ascii=False) 
        Detailed_Report+=str(ActiveLResult)
        Detailed_Report+="\n\nNumber of Exceptions Thrown: -\t"+str(Total-Observation)+"\n"
        Detailed_Report+="Number of Parsed Name: -\t"+str(Observation)+"\n"
        Detailed_Report+="Percentage of Parsed Result: -\t"+str((Observation/Total)*100)+"\n"
        Detailed_Report+="\n\n Evaluation Metrics\n\n"
    
        Detailed_Report+=str(df_report)
        f=open("Detailed_Report_Names.txt","w",encoding="utf8")
    
        f.write(Detailed_Report)
        f.close()
        return (True,"Detailed_Name_Report.txt Generated")
    else:
        Detailed_Report+="Output From Active Learning\n\n"
        ActiveLResult = json.dumps(Truth_Result, indent = 4,ensure_ascii=False) 
        Detailed_Report+=str(ActiveLResult)
        Detailed_Report+="\n\nNumber of Exceptions Thrown: -\t"+str(Total-Observation)+"\n"
        Detailed_Report+="Number of Parsed Name: -\t"+str(Observation)+"\n"
        
        f=open("Detailed_Report_Names.txt","w",encoding="utf8")
    
        f.write(Detailed_Report)
        f.close()
        return (True,"Detailed_Name_Report.txt Generated for single input")
        

    
    
    
