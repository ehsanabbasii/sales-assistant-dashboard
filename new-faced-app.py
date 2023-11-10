# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 00:12:54 2023

@author: Ehsan
"""

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)


        
    
app.layout = html.Div([
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

        html.Div([
            dcc.Link('مشتری جدید', href='/new-customer', style={
                'fontFamily': 'Shabnam',
                'textDecoration': 'none',  # Remove underlines from the links
                'color': 'blue',           # Set link color
                'display': 'inline',       # Display the link inline
                'padding': '5px 10px',     # Add padding to the links for spacing
                'border': '1px solid blue',  # Add a border to the links
                'borderRadius': '5px',      # Add rounded corners to the links
                'marginLeft': '10px',       # Push the link to the right
            }),

            dcc.Link('گزارش ها', href='/reports', style={
                'fontFamily': 'Shabnam',
                'textDecoration': 'none',  # Remove underlines from the links
                'color': 'blue',           # Set link color
                'display': 'inline',       # Display the link inline
                'padding': '5px 10px',     # Add padding to the links for spacing
                'border': '1px solid blue',  # Add a border to the links
                'borderRadius': '5px',      # Add rounded corners to the links
                'marginLeft': '10px',       # Push the link to the right
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

        

if __name__ == '__main__':
    app.run_server(debug=True)

