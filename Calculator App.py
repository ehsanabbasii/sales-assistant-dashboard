import dash
from dash import dcc, html, Input, Output, State
import dash_table
import pandas as pd
from dash.exceptions import PreventUpdate
import json
from datetime import datetime

from Classes import Customer

app = dash.Dash(__name__)

# Load product data from an Excel sheet (replace 'products.xlsx' with your file path)
df = pd.read_excel('products.xlsx')

# Define the Shabnam font style with black text color
font_style = {'fontFamily': 'Shabnam', 'textAlign': 'right', 'color': 'black'}

# Define the gray button style
button_style = {'backgroundColor': 'gray', 'color': 'white'}


main_page_layout = html.Div([
        
        html.Div([
            
            dcc.Link('مشتری جدید', href='/new-customer', style={
                'fontFamily': 'Shabnam',
                'textDecoration': 'none',  # Remove underlines from the links
                'color': 'black',           # Set link color
                'display': 'inline',       # Display the link inline
                'padding': '5px 10px',     # Add padding to the links for spacing
                'border': '1px solid black',  # Add a border to the links
                'borderRadius': '5px',      # Add rounded corners to the links
                'marginLeft': '10px',       # Push the link to the right
            }),

            dcc.Link('گزارش ها', href='/reports', style={
                'fontFamily': 'Shabnam',
                'textDecoration': 'none',  # Remove underlines from the links
                'color': 'black',           # Set link color
                'display': 'inline',       # Display the link inline
                'padding': '5px 10px',     # Add padding to the links for spacing
                'border': '1px solid black',  # Add a border to the links
                'borderRadius': '5px',      # Add rounded corners to the links
                'marginLeft': '10px',       # Push the link to the right
            }),
            
            
          

        html.Div([
             
            html.H1("دستیار فروش", style={
                'fontSize': '2.5rem',
                'fontFamily': 'Shabnam',  # Use your preferred font family
                'textAlign': 'center',
                'color': 'black',            # Text color within the header
                'margin': '0 0 0 20px',   # Apply left margin to push the H1 tag to the left
                'padding': '0',            # Remove padding to fit the header
                'display': 'inline',       # Display the H1 tag inline
            }),
            
           
        ], style={
            'flex': '1',                    # Allow the links to take available space
            'display': 'flex',              # Display links in a row
            'justifyContent': 'flex-end',   # Push the links to the right
            'alignItems': 'center',         # Center elements vertically
        }),
     
            
            
            
            
    ], style={
        'display': 'flex',              # Display elements in a row
        'justifyContent': 'space-between',  # Space elements horizontally
        'alignItems': 'center',         # Center elements vertically
        'backgroundColor': '#f4f4f4',  # Light gray background color
        'height': '40px',               # Set the height of the header
        'padding': '5px',               # Add padding to the header
    }),

    html.Div(id='page-content'),
    html.Div(id='page-content-2'),
])


# Update app.layout to include main_page_layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    
    
    main_page_layout
]
    
    , style={
    'background-image': 'url("/assets/background.jpg")',  # Replace with your image file path
    'background-size': 'cover',   # Adjust how the image is displayed
    'background-repeat': 'no-repeat',  # Prevent image repetition
    'background-position': 'center',   # Center the image
    'min-height': '100vh',            # Set a minimum height
    'color': 'white',                 # Text color on top of the image
}
    
                    )






# Define the New Customer page layout and callbacks
new_customer_layout = html.Div([
    html.Div([  # Left Div for Selected Items and Their Prices
        html.H2("کالاهای انتخاب شده", style={'fontSize': '1.5rem', **font_style}),
        dash_table.DataTable(
            id='selected-items-table',
            columns=[
             
                {'name': 'Price', 'id': 'Price'},
                {'name': 'Unit Price', 'id': 'Unit Price'},
                {'name': 'Quantity', 'id': 'Quantity'},
                {'name': 'Product', 'id': 'Product'},
            ],
            data=[],
            style_table={'border': '1px solid #e1e8ed', 'borderRadius': '8px', **font_style},
            style_cell={'textAlign': 'right', **font_style},
            style_header={'backgroundColor': 'gray', 'color': 'black'},
        ),
        html.Button('محاسبه مجموع', id='calculate-button', n_clicks=0, style={**button_style}),
        html.Button('پاک کردن', id='clear-button', n_clicks=0, style={**button_style}),
        html.Div(id='total-cost', style={'fontSize': '1.25rem', 'marginTop': '10px', **font_style}),
    ], style={'padding': '20px', 'width': '45%', 'float': 'left'}),
    
    html.Div([  # Right Div for Add Products and Save Customer Data
        html.Div([  # Upper sub Div for Add Products
            html.H2("کالاها را اضافه کنید", style={'fontSize': '1.5rem', **font_style}),
            dcc.Dropdown(
                id='product-dropdown',
                options=[{'label': product, 'value': product} for product in df['Product']],
                placeholder= "   "+"کالاهارا انتخاب کنید",
                style={'width': '100%,', "marginRight":"10px", **font_style}
            ),
            dcc.Input(
                id='quantity-input',
                type='number',
                value=1,
                min=1,
                placeholder='تعداد را وارد کنید',
                style={'width': '100%', **font_style}
            ),
            html.Button('اضافه به جدول', id='add-button', n_clicks=0, style={**button_style}),
            html.Button('برگرداندن', id='undo-button', n_clicks=0, style={**button_style}),
        ], style={'padding': '20px', **font_style}),
        
        html.Div([  # Lower sub Div for Save Customer Data
            html.H2("اطلاعات مشتری را ذخیره کنید", style={'fontSize': '1.5rem', **font_style}),
            dcc.Input(id='customer-name', type='text', placeholder='نام مشتری را وارد کنید', style={'width': '100%', "marginRight":"10px",**font_style}),
            dcc.Input(id='customer-phone', type='tel', placeholder='شماره مشتری را وارد کنید', style={'width': '100%',"marginRight":"10px",**font_style}),
            dcc.RadioItems(
                id='customer-gender',
                options=[
                    {'label': 'مذکر', 'value': 'male'},
                    {'label': 'مونث', 'value': 'female'},
                    {'label': 'بدون داده', 'value': 'other'},
                ],
                labelStyle={'display': 'block', 'float': 'right', **font_style},  # Display radio items vertically and align to the right
                style={'margin': '10px 0', **font_style},       # Add margin for spacing
            ),
            html.Button('ذخیره اطلاعات مشتری', id='save-button', n_clicks=0, style={**button_style}),
        ], style={'padding': '20px', **font_style}),
    ], style={'width': '45%', 'float': 'right', 'margin-top': '10px'}),
], style={'clear': 'both'})  # Clear the float to prevent layout issues

 


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/new-customer':
        return new_customer_layout
    elif pathname == '/reports':
        return html.H2("Reports Page (Under Construction)", style={'fontSize': '1.5rem'})
    else:
        return []    #html.H2("Welcome to the Main Page", style={'fontSize': '1.5rem'})



