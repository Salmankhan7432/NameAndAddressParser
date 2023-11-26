# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 01:15:44 2023

@author: Onais, Salman, Kashif
"""

import tkinter as tk
from tkinter import messagebox
from datetime import date
from tkinter import ttk

import tkinter as tk
from tkinter import ttk, simpledialog, DISABLED
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
import submission_form_parser as submissionform



class submission_form:
    def Browse_File(self, df, Iterate, form_frame, canvas, table_frame, label1, label2, label3, tab4):
        global scrollbar, submit_button  # S
        submitform = submissionform.submission_form()

        # global df, Stat, file_name, Input_name
        Stat = {}
        file_name = ""
        Input_name = ""
        ID = ""
        if Iterate == False:
            popup = msg.askokcancel("Choose File", "Select an Exception File")
            if popup:
                df = fd.askopenfilenames(
                    filetypes=[("JSON", ".json"), ("TXT", ".txt")],initialdir = "Exceptions")
                components = form_frame.winfo_children()    
    
                if len(components) != 0:
                    # Iterate through each component and remove it
                    for component in components:
                        component.destroy()
    
                    components = canvas.find_all()
    
                    # Remove each component from the canvas
                    for component in components:
                        canvas.delete(component)
                try:
    
                    scrollbar.destroy()
                except:
                    True
        else:
            components = form_frame.winfo_children()

            if len(components) != 0:
                # Iterate through each component and remove it
                for component in components:
                    component.destroy()

                components = canvas.find_all()

                # Remove each component from the canvas
                for component in components:
                    canvas.delete(component)
            try:

                scrollbar.destroy()
            except:
                True

        if df:
            with open(df[0], "r+", encoding="utf8") as f:
                Stat = json.load(f)
            RevisedJSON = Stat
            try:
                Stat = Stat[0]
                Mask = list(Stat.keys())[2]
            except:
                msg.showwarning(
                    "FileError", "File is Empty or missing format\n\nPlease Select an Appropriate Exception File.")
            
            
            file_name = os.path.basename(df[0])

            if "Record ID" in Stat:
                ID = Stat["Record ID"]
                Stat.pop("Record ID")
                
            else:
                ID = ""
                
                return

            if "INPUT" in Stat:
                Input_name = Stat["INPUT"]
                Input_name = Input_name
                Stat.pop("INPUT")
            else:
                Input_name = ""
                
                return

            def on_window_resize(event):

                # Adjust the label position to stay on the left when the window is resized

                label1.pack(side=tk.LEFT)
                label2.pack(side=tk.LEFT)
                label3.pack(side=tk.LEFT)

            tab4.bind("<Configure>", on_window_resize)
            label1.pack(side="left", padx=0, pady=10)
            label1.place(x=30, y=42)

            label2.pack(side="left", padx=0, pady=10)
            label2.place(x=220, y=42)

            label3.pack(side="left", padx=0, pady=10)
            label3.place(x=410, y=42)

            Exception_file_name_label = ttk.Label(
                form_frame, text="Exception File Name:", font=("Arial", 12))
            Exception_file_name_label.grid(
                row=1, column=0, sticky=tk.W, pady=5)
            Exception_file_name_entry = ttk.Entry(
                form_frame, font=("Arial", 12), width=42)
            Exception_file_name_entry.insert(0, file_name)
            Exception_file_name_entry.configure(state=DISABLED)
            Exception_file_name_entry.grid(row=1, column=1, pady=5)
            Exception_file_name_entry.configure(
                background="#ffffff", foreground="#000000")

            ID_label = ttk.Label(
                form_frame, text="Record ID:", font=("Arial", 12))
            ID_label.grid(row=2, column=0, sticky=tk.W, pady=5)

            ID_entry = tk.Text(form_frame, height=2, width=20)
            ID_entry.insert("1.0", ID)
            ID_entry.configure(state=DISABLED, font=("Arial", 12), width=42)
            ID_entry.grid(row=2, column=1, pady=5)
            ID_entry.configure(background="#ffffff", foreground="#000000")

            Input_label = ttk.Label(
                form_frame, text="Input:", font=("Arial", 12))
            Input_label.grid(row=3, column=0, sticky=tk.W, pady=5)

            Input_entry = tk.Text(form_frame, height=2, width=20, wrap=tk.WORD)
            Input_entry.insert("1.0", Input_name)
            Input_entry.configure(state=DISABLED, font=("Arial", 12), width=42)
            Input_entry.grid(row=3, column=1, pady=5)
            Input_entry.configure(background="#ffffff", foreground="#000000")

            Mask_label = ttk.Label(
                form_frame, text="Token Pattern:", font=("Arial", 12))
            Mask_label.grid(row=6, column=0, sticky=tk.W, pady=5)

            Mask_entry = tk.Text(form_frame, height=2, font=(
                "Arial", 12), width=42, wrap=tk.WORD)
            Mask_entry.insert("1.0", Mask)
            Mask_entry.configure(state=DISABLED)
            Mask_entry.grid(row=6, column=1, pady=5)
            Mask_entry.configure(background="#ffffff", foreground="#000000")

            region_label = ttk.Label(
                form_frame, text="Region: *", font=("Arial", 12))
            region_label.grid(row=4, column=0, sticky=tk.W, pady=5)
            regions = ["", "US", "Puerto Rico"]
            region_var = tk.StringVar(tab4)
            region_dropdown = ttk.Combobox(
                form_frame, textvariable=region_var, values=regions, font=("Arial", 12), width=40)
            region_dropdown.grid(row=4, column=1, pady=5)
            region_dropdown.configure(state="readonly")

            Type_label = ttk.Label(
                form_frame, text="Type: *", font=("Arial", 12))
            Type_label.grid(row=5, column=0, sticky=tk.W, pady=5)
            Types = ["", "Street Address", "PO Box Address", "Highway Contract Address", "Military Address",
                     "Attention line Address", "Roural Route Address", "Puerto Rico Address", "University Address"]
            Type_var = tk.StringVar(tab4)
            Type_dropdown = ttk.Combobox(
                form_frame, textvariable=Type_var, values=Types, font=("Arial", 12), width=40)
            Type_dropdown.grid(row=5, column=1, pady=5)
            Type_dropdown.configure(state="readonly")

            toggle_state = tk.StringVar(value="")

            # Create the form elements with custom styling
            Validation_DB_Label = ttk.Label(
                form_frame, text="Add to V_DB and KB?", font=("Arial", 12))
            Validation_DB_Label.grid(row=7, column=0, sticky=tk.W, pady=5)
            toggle_dropdown = ttk.Combobox(form_frame, textvariable=toggle_state, values=[
                                           "", "Yes", "No"], font=("Arial", 12), width=40, state="readonly")
            toggle_dropdown.grid(row=7, column=1, sticky=tk.W, pady=5)

            Approval_label = ttk.Label(
                form_frame, text="Approved By:", font=("Arial", 12))
            Approval_label.grid(row=9, column=0, sticky=tk.W, pady=5)
            Approval_List = ["", "Committee Member_1",
                             "Committee Member_2", "Committee Member_3"]
            Approval_List_var = tk.StringVar(tab4)
            Approval_List_dropdown = ttk.Combobox(
                form_frame, textvariable=Approval_List_var, values=Approval_List, font=("Arial", 12), width=40)
            Approval_List_dropdown.grid(row=9, column=1, sticky=tk.W, pady=5)
            Approval_List_dropdown.configure(state="readonly")

            Comment_label = ttk.Label(
                form_frame, text="Comment", font=("Arial", 12))
            Comment_label.grid(row=8, column=0, sticky=tk.W, pady=5)

            Comment_entry = tk.Text(
                form_frame, height=2, width=20, wrap=tk.WORD)
            Comment_entry.configure(font=("Arial", 12), width=42)
            Comment_entry.grid(row=8, column=1, pady=5)
            Comment_entry.configure(background="#ffffff", foreground="#000000")

            dropdown_values = {
                
                "USAD_SNO": "Street Number",
                "USAD_SPR": "Street Pre-Directional",
                "USAD_SNM": "Street Name",
                "USAD_SFX": "Street Suffix",
                "USAD_SPT": "Street Post-Directional",
                "USAD_ANM": "Secondary Address Name",
                "USAD_ANO": "Secondary Address Number",
                "USAD_CTY": "City Name",
                "USAD_STA": "State Name",
                "USAD_ZIP": "Zip Code",
                "USAD_ZP4": "Zip 4 Code",
                "USAD_BNM": "Box Name",
                "USAD_BNO": "Box Number",
                "USAD_RNM": "Route Name",
                "USAD_RNO": "Route Number",
                "USAD_ORG": "Organization Name",
                "USAD_MDG": "Military Rd Name",
                "USAD_MGN": "Military Rd Number",
                "USAD_HNM": "Highway Name",
                "USAD_HNO": "Highway Number", "USAD_NA":"Not Selected"}
            desired_order = [
                "USAD_SNO",
                "USAD_SPR",
                "USAD_SNM",
                "USAD_SFX",
                "USAD_SPT",
                "USAD_ANM",
                "USAD_ANO",
                "USAD_CTY",
                "USAD_STA",
                "USAD_ZIP",
                "USAD_ZP4",
                "USAD_BNM",
                "USAD_BNO",
                "USAD_RNM",
                "USAD_RNO",
                "USAD_ORG",
                "USAD_MDG",
                "USAD_MGN",
                "USAD_HNM",
                "USAD_HNO",
                "USAD_NA",
                ]
            
            # sorted_items = sorted(dropdown_values.items())

            # # Create a new dictionary from the sorted list
            # sorted_dict = dict(sorted_items)
            
            # # Print the sorted dictionary
            # print(sorted_dict)

            def add_table_row(m):
                global Stat
                # Add a new row to the table
                row = []
                
                # Create the text widgets for the first two columns with scrollbars
                # print(m)
                def on_select(event):
                    selected_value = dropdown_var.get()
                    selected_key = next(
                        (key for key, val in dropdown_values.items() if val == selected_value), None)
                    # if selected_key is not None:
                    #     print(selected_key)
                    # else:
                    #     print("Key not found for selected value:", selected_value)
                    # You can perform actions based on the selected key here

                text1 = tk.Label(table_inner_frame, height=1,
                                 width=20, text=m[2])
                text1.configure(font=("Arial", 12), fg="#000000",
                                background="#ffffff", relief=tk.SUNKEN)
                text1.grid(row=len(table_rows) + 1, column=0,
                           sticky="nsew", padx=1, pady=0)
                row.append(text1)

                text2 = tk.Label(table_inner_frame, height=1,
                                 width=20, text=m[0])
                text2.configure(font=("Arial", 12), fg="#000000",
                                background="#ffffff", relief=tk.SUNKEN)
                text2.grid(row=len(table_rows) + 1, column=1,
                           sticky="nsew", padx=1, pady=0)
                row.append(text2)
                #-----------------------------------------------------------------------------
                
                # Create a Combobox and populate it with values in the desired order
                dropdown_var = tk.StringVar(tab4)
                dropdown_var.set(dropdown_values[desired_order[0]])  # Set the default value
                
                selected_item = dropdown_values[m[1]]
                
                list_of_val = [dropdown_values[key] for key in desired_order]
                list_of_val.insert(0, selected_item)
                
                dropdown = ttk.Combobox(
                    table_inner_frame, textvariable=dropdown_var, values=list_of_val, width=18, height=2, font=("Arial", 12), state="readonly")
                dropdown.set(selected_item)
                
                dropdown.configure(postcommand=lambda: dropdown.configure(
                    height=dropdown_var), justify="center")
                dropdown.grid(row=len(table_rows) + 1, column=2, sticky="nsew", padx=2, pady=0)
                row.append(dropdown)
                
                #-----------------------------------------------------------------------------
                
                # # Create the dropdown for the last column
                # dropdown_var = tk.StringVar(tab4)
                # dropdown_var.set(list(dropdown_values.values())[0])
                
                # selected_item=dropdown_values[m[1]]
                # list_of_val=list(dropdown_values.values())
                
                # list_of_val.insert(0,selected_item)
                # list_of_val=list(set(list_of_val))
                # # print(selected_item)
                
                # dropdown = ttk.Combobox(table_inner_frame,textvariable=dropdown_var, values=list_of_val, width=18, height=2, font=("Arial", 12), state="readonly")
                # #dropdown.bind("<<ComboboxSelected>>", on_select)
                # dropdown.set(selected_item)
                # # dropdown.pack()
                # dropdown.configure(postcommand=lambda: dropdown.configure(
                #     height=dropdown_var), justify="center")
                # dropdown.grid(row=len(table_rows) + 1, column=2,
                #               sticky="nsew", padx=2, pady=0)
                # row.append(dropdown)

                # Update the row-span for the labels in the previous rows
                for r in range(len(table_rows)):
                    table_rows[r][0].grid(row=r + 1, column=0, sticky="e")
                    table_rows[r][1].grid(row=r + 1, column=1, sticky="e")
                    table_rows[r][2].grid(row=r + 1, column=2, sticky="e")

                # Append the new row to the table rows list
                table_rows.append(row)

                set_row_colors()  # Set alternate row colors

                # Update the canvas scroll region

            def set_cell_color(cell, color):
                cell.configure(background=color)

            def set_row_colors():
                global Stat
                for i, row in enumerate(table_rows):
                    if i % 2 == 0:
                        # Light gray background
                        set_cell_color(row[0], "#F0F0F0")
                        # Light gray background
                        set_cell_color(row[1], "#F0F0F0")
                        # Light gray background
                        set_cell_color(row[2], "#F0F0F0")
                    else:
                        set_cell_color(row[0], "#FFFFFF")  # White background
                        set_cell_color(row[1], "#FFFFFF")  # White background
                        set_cell_color(row[2], "#FFFFFF")  # White background

            table_rows = []

           
           # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            table_inner_frame = ttk.Frame(canvas)
            table_inner_frame.pack(fill=tk.BOTH, expand=True)
            canvas_config = canvas.create_window(
                (0, 0), window=table_inner_frame, anchor=tk.NW)
            scrollbar = ttk.Scrollbar(
                table_frame, orient=tk.VERTICAL, command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            table_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
            scrollbar.grid(column=5,row=5,sticky="ns")
            #canvas.update_idletasks()
           # canvas.configure(scrollregion=canvas.bbox("all"))
            def on_window_resize(event):
                canvas.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox("all"))

            tab4.bind("<Configure>", on_window_resize)
           
            
            for key, value in Stat.items():
                for m in value:
                    
                
                    add_table_row(m)
                    

            if len(RevisedJSON) > 1:

                submit_button = ttk.Button(form_frame, text="Submit and Next", command=lambda: submitform.submit_form(Exception_file_name_entry, Input_entry, region_var, Type_var, Approval_List_var,
                                                                                                                    Mask_entry, Comment_entry, toggle_state, table_rows, dropdown_values,
                                                                                                                    form_frame, scrollbar, canvas, df, RevisedJSON, table_frame,
                                                                                                                    label1, label2, label3, tab4, table_inner_frame), style="Submit.TButton")
                submit_button.grid(row=10, column=1, pady=5)

                # Create a custom style for the buttons
                style = ttk.Style(tab4)
                style.configure("Submit.TButton", font=(
                    "Arial", 12, "bold"), foreground="black", background="#4CAF50")
                
                # clear_button = ttk.Button(form_frame, text="Save and Exit", command=lambda: submitform.clear_form(form_frame, canvas,table_frame,scrollbar, RevisedJSON), style="Submit.TButton")  # ,
                # clear_button.grid(row=12, column=1, pady=5)

                # # Create a custom style for the buttons
                # style = ttk.Style(tab4)
                # style.configure("Submit.TButton", font=(
                #     "Arial", 12, "bold"), foreground="black", background="#4CAF50")
            else:
                submit_button = ttk.Button(form_frame, text="Submit", command=lambda: submitform.submit_form(Exception_file_name_entry, Input_entry, region_var, Type_var, Approval_List_var,
                                                                                                                      Mask_entry, Comment_entry, toggle_state, table_rows, dropdown_values,
                                                                                                                      form_frame, scrollbar, canvas, df, RevisedJSON, table_frame,
                                                                                                                      label1, label2, label3, tab4, table_inner_frame), style="Submit.TButton")  # ,
                submit_button.grid(row=10, column=1, pady=5)

                # Create a custom style for the buttons
                style = ttk.Style(tab4)
                style.configure("Submit.TButton", font=(
                    "Arial", 12, "bold"), foreground="black", background="#4CAF50")

            clear_button = ttk.Button(form_frame, text="Save and Exit", command=lambda: submitform.clear_form(form_frame, canvas,table_frame,df,scrollbar, RevisedJSON), style="Clear.TButton")  # ,
            clear_button.grid(row=12, column=1, pady=5)

            # Create a custom style for the buttons
            style = ttk.Style(tab4)
            style.configure("Clear.TButton", font=(
                "Arial", 12, "bold"), foreground="black", background="#FF0000")