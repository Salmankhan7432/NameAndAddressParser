# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 18:22:53 2023

@author: skhan2
"""

from flask import Flask, request, render_template, jsonify, send_file
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename, safe_join
from tqdm import tqdm
from flask_socketio import SocketIO
import os
from ORM import MaskTable, ComponentTable, MappingJSON
from DB_Operations import DB_Operations as CRUD
import SingleAddressParser_Module as SAP
import Address_Parser__Module as BAP
from flask_cors import CORS
import json
from datetime import datetime

current_time = datetime.now()
app = Flask(__name__, template_folder='templates')
engine = create_engine('sqlite:///KnowledgeBase_Test.db')
Session = sessionmaker(bind=engine)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

CORS(app)



@app.route('/', methods=["GET", "POST"])
def SingleLineAddressParser():
    result = {}
    if request.method == 'POST':
        address = request.form['address']
        convert = SAP.Address_Parser(address, 'Initials', address)
        if convert[4]:
            result = convert[0]
            result['Parsed_By'] = 'Rule Based'
        else:
            result = convert[0]
            result['Parsed_By'] = 'Active Learning'
        print(result)
        return jsonify(result=result)

    return render_template('index.html', result=result)

@app.route("/forceException", methods=["GET", "POST"])
def forceException():
    response = {'result': False}
    global download_except_path  # Make sure to use the global variable
    if request.method == "POST":
        address = request.form["address"]
        convert = SAP.throwException(address, "initials")
        if convert is not None:  # Check if the return value is not None
            response['result'] = True
            download_except_path = convert  # Assign the returned file path
        print(convert)
        
    return jsonify(response=response, download_url="/download_except")

@app.route('/download_except')
def download_except_file():  # Ensure this function name is unique
    global download_except_path
    if download_except_path is None:
        return jsonify({'error': 'No file to download'}), 404
    try:
        return send_file(download_except_path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/Batch_Parser', methods=["POST"])
def BatchParser():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        print(filename)
        file_path = os.path.join('File Uploads', filename)
        file.save(file_path)
        convert = BAP.Address_Parser(file_path, "update_progress")
        print("Convert 0: \n",convert[0], "\n Convert 1: \n", convert[1], "\n Convert 2: \n", convert[2])
        if convert[0]:
            result = convert[1]
            metrics = {'metrics': convert[1]}
            output_file_path = convert[2]
            global download_path
            download_path = output_file_path
            return jsonify(result=result, metrics=metrics, download_url = '/download_output')
        
    return jsonify(result=result, metrics=metrics)

@app.route('/download_output')
def download_file():
    try:
        return send_file(safe_join(app.root_path, download_path), as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/AddressComponents_dropdown', methods=['GET'])
def get_address_components():
    try:
        session = Session()
        components = session.query(ComponentTable.description).all()
        options = [component[0] for component in components]
        print(options)
        session.close()
        return jsonify(options)
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/check-mask-existence', methods=['POST'])
def check_mask_existence():
    session = Session()
    data = request.get_json()
    mask = data.get('mask')
    mask_record = session.query(MaskTable).filter_by(mask=mask).first()
    return jsonify({'exists': mask_record is not None})


@app.route('/MapCreationForm-Data',methods=["GET","POST"])
def MapCreationForm():
    session = Session()
    database_url = 'sqlite:///KnowledgeBase_Test.db'
    engine = create_engine(database_url)
    result={}
    mapdata = request.get_json()
    print("\nReceived Map Data:",mapdata)
    keys = list(mapdata.keys())
    Vdbs = {k: mapdata[k] for k in keys[:10]}
    Vdbs["Approved By"] = Vdbs["Approved By"] + " at " + str(current_time)
    Kbs = {k: mapdata[k] for k in keys[10:]}
    print("\n\nValidation Data Base: ",Vdbs)
    print("\n\nKnowledge Base: ",Kbs)
    if Vdbs["Address Approved?"] == "Yes":
        CRUD.add_data(engine,Kbs)
        print("Approved: Yes")
        with open("Validation_DB.txt", 'r+') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
            existing_data.append(Vdbs)
            file.seek(0)
            json.dump(existing_data, file, indent=4)
            file.truncate()
    else:
        print("Approved: No")
        Vdbs["Rejected By"] = Vdbs["Approved By"]
        del Vdbs["Approved By"]
        print(Vdbs)
        with open("ADDR_Rejection_DB.txt", "r+") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
            existing_data.append(Vdbs)
            file.seek(0)
            json.dump(existing_data, file, indent=4)
            file.truncate()
        
    return jsonify({"status":"success","message":"Form Data Received"})



@app.route('/UserDefinedComponents', methods=["GET","POST"])
def UD_Components():
    result= {}
    database_url = 'sqlite:///KnowledgeBase_Test.db'
    Database_schema = CRUD(database_url)
    if request.method == "POST":
        component_data = Database_schema.get_Component_data()
        for row in component_data:
            component = row.component
            Component_description = row.description
            result[component] = Component_description
        print(result)
        return jsonify(result=result)
    elif request.method == "GET":
        # Handle GET request (if needed)
        return jsonify(message="GET request received for UserDefinedComponents")
    return jsonify(result=result)

@app.route("/add_new_component", methods=["POST"])
def add_new_component():
    result = {}
    try:
        if request.method == "POST":
            new_component = request.form.get('newComponent')  # Get the new component from the form data
            print("New Component: ",new_component)
            new_description = request.form.get('newDescription')  # Get the new description from the form data
            print("New Description: ",new_description)
            session = Session()
    
            try:
                new_ud_component = ComponentTable(component=new_component, description=new_description)
                session.add(new_ud_component)
                session.commit()
    
    
                result['message'] = 'New component added successfully'
                session.close()
    
            except Exception as e:
                session.rollback()
                session.close()
                print("Error occurred:", str(e))
                return jsonify(result={'error': f'Error: {str(e)}'})
        return jsonify(result={'success': True, 'message': 'New component added successfully'})
    except Exception as e:
        return jsonify(result={'error': str(e)})

    return jsonify(result=result)

@app.route('/save_changes', methods=['POST'])
def Edit_Components():
    if request.method == 'POST':
        received_data = request.json['components']  # Get combined old and modified data
        print("Received data on server:", received_data)
        
        session = Session()
        try:
            print("Received data:", received_data)
            # Process and update Component Table using SQLAlchemy ORM
            for component_data in received_data:
                # Identify the old component
                old_component = session.query(ComponentTable).filter_by(
                    component=component_data['oldComponent'],
                    description=component_data['oldDescription']
                ).first()

                if old_component:
                    # Update the old component with new values
                    old_component.component = component_data['newComponent']
                    old_component.description = component_data['newDescription']
                    session.commit()
                old_mappings = session.query(MappingJSON).filter_by(
                    component_index=component_data['oldComponent']
                ).all()

                for old_mapping in old_mappings:
                    old_mapping.component_index = component_data['newComponent']
                    session.commit()
            session.commit()
            session.close()
            
            return jsonify({'message': 'Changes saved successfully'})

        except Exception as e:
            session.rollback()
            session.close()
            print("Error occurred:", str(e))
            return jsonify({'message': f'Error: {str(e)}'})

@app.route("/get_mask_count", methods=["GET"])
def get_mask_count():
    result = {}
    if request.method == "GET":
        component = request.args.get('component')  # Get the component from the query parameters
        session = Session()
        print('Component about to be deleted', component)

        try:
            # Query the count of associated masks
            mask_entries = session.query(MappingJSON.mask_index).filter_by(component_index=component).distinct().all()
            # mask_count = session.query(func.count(MappingJSON.mask_index)).filter_by(component_index=component).scalar()

            total_masks = 0
            for row in mask_entries:
                mask_index = row.mask_index
                masks = session.query(func.count(MaskTable.mask)).filter_by(mask=mask_index).scalar()
                total_masks += masks

            result['maskCount'] = total_masks
            print(result)
            session.close()

        except Exception as e:
            session.close()
            print("Error occurred:", str(e))
            return jsonify(result={'error': f'Error: {str(e)}'})

    return jsonify(result=result)



@app.route("/delete_record", methods=["POST"])
def delete_component():
    # result = {}
    if request.method == "POST":
        component = request.form['component']  # Get the component to be deleted
        print("Component to delete",component)
        session = Session()
        
        try:
            # Delete from MappingJSON and get associated MaskTable entries
            mappings_to_delete = session.query(MappingJSON).filter_by(component_index=component).all()
            mask_entries_to_delete = []
            for mapping in mappings_to_delete:
                mask_entries = session.query(MaskTable).filter_by(mask=mapping.mask_index).all()
                mask_entries_to_delete.extend(mask_entries)
                session.delete(mapping)

            # Delete from ComponentTable
            component_to_delete = session.query(ComponentTable).filter_by(component=component).first()
            if component_to_delete:
                session.delete(component_to_delete)

            # Delete from MaskTable
            for mask_entry in mask_entries_to_delete:
                session.delete(mask_entry)

            session.commit()
            session.close()

            return jsonify(result={'message': f'Record for component {component} deleted successfully'})
        except Exception as e:
            session.rollback()
            session.close()
            print("Error occurred:", str(e))
            return jsonify(result={'message': f'Error: {str(e)}'})


@app.route("/Login", methods=["POST"])
def loginPage():
    if request.method == "POST":
        return
    
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)

