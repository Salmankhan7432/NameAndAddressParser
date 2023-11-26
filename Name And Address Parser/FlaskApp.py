# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 18:22:53 2023

@author: skhan2
"""

from flask import Flask, request, render_template, jsonify
import SingleAddressParser_Module as SAP
import Address_Parser__Module as BAP
import json

app = Flask(__name__, template_folder='templates')

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)

