import re
from tqdm import tqdm
import pandas as pd
import json 


class RuleBasedAddressParser:
    def AddressParser(line):

        MASK=[] #In String
        Old_Address=line.strip()
        USAD_Conversion_Dict={"USAD_SNO":"","USAD_SPR":"","USAD_SPR":"","USAD_SNM":"","USAD_SFX":"","USAD_SPT":"","USAD_ANM":"","USAD_ANO":"","USAD_CTY":"","USAD_STA":"","USAD_ZIP":"","USAD_ZP4":"","USAD_BNM":"","USAD_BNO":"","USAD_RNM":"","USAD_RNO":"","USAD_HNM":"","USAD_HNO":""}
        List=USAD_Conversion_Dict.keys()
        FirstPhaseList=[]
        Address=line.strip()
        Address=re.sub(',',' , ',Address.strip())
        Address=re.sub(' +', ' ',Address)
        Address=re.sub('[.]','',Address)
        #Address=re.sub('#','',Address)
        fileHandle = open('USAddressWordTable.txt', 'r',encoding='utf8')

        Address=Address.upper()
        AddressList = re.split("\s|\s,\s ", Address)
        TrackKey=[]
        Mask=[]
        Combine=""
        LoopCheck=1
        for A in AddressList:
            FirstPhaseDict={}
            NResult=False
            try:
                Compare=A[0].isdigit()
            except:
                print()
            if A==",":
                O=0
                Mask.append(Combine)
                Combine=""
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
        USAD_Mapping={"USAD_SNO":[],"USAD_SPR":[],"USAD_SPR":[],"USAD_SNM":[],"USAD_SFX":[],"USAD_SPT":[],"USAD_ANM":[],"USAD_ANO":[],"USAD_CTY":[],"USAD_STA":[],"USAD_ZIP":[],"USAD_ZP4":[],"USAD_BNM":[],"USAD_BNO":[],"USAD_RNM":[],"USAD_RNO":[],"USAD_HNM":[],"USAD_HNO":[]}
        Start=0
        Counts=0
        if "X" not in TrackKey:
            
            for R in USAD_Conversion_Dict:
                
                if R=="USAD_SNO":
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                        if Key=="N":
                            USAD_Mapping["USAD_SNO"].append(j+1)
                            USAD_Conversion_Dict["USAD_SNO"]+=" "+Value.strip()
                            Counts+=1
                        if TrackKey[j+1]!="N":
                            USAD_Mapping["USAD_SNO"]=USAD_Mapping["USAD_SNO"]
                            USAD_Conversion_Dict["USAD_SNO"]=USAD_Conversion_Dict["USAD_SNO"].strip()
                            break
                        
                            
                elif R=="USAD_SPR":
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[Counts]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                        if Key=="D":
                            USAD_Mapping["USAD_SPR"].append(j+1)
                            USAD_Conversion_Dict["USAD_SPR"]+=" "+Value.strip()
                            Counts+=1
                        if TrackKey[j+1]!="D":
                            USAD_Mapping["USAD_SPR"]=USAD_Mapping["USAD_SPR"]
                            USAD_Conversion_Dict["USAD_SPR"]=USAD_Conversion_Dict["USAD_SPR"].strip()
                            break
    
                elif R=="USAD_SNM":
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                        if Key=="W" or Key=="N":
                            USAD_Conversion_Dict["USAD_SNM"]+=" "+Value.strip()
                            Counts+=1
                        if Key=="W":
                            if TrackKey[j+1]!="W":
                                USAD_Mapping["USAD_SNM"].append(j+1)
                                USAD_Conversion_Dict["USAD_SNM"]=USAD_Conversion_Dict["USAD_SNM"].strip()
                                break
                        else :
                            if TrackKey[j+1]!="N":
                                USAD_Mapping["USAD_SNM"]=USAD_Mapping["USAD_SNM"]
    
                                USAD_Conversion_Dict["USAD_SNM"]=USAD_Conversion_Dict["USAD_SNM"].strip()
                                break
                elif R=="USAD_SFX":
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                        if Key=="F":   
                            USAD_Mapping["USAD_SFX"].append(j+1)
                            USAD_Conversion_Dict["USAD_SFX"]+=" "+Value.strip()
                            Counts+=1
                        if TrackKey[j+1]!="F":
                            USAD_Mapping["USAD_SFX"]=USAD_Mapping["USAD_SFX"]
                            USAD_Conversion_Dict["USAD_SFX"]=USAD_Conversion_Dict["USAD_SFX"].strip()
                            break
                elif R=="USAD_SPT":
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                        if Key=="D":
                            USAD_Mapping["USAD_SPT"].append(j+1)
                            USAD_Conversion_Dict["USAD_SPT"]+=" "+Value.strip()
                            Counts+=1
                        if TrackKey[j+1]!="D":
                            USAD_Mapping["USAD_SPT"]=USAD_Mapping["USAD_SPT"]
                            USAD_Conversion_Dict["USAD_SPT"]=USAD_Conversion_Dict["USAD_SPT"].strip()
                            break
                elif R=="USAD_ANM":
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                        if Key=="S":
                            USAD_Mapping["USAD_ANM"].append(j+1)
                            USAD_Conversion_Dict["USAD_ANM"]+=" "+Value.strip()
                            Counts+=1
                        try:
                            if TrackKey[j+1]!="N":
                                USAD_Mapping["USAD_ANM"]=USAD_Mapping["USAD_ANM"]
                                USAD_Conversion_Dict["USAD_ANM"]=USAD_Conversion_Dict["USAD_ANM"].strip()
                            break
                        except:
                            USAD_Conversion_Dict["USAD_ANM"]=USAD_Conversion_Dict["USAD_ANM"].strip()
                            break
                elif R=="USAD_ANO":
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                        if Key=="N":
                            USAD_Mapping["USAD_ANO"].append(j+1)
                            USAD_Conversion_Dict["USAD_ANO"]+=" "+Value.strip()
                            Counts+=1
                        try:
                            if TrackKey[j+1]!="N":
                                USAD_Mapping["USAD_ANO"]=USAD_Mapping["USAD_ANO"]
    
                                USAD_Conversion_Dict["USAD_ANO"]=USAD_Conversion_Dict["USAD_ANO"].strip()
                            break
                        except:
                            USAD_Conversion_Dict["USAD_ANO"]=USAD_Conversion_Dict["USAD_ANO"].strip()
                            break
                elif R=="USAD_CTY":
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                        if Key=="W":
                            USAD_Mapping["USAD_CTY"].append(j+1)
                            USAD_Conversion_Dict["USAD_CTY"]+=" "+Value.strip()
                            Counts+=1
                        if TrackKey[j+1]!="W":
                            USAD_Mapping["USAD_CTY"]=USAD_Mapping["USAD_CTY"]
                            USAD_Conversion_Dict["USAD_CTY"]=USAD_Conversion_Dict["USAD_CTY"].strip()
                            break
                elif R=="USAD_STA":
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                        if Key=="T":
                            USAD_Mapping["USAD_STA"].append(j+1)
                            USAD_Conversion_Dict["USAD_STA"]+=" "+Value.strip()
                            Counts+=1
                        try:
                                
                            if TrackKey[j+1]!="T":
                                USAD_Mapping["USAD_STA"]=USAD_Mapping["USAD_STA"]
        
                                USAD_Conversion_Dict["USAD_STA"]=USAD_Conversion_Dict["USAD_STA"].strip()
                                break
                        except:
                            USAD_Mapping["USAD_STA"]=USAD_Mapping["USAD_STA"]
                            USAD_Conversion_Dict["USAD_STA"]=USAD_Conversion_Dict["USAD_STA"].strip()
    
                elif R=="USAD_ZIP":
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="N":
                            USAD_Mapping["USAD_ZIP"].append(j+1)
                            USAD_Conversion_Dict["USAD_ZIP"]+=" "+Value.strip()
                            Counts+=1
                        try:
                            if TrackKey[j+1]=="N":
                                USAD_Mapping["USAD_ZIP"]=USAD_Mapping["USAD_ZIP"]
                                USAD_Conversion_Dict["USAD_ZIP"]=USAD_Conversion_Dict["USAD_ZIP"].strip()
                                break
                        except:
                                USAD_Mapping["USAD_ZIP"]=USAD_Mapping["USAD_ZIP"]
                                USAD_Conversion_Dict["USAD_ZIP"]=USAD_Conversion_Dict["USAD_ZIP"].strip()
        elif "X" in TrackKey:
            list_of_values=[]
            for d in FirstPhaseList:
                for v in d.values():
                    list_of_values.append(v)
            for R in USAD_Conversion_Dict:
                if R=="X" and "HC" not in list_of_values:
                    
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="X":
                            USAD_Mapping["USAD_BNM"].append(j+1)
                            USAD_Conversion_Dict["USAD_BNM"]+=Value.strip()+" "
                            Counts+=1
            
                
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="N":
                            USAD_Mapping["USAD_BNO"].append(j+1)
                            USAD_Conversion_Dict["USAD_BNO"]+=Value.strip()+" "
                            Counts+=1
                        try:          
                            if TrackKey[j+1]!="N":
                                USAD_Mapping["USAD_BNO"]=USAD_Mapping["USAD_BNO"]
        
                                USAD_Conversion_Dict["USAD_BNO"]=USAD_Conversion_Dict["USAD_BNO"].strip()
                                break
                        except:
                            USAD_Mapping["USAD_BNO"]=USAD_Mapping["USAD_BNO"]
                            USAD_Conversion_Dict["USAD_BNO"]=USAD_Conversion_Dict["USAD_BNO"].strip()

                    
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="W":
                            USAD_Mapping["USAD_CTY"].append(j+1)
                            USAD_Conversion_Dict["USAD_CTY"]+=Value.strip()+" "
                            Counts+=1
                        try:          
                            if TrackKey[j+1]!="W":
                                USAD_Mapping["USAD_CTY"]=USAD_Mapping["USAD_CTY"]
        
                                USAD_Conversion_Dict["USAD_CTY"]=USAD_Conversion_Dict["USAD_CTY"].strip()
                                break
                        except:
                            USAD_Mapping["USAD_CTY"]=USAD_Mapping["USAD_CTY"]
                            USAD_Conversion_Dict["USAD_CTY"]=USAD_Conversion_Dict["USAD_CTY"].strip()    
                
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="T":
                            USAD_Mapping["USAD_STA"].append(j+1)
                            USAD_Conversion_Dict["USAD_STA"]+=Value.strip()+" "
                            Counts+=1
                        
                        try:          
                            if TrackKey[j+1]!="T":
                                USAD_Mapping["USAD_STA"]=USAD_Mapping["USAD_STA"]
        
                                USAD_Conversion_Dict["USAD_STA"]=USAD_Conversion_Dict["USAD_STA"].strip()
                                break
                        except:
                            USAD_Mapping["USAD_STA"]=USAD_Mapping["USAD_STA"]
                            USAD_Conversion_Dict["USAD_STA"]=USAD_Conversion_Dict["USAD_STA"].strip()
                
                
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="N":
                            USAD_Mapping["USAD_ZIP"].append(j+1)
                            USAD_Conversion_Dict["USAD_ZIP"]+=Value.strip()+" "
                            Counts+=1
        
                elif "HC" in list_of_values:
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="F":
                            USAD_Mapping["USAD_HNM"].append(j+1)
                            USAD_Conversion_Dict["USAD_HNM"]+=Value.strip()+" "
                            Counts+=1
                
                
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="N":
                            USAD_Mapping["USAD_HNO"].append(j+1)
                            USAD_Conversion_Dict["USAD_HNO"]+=Value.strip()+" "
                            Counts+=1
                        try:          
                            if TrackKey[j+1]!="T":
                                USAD_Mapping["USAD_HNO"]=USAD_Mapping["USAD_HNO"]
        
                                USAD_Conversion_Dict["USAD_HNO"]=USAD_Conversion_Dict["USAD_HNO"].strip()
                                break
                        except:
                            USAD_Mapping["USAD_HNO"]=USAD_Mapping["USAD_HNO"]
                            USAD_Conversion_Dict["USAD_HNO"]=USAD_Conversion_Dict["USAD_HNO"].strip()

                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="X":
                            USAD_Mapping["USAD_BNM"].append(j+1)
                            USAD_Conversion_Dict["USAD_BNM"]+=Value.strip()+" "
                            Counts+=1
                
                
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="N":
                            USAD_Mapping["USAD_BNO"].append(j+1)
                            USAD_Conversion_Dict["USAD_BNO"]+=Value.strip()+" "
                            Counts+=1
                        try:          
                            if TrackKey[j+1]!="T":
                                USAD_Mapping["USAD_BNO"]=USAD_Mapping["USAD_BNO"]
        
                                USAD_Conversion_Dict["USAD_BNO"]=USAD_Conversion_Dict["USAD_BNO"].strip()
                                break
                        except:
                            USAD_Mapping["USAD_BNO"]=USAD_Mapping["USAD_BNO"]
                            USAD_Conversion_Dict["USAD_BNO"]=USAD_Conversion_Dict["USAD_BNO"].strip()
                    
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="W":
                            USAD_Mapping["USAD_CTY"].append(j+1)
                            USAD_Conversion_Dict["USAD_CTY"]+=Value.strip()+" "
                            Counts+=1
                        try:          
                            if TrackKey[j+1]!="W":
                                USAD_Mapping["USAD_CTY"]=USAD_Mapping["USAD_CTY"]
        
                                USAD_Conversion_Dict["USAD_CTY"]=USAD_Conversion_Dict["USAD_CTY"].strip()
                                break
                        except:
                            USAD_Mapping["USAD_CTY"]=USAD_Mapping["USAD_CTY"]
                            USAD_Conversion_Dict["USAD_CTY"]=USAD_Conversion_Dict["USAD_CTY"].strip()    
                
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="T":
                            USAD_Mapping["USAD_STA"].append(j+1)
                            USAD_Conversion_Dict["USAD_STA"]+=Value.strip()+" "
                            Counts+=1
                        
                        try:          
                            if TrackKey[j+1]!="T":
                                USAD_Mapping["USAD_STA"]=USAD_Mapping["USAD_STA"]
        
                                USAD_Conversion_Dict["USAD_STA"]=USAD_Conversion_Dict["USAD_STA"].strip()
                                break
                        except:
                            USAD_Mapping["USAD_STA"]=USAD_Mapping["USAD_STA"]
                            USAD_Conversion_Dict["USAD_STA"]=USAD_Conversion_Dict["USAD_STA"].strip()
                
                
                    for j in range(Counts,len(TrackKey)):
                        Dictionary=FirstPhaseList[j]
                        Key=""
                        Value=""
                        for K,V in Dictionary.items():
                            Key=K
                            Value=V
                            
                        if Key=="N":
                            USAD_Mapping["USAD_ZIP"].append(j+1)
                            USAD_Conversion_Dict["USAD_ZIP"]+=Value.strip()+" "
                            Counts+=1
                
                # else:
                #     for j in range(Counts,len(TrackKey)):
                #         Dictionary=FirstPhaseList[j]
                #         Key=""
                #         Value=""
                #         for K,V in Dictionary.items():
                #             Key=K
                #             Value=V
                            
                #         if Key=="R":
                #             USAD_Mapping["USAD_RNM"].append(j+1)
                #             USAD_Conversion_Dict["USAD_RNM"]+=Value.strip()+" "
                #             Counts+=1
                
                
                #     for j in range(Counts,len(TrackKey)):
                #         Dictionary=FirstPhaseList[j]
                #         Key=""
                #         Value=""
                #         for K,V in Dictionary.items():
                #             Key=K
                #             Value=V
                            
                #         if Key=="N":
                #             USAD_Mapping["USAD_RNO"].append(j+1)
                #             USAD_Conversion_Dict["USAD_RNO"]+=Value.strip()+" "
                #             Counts+=1
                #         try:          
                #             if TrackKey[j+1]!="N":
                #                 USAD_Mapping["USAD_RNO"]=USAD_Mapping["USAD_RNO"]
        
                #                 USAD_Conversion_Dict["USAD_RNO"]=USAD_Conversion_Dict["USAD_RNO"].strip()
                #                 break
                #         except:
                #             USAD_Mapping["USAD_RNO"]=USAD_Mapping["USAD_RNO"]
                #             USAD_Conversion_Dict["USAD_RNO"]=USAD_Conversion_Dict["USAD_RNO"].strip()

                #     for j in range(Counts,len(TrackKey)):
                #         Dictionary=FirstPhaseList[j]
                #         Key=""
                #         Value=""
                #         for K,V in Dictionary.items():
                #             Key=K
                #             Value=V
                            
                #         if Key=="X":
                #             USAD_Mapping["USAD_BNM"].append(j+1)
                #             USAD_Conversion_Dict["USAD_BNM"]+=Value.strip()+" "
                #             Counts+=1
                
                
                #     for j in range(Counts,len(TrackKey)):
                #         Dictionary=FirstPhaseList[j]
                #         Key=""
                #         Value=""
                #         for K,V in Dictionary.items():
                #             Key=K
                #             Value=V
                            
                #         if Key=="N":
                #             USAD_Mapping["USAD_BNO"].append(j+1)
                #             USAD_Conversion_Dict["USAD_BNO"]+=Value.strip()+" "
                #             Counts+=1
                #         try:          
                #             if TrackKey[j+1]!="T":
                #                 USAD_Mapping["USAD_BNO"]=USAD_Mapping["USAD_BNO"]
        
                #                 USAD_Conversion_Dict["USAD_BNO"]=USAD_Conversion_Dict["USAD_BNO"].strip()
                #                 break
                #         except:
                #             USAD_Mapping["USAD_BNO"]=USAD_Mapping["USAD_BNO"]
                #             USAD_Conversion_Dict["USAD_BNO"]=USAD_Conversion_Dict["USAD_BNO"].strip()
                    
                #     for j in range(Counts,len(TrackKey)):
                #         Dictionary=FirstPhaseList[j]
                #         Key=""
                #         Value=""
                #         for K,V in Dictionary.items():
                #             Key=K
                #             Value=V
                            
                #         if Key=="W":
                #             USAD_Mapping["USAD_CTY"].append(j+1)
                #             USAD_Conversion_Dict["USAD_CTY"]+=Value.strip()+" "
                #             Counts+=1
                #         try:          
                #             if TrackKey[j+1]!="W":
                #                 USAD_Mapping["USAD_CTY"]=USAD_Mapping["USAD_CTY"]
        
                #                 USAD_Conversion_Dict["USAD_CTY"]=USAD_Conversion_Dict["USAD_CTY"].strip()
                #                 break
                #         except:
                #             USAD_Mapping["USAD_CTY"]=USAD_Mapping["USAD_CTY"]
                #             USAD_Conversion_Dict["USAD_CTY"]=USAD_Conversion_Dict["USAD_CTY"].strip()    
                
                #     for j in range(Counts,len(TrackKey)):
                #         Dictionary=FirstPhaseList[j]
                #         Key=""
                #         Value=""
                #         for K,V in Dictionary.items():
                #             Key=K
                #             Value=V
                            
                #         if Key=="T":
                #             USAD_Mapping["USAD_STA"].append(j+1)
                #             USAD_Conversion_Dict["USAD_STA"]+=Value.strip()+" "
                #             Counts+=1
                        
                #         try:          
                #             if TrackKey[j+1]!="T":
                #                 USAD_Mapping["USAD_STA"]=USAD_Mapping["USAD_STA"]
        
                #                 USAD_Conversion_Dict["USAD_STA"]=USAD_Conversion_Dict["USAD_STA"].strip()
                #                 break
                #         except:
                #             USAD_Mapping["USAD_STA"]=USAD_Mapping["USAD_STA"]
                #             USAD_Conversion_Dict["USAD_STA"]=USAD_Conversion_Dict["USAD_STA"].strip()
                
                
                #     for j in range(Counts,len(TrackKey)):
                #         Dictionary=FirstPhaseList[j]
                #         Key=""
                #         Value=""
                #         for K,V in Dictionary.items():
                #             Key=K
                #             Value=V
                            
                #         if Key=="N":
                #             USAD_Mapping["USAD_ZIP"].append(j+1)
                #             USAD_Conversion_Dict["USAD_ZIP"]+=Value.strip()+" "
                #             Counts+=1
                     
        dic = {key:value for key,value in USAD_Conversion_Dict.items() if value != ''}
        return dic
        
parser = RuleBasedAddressParser.AddressParser("HC 68 BOX 23 Chicago, IL 44432")
print(parser)