@app.callback(
    [Output('selected-items-table', 'data'),
     Output('quantity-input', 'value'),
     Output('customer-name', 'value'),  # Added this line
     Output('customer-phone', 'value')],  # Added this line
    [Input('add-button', 'n_clicks'),
     Input('undo-button', 'n_clicks'),
     Input('clear-button', 'n_clicks')],
    [State('product-dropdown', 'value'),
     State('quantity-input', 'value'),
     State('selected-items-table', 'data'),
     State('customer-name', 'value'),  # Added this line
     State('customer-phone', 'value')]  # Added this line
)
def update_table(n_clicks_add, n_clicks_undo, n_clicks_clear, selected_product, quantity, table_data, customer_name, customer_phone):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'add-button' and selected_product is not None and quantity is not None:
        unit_price = df[df['Product'] == selected_product]['Price'].values[0]
        new_row = {'Product': selected_product, 'Quantity': quantity, 'Unit Price': unit_price, 'Price': unit_price * quantity}
        table_data.append(new_row)
        return table_data, 1, customer_name, customer_phone  # Include customer_name and customer_phone
    elif button_id == 'undo-button' and len(table_data) > 0:
        table_data.pop()
        return table_data, 1, customer_name, customer_phone  # Include customer_name and customer_phone
    elif button_id == 'clear-button':
        return [], 1, '', ''  # Clear customer_name and customer_phone, too
    return table_data, 1, customer_name, customer_phone


# @app.callback(
#     [
#      Output('total-cost', 'children')],
#     [Input('clear-button', 'n_clicks')],
  
# )
# def clear_all(n_clicks, table_data):
#     if n_clicks > 0:
#         return "Total Cost: $0.00"  # Clear table data and reset total cost
#     return "Total Cost: $0.00"


@app.callback(
    Output('total-cost', 'children'),
    [Input('calculate-button', 'n_clicks')],
    [State('selected-items-table', 'data')]
)
def calculate_total(n_clicks, table_data):
    if n_clicks > 0 and table_data:
        total = sum(item['Price'] for item in table_data)
        return f"قیمت نهایی: {total:,.0f}"
    return "قیمت نهایی: 0"

@app.callback(
    Output('page-content-2', 'children'),
    [Input('save-button', 'n_clicks')],
    [State('customer-name', 'value'),
     State('customer-phone', 'value'),
     State('selected-items-table', 'data'),
     State('customer-gender', 'value')]
)
def save_customer_data(n_clicks, name, phone, purchase_data, gender):
    if n_clicks > 0 and name and phone and purchase_data:
        
        current_customer = Customer()
        
        current_customer.name = name
        current_customer.phone = phone
        current_customer.purchase_list = purchase_data
        current_customer.purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_customer.gender = gender
        # Serialize the customer data to JSON and save it to a file
        customer_data = {
            'Name': current_customer.name,
            'Phone': current_customer.phone,
            'PurchaseList': current_customer.purchase_list,
            'PurchaseDate': current_customer.purchase_date,
            "Gender": current_customer.gender
            
        }
        
        try:
            with open('data/customer_data.json', 'r', encoding="utf-8") as file:
                customer_json = json.load(file)
        except FileNotFoundError:
            customer_json = {}  # If the file doesn't exist, start with an empty dictionary
        
        customer_id = current_customer.generate_id_for_customer()  # A unique identifier for the customer
        customer_json[customer_id] = customer_data
        
        # Save the updated data to the JSON file
        if customer_json != None:
            with open('data/customer_data.json', 'w', encoding="utf-8") as file:
                json.dump(customer_json, file, indent=4, ensure_ascii=False)
                    
                    
        






if __name__ == '__main__':
    app.run_server(debug=True)
