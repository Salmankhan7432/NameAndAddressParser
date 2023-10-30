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
# Main Class for the name and address parsing, on individual level
scrollbar = None
submit_button = None
class NameAddressParser:
    
    root = tk.Tk()
    tabControl = ttk.Notebook(root)
    tabControl.pack(expand = 1, fill ="both")

    
    
    #init function for creating th GUI as Tkinter
    def __init__(self, today = date.today()):
        NameAddressParser.root.title("Parser - US Census Bureau "+ str(today))
        NameAddressParser.root.geometry("1280x720")
        NameAddressParser.NameParser()
        NameAddressParser.AddressParser()
        NameAddressParser.NameAddressParser()
        NameAddressParser.ApprovalForm()
        NameAddressParser.root.mainloop()


    #Process for Name Parser, wherein after the click of the button "Choose Two Files" this method is triggered
 
    
    #Process for Address Parser, wherein after the click of the button "Choose Two Files" this method is triggered
     

    
    #Process for Address Parser, wherein after the click of the button "Choose Two Files" this method is triggered
     
    
    # This method is for creating a TAB in the GUI for Name Parser
    def NameParser():
        tab1 = ttk.Frame(NameAddressParser.tabControl)
        NameAddressParser.tabControl.add(tab1, text ='Name Parser')
        ttk.Label(tab1, 
          text ="Please Choose a Pipe Delimitted File").grid(column = 0, 
                               row = 0,
                               padx = 0,
                               pady = 0)  
        def Process_Name_Parser_input():
            msg.showinfo("Choose File","Select Input File")
            #Changed by salman

            df = fd.askopenfilenames( filetypes=[("TXT", ".txt"),("JSON",".json")]) 
            if df:
                Output=NModule.ExtractNames(df[0])
                if Output[0]:
                    msg.showinfo("Success",Output[1])
                else:
                    msg.showerror("Error!", Output[1])
            else: msg.showerror("Alert","Please select input file.")
            return
        
        def Process_Name_Parser():
            msg.showinfo("Choose File","Select Input File")
            #this file is used to give UI for the user to open a Input file
            df = fd.askopenfilenames( filetypes=[("TXT", ".txt")]) 
            if(df):
                msg.showinfo("Choose File","Select Truth File")
                #this file is used to give UI for the user to open a truth file
                truth = fd.askopenfilenames( filetypes=[("TXT", ".txt"),("JSON",".json")]) 
                
                
                
                if truth:
                    Output=NModule.ExtractNames(df[0],TruthSet=truth[0])
                    if Output[0]:
                        msg.showinfo("Success",Output[1])
                    else:
                        msg.showerror("Error!", Output[1])                
                    
                  
                    # except:
                    #     msg.showinfo("Alert!","File Reading Error !")
                else: msg.showerror("Alert!","Truth file is required!")
            else: msg.showerror("Alert","Please select input file.")
            return
                
                
                
                
                
                
                
                
                
                
                
                
               

        Nbutton = ttk.Button(tab1, text ="Choose Two Files (input and test)",width=30, command=Process_Name_Parser).grid(column = 5, 
                             row = 60,
                             padx = 10,
                             pady = 10)
        NbuttonSingle = ttk.Button(tab1, text ="Choose Single File (input)",width=30, command=Process_Name_Parser_input).grid(column = 5, 
                             row = 50,
                             padx = 10,
                             pady = 10)
        
        Or_Label=ttk.Label(tab1,text="Enter Name").grid(column = 4, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        nad=tk.StringVar()
        single_input = ttk.Entry(tab1,width=100,textvariable=nad).grid(column = 5, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10)
        ttk.Label(tab1, 
          text ="OR").grid(column = 5, 
                               row = 15,
                               padx = 0,
                               pady = 0) 

        
        
        def Single_Name(): 
            Convert=NAD_API.ExtractNames(nad.get())
            msg.showinfo("Output",Convert)
        
        ttk.Button(tab1, text ="Submit",width=20, command=Single_Name).grid(column =7, 
                                 row =10)    
                                      
                                              
    # This method is for creating a TAB in the GUI for Address Parser
    def AddressParser():
        tab2 = ttk.Frame(NameAddressParser.tabControl)
        NameAddressParser.tabControl.add(tab2, text ='Address Parser')
        ttk.Label(tab2, 
          text ="Please Choose a Pipe Delimitted File").grid(column = 0, 
                                row = 0,
                                padx = 5,
                                pady = 5)  
                                                             
        def Process_Address_Parser():
            msg.showinfo("Choose File","Select Input File")

            df = fd.askopenfilenames( filetypes=[("TXT", ".txt"),("JSON",".json")]) 
            if df:
                msg.showinfo("Choose File","Select Truth File")
                
                truth = fd.askopenfilenames( filetypes=[("TXT", ".txt")]) #this file is used to give UI for the user to open a file
                if truth:
                    Output=AdM.Address_Parser(df[0],TruthSet=truth[0])
                    if Output[0]:
                        msg.showinfo("Success",Output[1])
                    else:
                        msg.showerror("Error!", Output[1])                
                    
                  
                    # except:
                    #     msg.showinfo("Alert!","File Reading Error !")
                else: msg.showerror("Alert!","Truth file is required!")
            else: msg.showerror("Alert","Please select input file.")
            return
        
        
        def Process_Address_Parser_input():
            msg.showinfo("Choose File","Select Input File")

            df = fd.askopenfilenames( filetypes=[("TXT", ".txt"),("JSON",".json")]) 
            if df:
                Output=AdM.Address_Parser(df[0])
                if Output[0]:
                    msg.showinfo("Success",Output[1])
                else:
                    msg.showerror("Error!", Output[1])
            else: msg.showerror("Alert","Please select input file.")
            return
        
        
        # Nbutton = ttk.Button(tab2, text ="Choose Two Files (input and test)",width=30, command=Process_Address_Parser).grid(column = 5, 
        #                      row = 60,
        #                      padx = 10,
        #                      pady = 10)
        NbuttonSingle = ttk.Button(tab2, text ="Choose Batch File",width=30, command=Process_Address_Parser_input).grid(column = 5, 
                             row = 50,
                             padx = 10,
                             pady = 10)
        
        Or_Label=ttk.Label(tab2,text="Enter Address").grid(column = 4, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        
        nad=tk.StringVar()
        single_input = ttk.Entry(tab2,width=100,textvariable=nad).grid(column = 5, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        ttk.Label(tab2, 
          text ="OR").grid(column = 5, 
                               row = 15,
                               padx = 0,
                               pady = 0) 
        # text = tk.Text(tab2, height=24)
        # text.grid(row=55, column=5, sticky=tk.EW)
        
        # # create a scrollbar widget and set its command to the text widget
        # scrollbar = tk.Scrollbar(tab2, orient='vertical', command=text.yview)
        # scrollbar.grid(column=6, row=55, rowspan=2,  sticky="ns")
        
        # #  communicate back to the scrollbar
        # text['yscrollcommand'] = scrollbar.set
        
        
        # text_result = tk.Text(tab2, height=5,width=30)
        # text_result.grid(row=55, column=7,padx=20,pady=20)
        
        import textwrap
        
        
        def wrap(string, lenght=60):
            return '\n'.join(textwrap.wrap(string, lenght))
        
        
        tree = ttk.Treeview(tab2, column=["Address Component","Address Token","Mask Token","Exception","File"] ,selectmode="extended",show='headings',height=10)
        for item in tree.get_children():
            tree.delete(item)
        tree.column("# 1", width=50, stretch='YES')
        tree.heading("# 1", text="Address Component")
        
        tree.column("# 2", width=200, stretch='YES')
        tree.heading("# 2", text="Address Token")
        
        tree.column("# 3", width=200, stretch='YES')
        tree.heading("# 3", text="Mask Token")
        
        tree.column("# 4", width=50, stretch='YES')
        tree.heading("# 4", text="Exception")
        
        tree.column("# 5", width=200, stretch='YES')
        tree.heading("# 5", text="File Name")
        
        
        def Single_Address():
            
            def submit():
                # Get the checkbox state
                checkbox_state = checkbox_var.get()
                txtMask_1 = tk.StringVar()
                txtFirstPhaseList = tk.StringVar()
                txtInitials = tk.StringVar()
                Mask_1 = txtMask_1.get()
                FirstPhaseList = txtFirstPhaseList.get()
                initials = txtInitials.get()
                # Print the checkbox state
                if checkbox_var.get():
                    # AD_API.Address_Parser()
                    AD_API.throwException(originalInput=nad.get(), initials=initial)
                    msg.showinfo("Exception","Forced Exception is Created!")
                else:
                    msg.showinfo("Exception","Check the box to create an Exception")

            # checkbox_var = tk.IntVar()

            # # Create the checkbox
            # checkbox = ttk.Checkbutton(tab2, text="Forced Exception", variable=checkbox_var)
            # checkbox.grid(row=12, column=5, padx=10, pady=10)

            # # Create the submit button
            # submit_button = ttk.Button(tab2, text="Forced Exception", command=submit)
            # submit_button.grid(row=13, column=5, padx=10, pady=10)
            ### toggle_state = tk.StringVar(value="No")


            ### Create the form elements with custom styling
            ### Forced_Except_Label = ttk.Label(tab2, text="Forced Exception? ", font=("Arial", 12))
            ### Forced_Except_Label.grid(row=5, column=0, sticky=tk.W, pady=5)
            ### toggle_button = ttk.Checkbutton(tab2, onvalue="Yes", offvalue="No", variable=toggle_state, style="Toggle.TCheckbutton")

            ### toggle_button.grid(row=5, column=0,columnspan=2, pady=5)
            ### style.configure("Toggle.TCheckbutton", font=("Arial", 14))
            
            
            s = ttk.Style()
            s.configure('Treeview', rowheight=35, background="black", 
                fieldbackground="black", foreground="white")
            
            
            initial = simpledialog.askstring("Optional", "Your Initials")
           
            Convert=AD_API.Address_Parser(nad.get(),initial,originalInput=nad.get())
            
            Result=Convert[0]
            
            if Result:
                checkbox_var = tk.IntVar()

                # Create the checkbox
                checkbox = ttk.Checkbutton(tab2, text="Forced Exception", variable=checkbox_var)
                checkbox.grid(row=60, column=5, padx=10, pady=10)

                # Create the submit button
                submit_button = ttk.Button(tab2, text="Submit", command=submit)
                submit_button.grid(row=61, column =5 , padx=10, pady=10)
            
            try:  
                
                for item in tree.get_children():
                    tree.delete(item)
                tree.insert('','end',values=(wrap('Mask'),wrap(Convert[1]),"","",""))
                for k, v in Result["Output"].items():  
                    tree.insert('', 'end', values=(wrap(k),wrap(v[1]),wrap(v[0])))
                
            except:
               
                for item in tree.get_children():
                    tree.delete(item)
                tree.insert('','end',values=("","",Convert[1],Convert[2]))


            
            
            
            tree.grid(row=55, column=5, sticky=tk.EW)
            
            
        
        ttk.Button(tab2, text ="Submit",width=30, command=Single_Address).grid(column = 7, 
                                 row = 10)    

        return



    def NameAddressParser():
        
        tab3 = ttk.Frame(NameAddressParser.tabControl)
        NameAddressParser.tabControl.add(tab3, text ='Name and Address Parser')
        ttk.Label(tab3, 
          text ="Please Choose a Pipe Delimitted File").grid(column = 0, 
                               row = 0,
                               padx = 5,
                               pady = 5)  
        def Process_Name_Address_Parser():
            msg.showinfo("Select File","Please select the input file")
            df = fd.askopenfilenames( filetypes=[("TXT", ".txt")]) #this file is used to give UI for the user to open a file
            if df:
                # msg.showinfo("Select File","Please select the input file")
                # truth = fd.askopenfilenames( filetypes=[("TXT", ".txt")])
                # if truth:
                ReturnVal=NaM.NameandAddressParser(df[0])
                jsonData = json.dumps(ReturnVal[0], indent=2)
                with open('OutputNameAddressParsedFile.txt', 'w') as out_file:
                    json.dump(jsonData, out_file, sort_keys = True, indent = 4,ensure_ascii = False)
                    msg.showinfo("Success!","Parsing is Successful, Output File Name 'OutputNameAddressParsedFile' is Generated!")         
                # text = tk.Text(tab3, height=28)
                # text.grid(row=80, column=10, sticky=tk.EW)
                
                # # create a scrollbar widget and set its command to the text widget
                # scrollbar = ttk.Scrollbar(tab3, orient='vertical', command=text.yview)
                # scrollbar.grid(row=80, column=11, sticky=tk.NS)
                
                # #  communicate back to the scrollbar
                # text['yscrollcommand'] = scrollbar.set

                # text.insert('end', jsonData)
                
                
                # text1 = tk.Text(tab3, height=5)
                # text1.grid(row=10, column=30, sticky=tk.NW)
                
                # create a scrollbar widget and set its command to the text widget
                
                #  communicate back to the scrollbar
                String="Percentage of Parsed Name and Address"
                String+="= "+str(round(ReturnVal[1],2))
                String+="\n% of Correctly parsed Addresses= "+str(round(ReturnVal[1],2))
                text.delete("1.0",'end-1c')
                text_result.delete("1.0",'end-1c')
            
                text.insert('end', jsonData)
                text_result.insert('end', String)
            # else: msg.showerror("Warning","Truth file is required.")
            else: msg.showerror("Warning","Input file is not selected.")

            return
        Or_Label=ttk.Label(tab3,text="Enter Name And Address").grid(column = 4, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        Nbutton = ttk.Button(tab3, text ="Choose Two Files",width=30, command= Process_Name_Address_Parser).grid(column = 5, 
                             row = 50,
                             padx = 10,
                             pady = 10)
        nad=tk.StringVar()
        single_input = ttk.Entry(tab3,width=100,textvariable=nad).grid(column = 5, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10)
        ttk.Label(tab3, 
          text ="OR").grid(column = 5, 
                               row = 15,
                               padx = 0,
                               pady = 0) 
        text = tk.Text(tab3, height=24)
        text.grid(row=55, column=5, sticky=tk.EW)
        
        # create a scrollbar widget and set its command to the text widget
        scrollbar = tk.Scrollbar(tab3, orient='vertical', command=text.yview)
        scrollbar.grid(column=6, row=55, rowspan=2,  sticky="ns")
        
        #  communicate back to the scrollbar
        text['yscrollcommand'] = scrollbar.set
        
        
        text_result = tk.Text(tab3, height=5,width=30)
        text_result.grid(row=55, column=7,padx=20,pady=20)
        
        def Single_Name_Address(): 
            Convert=ADN_API.NameandAddressParser(nad.get())
            msg.showinfo("Output",Convert)
        
        ttk.Button(tab3, text ="Submit",width=30, command=Single_Name_Address).grid(column = 7, 
                                 row = 10)
        return
    def ApprovalForm():
        import textwrap
        
        
        def wrap(string, lenght=60):
            return '\n'.join(textwrap.wrap(string, lenght))
        tab4 = ttk.Frame(NameAddressParser.tabControl)
        ttk.Button(tab4, text="Choose an Exception File", width=30, command=lambda: Browse_File([],False)).pack(side="top", padx=0, pady=0)


        label1 = tk.Label(tab4, height=2, width=20, text="Mask Token")
        label1.configure(font=("Arial", 12),relief=tk.RAISED)



        label2 = tk.Label(tab4, height=2, width=20,text="Adress Token")
        label2.configure(font=("Arial", 12), relief=tk.RAISED)


        label3 = tk.Label(tab4, height=2, width=20,text="Address Component")
        label3.configure(font=("Arial", 12), relief=tk.RAISED)

        
        label1.pack_forget()
        label2.pack_forget()
        label3.pack_forget()
        
        
        NameAddressParser.tabControl.add(tab4, text ='Mapping Approval Form')
        form_frame = ttk.Frame(tab4,width=360,height=800)
        form_frame.pack(side=tk.RIGHT,fill=tk.BOTH,padx=10, pady=10)

        
        table_frame = ttk.Frame(tab4)
        table_frame.pack(pady=60)
        table_frame.configure(height=600)
        canvas = tk.Canvas(table_frame,width=580,height=600)
        canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        
        def DateTime():
            # Get the current date and time
            # label = ""
            now = datetime.now()
            current_date = now.strftime("%m-%d-%Y")
            
        
            
            DateTime_label = ttk.Label(tab4, text=f"Date: {current_date}", font=("Arial", 12))
            DateTime_label.pack(side=tk.TOP, padx=10, pady=5)

        
         #S
        def Browse_File(df,Iterate):
            global scrollbar, submit_button #S
            # global df, Stat, file_name, Input_name
            Stat={}
            file_name = ""
            Input_name = ""
            if Iterate==False:
                
                msg.showinfo("Choose File", "Select an Exception File")
                df = fd.askopenfilenames(filetypes=[("JSON", ".json"),("TXT",".txt")])
            else:
                components = form_frame.winfo_children()

                if len(components)!=0:
                    # Iterate through each component and remove it
                    print("fsdafasdfasdf")
                    for component in components:
                        component.destroy()
                    
                    components = canvas.find_all()
    
                    # Remove each component from the canvas
                    for component in components:
                        canvas.delete(component)
            
            if df:
                with open(df[0], "r+", encoding="utf8") as f:
                    Stat = json.load(f)
                RevisedJSON=Stat
                
                Stat=Stat[0]
                # df = df[0]
                # print(len(df))
                # print(len(Stat))
                Mask = list(Stat.keys())[1]
                file_name = os.path.basename(df[0])
                
                
                
                if "INPUT" in Stat:
                    Input_name = Stat["INPUT"]
                    Stat.pop("INPUT")
                else:
                    Input_name = ""
                    msg.showwarning("FileError", "Please Select an Appropriate Exception file.")
                    return
                
                
                label1.pack(side="left", padx=0, pady=10)
                label1.place(x=30,y=42)            
                
                
                label2.pack(side="left", padx=0, pady=10)
                label2.place(x=220,y=42)
                
                
                label3.pack(side="left", padx=0, pady=10)
                label3.place(x=410,y=42)
                
                Exception_file_name_label = ttk.Label(form_frame, text="Exception File Name:", font=("Arial", 12))
                Exception_file_name_label.grid(row=1, column=0, sticky=tk.W, pady=5)
                Exception_file_name_entry = ttk.Entry(form_frame, font=("Arial", 12),width=42)
                Exception_file_name_entry.insert(0,file_name)
                Exception_file_name_entry.configure(state=DISABLED)
                Exception_file_name_entry.grid(row=1, column=1, pady=5)
                Exception_file_name_entry.configure(background="#ffffff", foreground="#000000")
                        
                Input_label = ttk.Label(form_frame, text="Input:", font=("Arial", 12))
                Input_label.grid(row=2, column=0, sticky=tk.W, pady=5)
                
                
                Input_entry = tk.Text(form_frame, height=2, width=20, wrap=tk.WORD)
                Input_entry.insert("1.0",Input_name)
                Input_entry.configure(state=DISABLED,font=("Arial", 12),width=42)
                Input_entry.grid(row=2, column=1, pady=5)
                Input_entry.configure(background="#ffffff", foreground="#000000")
                
                Mask_label = ttk.Label(form_frame, text="Token Pattern:", font=("Arial", 12))
                Mask_label.grid(row=5, column=0, sticky=tk.W, pady=5)
                
                
                region_label = ttk.Label(form_frame, text="Region: *", font=("Arial", 12))
                region_label.grid(row=3, column=0, sticky=tk.W, pady=5)
                regions = ["","US", "Puerto Rico"]
                region_var = tk.StringVar(tab4)
                region_dropdown = ttk.Combobox(form_frame, textvariable=region_var, values=regions, font=("Arial", 12),width=40)
                region_dropdown.grid(row=3, column=1, pady=5)
                region_dropdown.configure(state="readonly")
                
                Type_label = ttk.Label(form_frame, text="Type: *", font=("Arial", 12))
                Type_label.grid(row=4, column=0, sticky=tk.W, pady=5)
                Types=["","Individual Address","PO Box Address","Highway Contract Address","Military Address","Attention line Address","Roural Route Address","Puerto Rico Address","University Address"]
                Type_var = tk.StringVar(tab4)
                Type_dropdown = ttk.Combobox(form_frame, textvariable=Type_var, values=Types, font=("Arial", 12),width=40)
                Type_dropdown.grid(row=4, column=1, pady=5)
                Type_dropdown.configure(state = "readonly")
                
                
                toggle_state = tk.StringVar(value="")
                
                # Create the form elements with custom styling
                Validation_DB_Label = ttk.Label(form_frame, text="Add to DataBase Validation?", font=("Arial", 12))
                Validation_DB_Label.grid(row=6, column=0, sticky=tk.W, pady=5)
                toggle_dropdown = ttk.Combobox(form_frame, textvariable=toggle_state, values=["","Yes", "No"], font=("Arial", 12),width=40, state="readonly")
                toggle_dropdown.grid(row=6, column=1, sticky=tk.W, pady=5)
                
                Approval_label = ttk.Label(form_frame, text="Approved By:", font=("Arial", 12))
                Approval_label.grid(row=8, column=0, sticky=tk.W, pady=5)
                Approval_List = ["", "Committee Member_1", "Committee Member_2", "Committee Member_3"]
                Approval_List_var = tk.StringVar(tab4)
                Approval_List_dropdown = ttk.Combobox(form_frame,textvariable=Approval_List_var,values=Approval_List,font=("Arial", 12),width=40)
                Approval_List_dropdown.grid(row=8, column=1, sticky=tk.W, pady=5)
                Approval_List_dropdown.configure(state="readonly")
                
                
                Exception_file_name_entry = ttk.Entry(form_frame, font=("Arial", 12),width=42)
                Exception_file_name_entry.insert(0,file_name)
                Exception_file_name_entry.configure(state=DISABLED)
                Exception_file_name_entry.grid(row=1, column=1, pady=5)
                Exception_file_name_entry.configure(background="#ffffff", foreground="#000000")
                
                Comment_label = ttk.Label(form_frame, text="Comment", font=("Arial", 12))
                Comment_label.grid(row=7, column=0, sticky=tk.W, pady=5)
           
            
                Comment_entry = tk.Text(form_frame, height=2, width=20, wrap=tk.WORD)
                Comment_entry.configure(font=("Arial", 12),width=42)
                Comment_entry.grid(row=7, column=1, pady=5)
                Comment_entry.configure(background="#ffffff", foreground="#000000")
                
                
                
                Mask_entry = tk.Text(form_frame, height=2, font=("Arial", 12), width=42, wrap=tk.WORD)
                Mask_entry.insert("1.0",Mask)
                Mask_entry.configure(state=DISABLED)
                Mask_entry.grid(row=5, column=1, pady=5)
                Mask_entry.configure(background="#ffffff", foreground="#000000")
                
                
                dropdown_values = {
                  "Not Selected" : "",
                  "USAD_SNO" : "Street Number",
                  "USAD_SPR" : "Street Pre-Directional",
                  "USAD_SNM" : "Street Name",
                  "USAD_SFX" : "Street Suffix",
                  "USAD_SPT" : "Street Post-Directional",
                  "USAD_ANM" : "Secondary Address Name",
                  "USAD_ANO" : "Secondary Address Number",
                  "USAD_CTY" : "City Name",
                  "USAD_STA" : "State Name",
                  "USAD_ZIP" : "Zip Code",
                  "USAD_ZP4" : "Zip 4 Code",
                  "USAD_BNM" : "Box Name",
                  "USAD_BNO" : "Box Number",
                  "USAD_RNM" : "Route Name",
                  "USAD_RNO" : "Route Number",
                  "USAD_ORG" : "Organization Name",
                  "USAD_MDG" : "Military Rd Name",
                  "USAD_MGN" : "Military Rd Number",
                  "USAD_HNM" : "Highway Name",
                  "USAD_HNO" : "Highway Number"}
                
                
                def submit_form():
                    # Retrieve the entered values and process the form data
                    global Stat
                    Exception_file_name = Exception_file_name_entry.get()
                    Input = Input_entry.get("1.0", "end-1c")
                    Input_bytes = Input.encode('utf-8')
                    region = region_var.get()
                    type_value = Type_var.get()
                    approval = Approval_List_var.get()
                    pattern = Mask_entry.get("1.0", "end-1c")
                    Comment = Comment_entry.get("1.0", "end-1c")
                    # component_values = dropdown_var.get()
                    table_data = []
                    today = datetime.now()
                    addValid = toggle_state.get()
                    ID = hashlib.sha1(Input_bytes)
                    Unique_ID = ID.hexdigest()
                    
                    for row in table_rows[0:]:
                        column1 = row[0].cget("text").strip()
                        column2 = row[1].cget("text").strip()
                        column3 = row[2].get()
                        
                        selected_key = next((key for key, val in dropdown_values.items() if val == column3), None)
                        
                        if selected_key is not None:
                            table_data.append((column1, column2, selected_key))
                        if not column3:
                            msg.showerror("Error", "One or More Components are missing!.")
                            return False

                    
                    # Perform validation checks
                    if not Exception_file_name:
                        msg.showerror("Error", "Exception File Name is required.")
                        return False
                    if not Input:
                        msg.showerror("Error", "Input is required.")
                        return False
                    if not region:
                        msg.showerror("Error", "Region is required.")
                        return False
                    if not type_value:
                        msg.showerror("Error", "Type is required.")
                        return False
                    if not addValid:
                        msg.showerror("Error", "Please Select 'Yes/No' for DataBase Validation")
                        return False
                    if not approval:
                        msg.showerror("Error", "Approval Field is required.")
                        return False
                    # if not component_values:
                    #     messagebox.showerror("Error", "All Components are required.")
                    #     return False
                    form_data = {
                        "Unique_ID": Unique_ID,
                        "Exception_file_name": Exception_file_name,
                        "Input": Input,
                        "Region": region,
                        "Type": type_value,
                        "Token Pattern": pattern,
                        "Approved By": (f"{approval} at {today}"),
                        "Comment": Comment,
                        "Table Data": table_data
                    }
                    rejection_data = {
                        "Exception_file_name": Exception_file_name,
                        "Input": Input,
                        "Token Pattern": pattern,
                        "Rejected By": (f"{approval} at {today}"),
                        "Comment": Comment
                    }
                    
                    print("Approved?" , toggle_state.get())
                    if toggle_state.get() == "Yes":
                        
                        with open("Validation_DB.txt", 'r+') as file:
                            try:
                                existing_data = json.load(file)
                            except json.JSONDecodeError:
                                existing_data = []
                        
                            # Append the new data to the existing data list
                            existing_data.append(form_data)
                            
                            # Set the file's current position at the beginning
                            file.seek(0)
                            
                            # Write the updated data back to the file
                            json.dump(existing_data, file, indent=4)
                            file.truncate()
                        
                        # messagebox.showinfo("Demo", "Address is added to Validation DataBase")
                        print(f"Unique_ID: {Unique_ID}")
                        print(f"Exception_file_name: {Exception_file_name}")
                        print(f"Input: {Input}")
                        print(f"Region: {region}")
                        print(f"Type: {type_value}")
                        print(f"Token Pattern: {pattern}")
                        print(f"Comment: {Comment}")
                
                        msg.showinfo("Info", "Address Added to Validation DataBase!")
                        print(f"Approved By: {approval} at {today}")
                        components = form_frame.winfo_children()
                        scrollbar.destroy()
                        for component in components:
                            component.destroy()
                        
                        components=table_frame.winfo_children()
                        
                        for componenet in components:
                            component.destroy()
                        
                        components = canvas.find_all()
                        scrollbar.destroy()
                        # Remove each component from the canvas
                        for component in components:
                            canvas.delete(component)
                        scrollbar.destroy()
                  
                        RevisedJSON.pop(0)
                        
                            
                        with open(df[0], 'w', encoding='utf-8') as f:                
                            json.dump(RevisedJSON, f)
                        if len(RevisedJSON)>0:
                            Browse_File(df,True)
                            scrollbar.destroy()
                        
                    elif toggle_state.get() == "No":
                        msg.showinfo("Info", "Address is not Approved!")#\nPlease Select a New Exception File")
                        # Clear()
                        components = form_frame.winfo_children()
                        scrollbar.destroy()
                        for component in components:
                            component.destroy()
                        
                        components=table_frame.winfo_children()
                        
                        for componenet in components:
                            component.destroy()
                        
                        components = canvas.find_all()
                        scrollbar.destroy()
                        # Remove each component from the canvas
                        for component in components:
                            canvas.delete(component)
                        scrollbar.destroy()
                  
                        RevisedJSON.pop(0)
                        
                            
                        with open(df[0], 'w', encoding='utf-8') as f:                
                            json.dump(RevisedJSON, f)
                        if len(RevisedJSON)>0:
                            Browse_File(df,True)
                            scrollbar.destroy()
                        with open("ADDR_Rejection_DB.txt", 'r+') as r_file:
                            try:
                                previous_data = json.load(r_file)
                            except json.JSONDecodeError:
                                previous_data = []
                        
                            # Append the new data to the existing data list
                            previous_data.append(rejection_data)
                            
                            # Set the file's current position at the beginning
                            r_file.seek(0)
                            
                            # Write the updated data back to the file
                            json.dump(previous_data, r_file, indent=4)
                            r_file.truncate()
                        print(rejection_data)
                            # msg.showinfo("Info", "Address is not Approved")#\nPlease Select a New Exception File")
                    print("Table Data:")
                    
                    for data in table_data:
                        print(data)
                    
                   
                        
                        
                    
                    return form_data, rejection_data
                
                

                def add_table_row(m):
                    global Stat
                    # Add a new row to the table
                    row = []
                    
                    
                    
                    # Create the text widgets for the first two columns with scrollbars

                    def on_select(event):
                        selected_value = dropdown_var.get()
                        selected_key = next((key for key, val in dropdown_values.items() if val == selected_value), None)
                        # if selected_key is not None:
                        #     print(selected_key)
                        # else:
                        #     print("Key not found for selected value:", selected_value)
  # You can perform actions based on the selected key here
                    
                    
                    text1 = tk.Label(table_inner_frame, height=1, width=20, text=m[0])
                    text1.configure(font=("Arial", 12), fg="#000000", background="#ffffff",relief=tk.SUNKEN)
                    text1.grid(row=len(table_rows) + 1, column=0, sticky="nsew", padx=1, pady=0)
                    row.append(text1)
                    
                    text2 = tk.Label(table_inner_frame, height=1, width=20, text=m[1])
                    text2.configure(font=("Arial", 12), fg="#000000", background="#ffffff",relief=tk.SUNKEN)
                    text2.grid(row=len(table_rows) + 1, column=1, sticky="nsew", padx=1, pady=0)
                    row.append(text2)
                    
                    # Create the dropdown for the last column
                    dropdown_var = tk.StringVar(tab4)
                    dropdown_var.set(list(dropdown_values.values())[0])
                    dropdown = ttk.Combobox(table_inner_frame ,textvariable = dropdown_var,values=list(dropdown_values.values()), width=18,height=2, font=("Arial", 12), state="readonly")
                    dropdown.bind("<<ComboboxSelected>>", on_select)
                    # dropdown.pack()
                    dropdown.configure(postcommand=lambda: dropdown.configure(height=dropdown_var),justify="center")
                    dropdown.grid(row=len(table_rows) + 1, column=2, sticky="nsew", padx=2, pady=0)
                    row.append(dropdown)
                    
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
                            set_cell_color(row[0], "#F0F0F0")  # Light gray background
                            set_cell_color(row[1], "#F0F0F0")  # Light gray background
                            set_cell_color(row[2], "#F0F0F0")  # Light gray background
                        else:
                            set_cell_color(row[0], "#FFFFFF")  # White background
                            set_cell_color(row[1], "#FFFFFF")  # White background
                            set_cell_color(row[2], "#FFFFFF")  # White background
                
                table_rows = []

            
            
                                
                # scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=canvas.yview)
                # # scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=canvas.yview)
                # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                # canvas.configure(yscrollcommand=scrollbar.set)
                if scrollbar:
                    scrollbar.destroy()
                    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=canvas.yview)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    canvas.configure(yscrollcommand=scrollbar.set)
                else:
                    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=canvas.yview)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    canvas.configure(yscrollcommand=scrollbar.set)
                
                table_inner_frame = ttk.Frame(canvas)
                table_inner_frame.pack(fill=tk.BOTH, expand=True)
                canvas.create_window((0, 0), window=table_inner_frame, anchor=tk.NW)
                # scrollbar = None
                
                # #S
                # if scrollbar:
                #     # If the scrollbar exists, update its position and command
                #     scrollbar.grid_forget()
                #     scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=canvas.yview)
                #     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                #     canvas.configure(yscrollcommand=scrollbar.set)
                # else:
                #     # If the scrollbar doesn't exist, create it
                #     scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=canvas.yview)
                #     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                #     canvas.configure(yscrollcommand=scrollbar.set)
                # #S
                
                def update_size(e=None):
                    canvas["scrollregion"] = canvas.bbox("all")
                canvas.bind('<Configure>', update_size)
                
                

                
                for key, value in Stat.items():
                    for m in value:
                        m=list(m.items())
                        add_table_row(m[0])
                if submit_button:
                    submit_button.destroy()
                        
                if len(RevisedJSON)>1:
                        
                    submit_button = ttk.Button(form_frame, text="Save and Next", command=submit_form, style="Submit.TButton") #, 
                    submit_button.grid(row=9, column=1, pady=5)
                
                    # Create a custom style for the buttons
                    style = ttk.Style(tab4)
                    style.configure("Submit.TButton", font=("Arial", 12, "bold"), foreground="black", background="#4CAF50")
                else:
                    submit_button = ttk.Button(form_frame, text="Save and Submit", command=submit_form, style="Submit.TButton") #, 
                    submit_button.grid(row=9, column=1, pady=5)
                    
                
                    # Create a custom style for the buttons
                    style = ttk.Style(tab4)
                    style.configure("Submit.TButton", font=("Arial", 12, "bold"), foreground="black", background="#4CAF50")
                
                
                # components = form_frame.winfo_children()
                # scrollbar.destroy()
                # for component in components:
                #     component.destroy()
                
                # components=table_frame.winfo_children()
                
                # for componenet in components:
                #     component.destroy()
                
                # components = canvas.find_all()
                # scrollbar.destroy()
                # # Remove each component from the canvas
                # for component in components:
                #     canvas.delete(component)
                # scrollbar.destroy()
          
                # RevisedJSON.pop(0)    
                
            else:
                msg.showerror("Alert", "Please select an Exception File.")
                
            
            return
        
        
        
        
        
        
        
name=NameAddressParser()