# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 14:20:12 2023

@author: Ehsan
"""

import dash
from dash import dcc, html, Input, Output, State
import dash_table
import pandas as pd
from dash.exceptions import PreventUpdate
import json
from datetime import datetime

app = dash.Dash(__name__)

# Load product data from an Excel sheet (replace 'products.xlsx' with your file path)
df = pd.read_excel('products.xlsx')

# Define Twitter-like styles
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1("Exhibition Sales Booth", style={'fontSize': '2.5rem'}),
    dcc.Link('New Customer', href='/new-customer', style={'marginRight': '10px'}),
    dcc.Link('Reports', href='/reports', style={'marginRight': '10px'}),
    html.Div(id='page-content'),
])

# Define the New Customer page layout and callbacks
new_customer_layout = html.Div([
    html.H2("Add Products", style={'fontSize': '1.5rem'}),
    dcc.Input(id='customer-name', type='text', placeholder='Enter customer name', style={'width': '100%'}),
    dcc.Input(id='customer-phone', type='tel', placeholder='Enter customer phone number', style={'width': '100%'}),
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': product, 'value': product} for product in df['Product']],
        placeholder="Select products",
        style={'width': '100%'}
    ),
    dcc.Input(
        id='quantity-input',
        type='number',
        value=1,
        min=1,
        placeholder='Enter quantity',
        style={'width': '100%'}
    ),
    html.Button('Add to Table', id='add-button', n_clicks=0, style={'backgroundColor': '#1da1f2', 'color': 'white'}),
    html.Button('Undo', id='undo-button', n_clicks=0, style={'backgroundColor': '#1da1f2', 'color': 'white'}),
    html.Button('Clear All', id='clear-button', n_clicks=0, style={'backgroundColor': '#1da1f2', 'color': 'white'}),
    html.Button('Save Customer Data', id='save-button', n_clicks=0, style={'backgroundColor': '#1da1f2', 'color': 'white'}),
    html.Div([
        html.H2("Selected Items and Their Prices", style={'fontSize': '1.5rem'}),
        dash_table.DataTable(
            id='selected-items-table',
            columns=[
                {'name': 'Product', 'id': 'Product'},
                {'name': 'Quantity', 'id': 'Quantity'},
                {'name': 'Unit Price', 'id': 'Unit Price'},
                {'name': 'Price', 'id': 'Price'},
            ],
            data=[],
            style_table={'border': '1px solid #e1e8ed', 'borderRadius': '8px'},
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': '#1da1f2', 'color': 'white'},
        ),
        html.Button('Calculate Total', id='calculate-button', n_clicks=0, style={'backgroundColor': '#1da1f2', 'color': 'white'}),
        html.Div(id='total-cost', style={'fontSize': '1.25rem', 'marginTop': '10px'}),
    ], style={'padding': '20px'}),
])

class Customer:
    def __init__(self):
        self.name = ""
        self.phone = ""
        self.purchase_list = []
        self.purchase_date = ""

current_customer = Customer()

@app.callback(
    [Output('selected-items-table', 'data'),
     Output('quantity-input', 'value')],
    [Input('add-button', 'n_clicks'),
     Input('undo-button', 'n_clicks'),
     Input('clear-button', 'n_clicks')],
    [State('product-dropdown', 'value'),
     State('quantity-input', 'value'),
     State('selected-items-table', 'data')]
)
def update_table(n_clicks_add, n_clicks_undo, n_clicks_clear, selected_product, quantity, table_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'add-button' and selected_product is not None and quantity is not None:
        unit_price = df[df['Product'] == selected_product]['Price'].values[0]
        new_row = {'Product': selected_product, 'Quantity': quantity, 'Unit Price': unit_price, 'Price': unit_price * quantity}
        table_data.append(new_row)
        return table_data, 1
    elif button_id == 'undo-button' and len(table_data) > 0:
        table_data.pop()
        return table_data, 1
    elif button_id == 'clear-button':
        return [], 1
    return table_data, 1

@app.callback(
    Output('total-cost', 'children'),
    [Input('calculate-button', 'n_clicks')],
    [State('selected-items-table', 'data')]
)
def calculate_total(n_clicks, table_data):
    if n_clicks > 0 and table_data:
        total = sum(item['Price'] for item in table_data)
        return f"Total Cost: ${total:,.0f}"
    return "Total Cost: $0.00"

@app.callback(
    Output('page-content', 'children'),
    [Input('save-button', 'n_clicks')],
    [State('customer-name', 'value'),
     State('customer-phone', 'value'),
     State('selected-items-table', 'data')]
)
def save_customer_data(n_clicks, name, phone, purchase_data):
    if n_clicks > 0 and name and phone and purchase_data:
        current_customer.name = name
        current_customer.phone = phone
        current_customer.purchase_list = purchase_data
        current_customer.purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Serialize the customer data to JSON and save it to a file
        customer_data = {
            'Name': current_customer.name,
            'Phone': current_customer.phone,
            'PurchaseList': current_customer.purchase_list,
            'PurchaseDate': current_customer.purchase_date
        }
        with open(f'{current_customer.name}_customer_data.json', 'w') as json_file:
            json.dump(customer_data, json_file)
            
        # Clear the customer's data after saving
        current_customer.__init__()

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/new-customer':
        return new_customer_layout
    elif pathname == '/reports':
        return html.H2("Reports Page (Under Construction)", style={'fontSize': '1.5rem'})
    else:
        return html.H2("Welcome to the Main Page", style={'fontSize': '1.5rem'})

if __name__ == '__main__':
    app.run_server(debug=True)
