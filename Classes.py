# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 18:40:12 2023

@author: Ehsan
"""
import uuid
import base64

class Customer:
    def __init__(self):
        self.name = ""
        self.phone = ""
        self.purchase_list = []
        self.purchase_date = ""
        self.gender = ""
        self.id = ''
        
    def generate_id_for_customer(self):
        # Generate a UUID
        customer_uuid = uuid.uuid4()
        # Convert the UUID to bytes
        customer_bytes = customer_uuid.bytes
        # Encode the bytes into a base64 string (which will be shorter)
        short_id = base64.urlsafe_b64encode(customer_bytes).decode()[:10]
        #print(short_id)
        self.id = short_id
        return self.id
