# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 18:22:53 2023

@author: skhan2
"""

from flask import Flask, request, render_template, jsonify
from sqlalchemy import create_engine
import SingleAddressParser_Module as SAP
from ORM import MaskTable, ComponentTable, MappingJSON
from sqlalchemy.orm import sessionmaker
import Address_Parser__Module as BAP
from DB_Operations import DB_Operations as CRUD
import json

app = Flask(__name__, template_folder='templates')
engine = create_engine('sqlite:///KnowledgeBase_TestDummy1.db')
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
    database_url = 'sqlite:///KnowledgeBase_TestDummy1.db'
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
        
@app.route("/delete_record",methods=["POST"])
def delete_component():
    result={}
    if request.method=="POST":
        pass
    return jsonify(result=result)

    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)

