# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 11:22:18 2023

@author: Onais, Salman, Kashif
"""
import tkinter as tk
from tkinter import messagebox
from datetime import date
from tkinter import ttk
import threading
import tkinter as tk					
from tkinter import ttk,simpledialog,DISABLED
from datetime import date
import tkinter.filedialog as fd
import tkinter.messagebox as msg
import pandas as pd
from functools import partial
import json
import NameParser___Module as NModule
import NameAddressParser__Module as NaM
import Address_Parser__Module as AdM
import SingleNameParser_Module as NAD_API
import SingleAddressParser_Module as AD_API
import SingleNameAddressParser_Module as ADN_API
from datetime import datetime
import os
import subprocess
import hashlib
import Address_parser_mixc_methods as mx
import Address_parser_approval_form as approvalform

class NAP_GUIBuilder(tk.Tk):
    def __init__(self):
        # Set the geometry of the window
        
        super().__init__()
        self.title("Parser - "+ str(date.today()))
        
        self.NAP_GUIBuilder_CreateTabs()
        screen_width = self.winfo_screenwidth()
        
        screen_height = self.winfo_screenheight()

        self.geometry(f"{screen_width}x{screen_height}")
        self.state('zoomed')
        self.tree = None
    def NAP_GUIBuilder_CreateTabs(self):
        
        #Create Tabs Depending on the init for root (tk.Tk)
        
        self.tabControl = ttk.Notebook(self)
        self.tabControl.pack(expand = 1, fill ="both")
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text ='SingleLine Address Parser')
        
        self.tab5 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab5, text ='Batch Parser')
        
        
        
        
        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab4, text ='Map Creation Form')
        
        
        # Calling Different Methods with respect to the tab
        self.NAP_GUIBuilder_AddressParser()
        self.NAP_GUIBuilder_AddressParserFile()
        self.NAP_GUIBuilder_MappingApprovalForm()
        
        

    def NAP_GUIBuilder_AddressParser(self):
        
        
        
        Instance = mx.Address_parser_misc()
        
         
        
        
        ttk.Label(self.tab2, text ="Please Choose a Pipe Delimitted File"). grid(column = 0, 
                               row = 0,
                               padx = 5,
                               pady = 5)  
        
        
        
        ttk.Label(self.tab2,text="Enter Address").grid(column = 4, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        
        single_input = tk.Text(self.tab2,width=80,height=3,wrap=tk.WORD)
        single_input.grid(column = 5, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        
    
        s=ttk.Style()
        s.theme_use("clam")
        s.configure('Treeview',rowheight=30)

        s.configure("TProgressbar", foreground='red', background='green')
        
        tree = ttk.Treeview(self.tab2, column=["Mask Token","Address Token","Address Component","Component Description","Parsed By"] ,show='headings',height=14)
        
    
        for item in tree.get_children():
            tree.delete(item)
        tree.column("# 1", width=60, stretch='YES')
        tree.heading("# 1", text="Mask Token")
        
        tree.column("# 2", width=100, stretch='YES')
        tree.heading("# 2", text="Address Token")
        
        tree.column("# 3", width=80, stretch='YES')
        tree.heading("# 3", text="Address Component")
        
        tree.column("# 4", width=100, stretch='YES')
        tree.heading("# 4", text="Component Description")
        
        tree.column("# 5", width=50, stretch='YES')
        tree.heading("# 5", text="Parsed By")
        ttk.Button(self.tab2, text ="Submit", command=lambda:Instance.Single_Address(single_input, self.tab2,tree),width=30).grid(column = 7, 
                                 row = 10)
        
        
    def NAP_GUIBuilder_MappingApprovalForm(self):
       
        import textwrap
        
        
        def wrap(string, lenght=60):
            return '\n'.join(textwrap.wrap(string, lenght))
        
        
        approval_form_instance=approvalform.submission_form()
        
        ttk.Button(self.tab4, text="Choose an Exception File", width=30, command=lambda: approval_form_instance.Browse_File([],False,form_frame,canvas,table_frame,label1,label2,label3,self.tab4)).pack(side="top", padx=0, pady=0)


        label1 = tk.Label(self.tab4, height=2, width=20, text="Mask Token")
        label1.configure(font=("Arial", 12),relief=tk.RAISED)



        label2 = tk.Label(self.tab4, height=2, width=20,text="Adress Token")
        label2.configure(font=("Arial", 12), relief=tk.RAISED)


        label3 = tk.Label(self.tab4, height=2, width=20,text="Address Component")
        label3.configure(font=("Arial", 12), relief=tk.RAISED)

        
        label1.pack_forget()
        label2.pack_forget()
        label3.pack_forget()
        
        
        form_frame = ttk.Frame(self.tab4,width=50,height=600)
        form_frame.pack(side=tk.RIGHT,fill=tk.BOTH,padx=0, pady=30)
        form_frame.place(x=650,y=40)
        
        table_frame = ttk.Frame(self.tab4)

        table_frame.pack(side=tk.LEFT,pady=0,padx=5)
        table_frame.place(x=30,y=90)
        #table_frame.grid(column=1,row=1)
        table_frame.configure(height=550)
        
        canvas = tk.Canvas(table_frame,width=580,height=420)
        canvas.grid(column=3,row=5)
        
        
        

    
    def NAP_GUIBuilder_AddressParserFile(self):
        
        Instance = mx.Address_parser_misc()
        s=ttk.Style()
        s.theme_use("clam")

        s.configure("TProgressbar", foreground='red', background='green')
        def Threads(Progress):
            thread1=threading.Thread(target=lambda:Instance.Process_Address_Parser_Single_input(Progress))
            
            thread1.start()
        ttk.Label(self.tab5,text="Please Choose A Pipe Delimitted File").grid(column = 0, 
                                 row = 0,
                                 padx = 10,
                                 pady = 10)
        Progress = ttk.Progressbar(self.tab5, orient=tk.HORIZONTAL,length=300,mode='determinate',style="TProgressbar")
        Progress.grid( column=5,row=11,padx=10,pady=10)
        
        ttk.Button(self.tab5, text ="Choose Batch File",width=30, command=lambda:Threads(Progress)).grid(column = 5, 
                             row = 10,
                             padx = 10,
                             pady = 10)
        
        return
    
if __name__ == "__main__":
    Run= NAP_GUIBuilder()
    Run.mainloop()


