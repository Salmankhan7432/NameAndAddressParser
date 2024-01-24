# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 18:22:53 2023

@author: skhan2
"""

from flask import Flask, request, render_template, jsonify
from sqlalchemy import create_engine, func
import SingleAddressParser_Module as SAP
from ORM import MaskTable, ComponentTable, MappingJSON
from sqlalchemy.orm import sessionmaker
import Address_Parser__Module as BAP
from DB_Operations import DB_Operations as CRUD
import json

app = Flask(__name__, template_folder='templates')
engine = create_engine('sqlite:///KnowledgeBase_TestDummy5.db')
Session = sessionmaker(bind=engine)


@app.route('/', methods=["GET", "POST"])
def index():
    result = {}
    if request.method == 'POST':
        address = request.form['address']
        convert = SAP.Address_Parser(address, 'Initials', address)
        result = convert[0]
        print(result)
        return jsonify(result=result)

    return render_template('index.html', result=result)

@app.route('/UserDefinedComponents', methods=["GET","POST"])
def UD_Components():
    result= {}
    database_url = 'sqlite:///KnowledgeBase_TestDummy5.db'
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
                # Create a new UserDefinedComponents instance and add it to the database
                new_ud_component = ComponentTable(component=new_component, description=new_description)
                session.add(new_ud_component)
                session.commit()
    
                # You may also want to update the MappingJSON and MaskTable accordingly
    
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
            mask_count = session.query(func.count(MappingJSON.mask_index)).filter_by(component_index=component).scalar()

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
    result = {}
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

    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)

