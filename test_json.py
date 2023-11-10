# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 19:47:10 2023

@author: Ehsan
"""
import json
from Classes import Customer



current_customer = Customer()

current_customer.name = "A"
current_customer.phone = "B"
current_customer.purchase_list = ["Donkeys 5th foot"]
current_customer.purchase_date = "7:59"
customer_id = current_customer.generate_id_for_customer()




customer_data = {
    'Name': current_customer.name,
    'Phone': current_customer.phone,
    'PurchaseList': ["Donkeys 5th foot"],
    'PurchaseDate': "8-12-06"
}

try:
    with open('data/customer_data.json', 'r') as file:
        customer_json = json.load(file)
except FileNotFoundError:
    customer_json = {}  # If the file doesn't exist, start with an empty dictionary


customer_json

customer_json[customer_id] = customer_data

# # Save the updated data to the JSON file
if customer_json != None:
    with open('data/customer_data.json', 'w') as file:
        json.dump(customer_json, file, indent=4)


