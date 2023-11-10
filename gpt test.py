# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 00:55:45 2023

@author: Ehsan
"""

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

# Define a custom CSS style for the entire app layout
app.layout = html.Div([
    html.Div([
        html.H1("Exhibition Sales Booth", style={
            'fontSize': '2.5rem',
            'fontFamily': 'Shabnam',  # Use your preferred font family
            'textAlign': 'center',
            'color': '#1da1f2',      # Set a primary color
            'marginBottom': '20px',  # Add spacing below the title
        }),

        dcc.Link('New Customer', href='/new-customer', style={
            'textDecoration': 'none',  # Remove underlines from links
            'color': '#1da1f2',        # Use the same primary color
            'marginRight': '20px',     # Add spacing between links
            'fontSize': '1.2rem',      # Adjust link font size
        }),

        dcc.Link('Reports', href='/reports', style={
            'textDecoration': 'none',  # Remove underlines from links
            'color': '#1da1f2',        # Use the same primary color
            'fontSize': '1.2rem',      # Adjust link font size
        }),
    ], style={
        'display': 'flex',            # Display links horizontally
        'justifyContent': 'center',   # Center links horizontally
        'alignItems': 'center',       # Center links vertically
        'backgroundColor': '#f4f4f4',  # Set a background color
        'padding': '20px',            # Add padding to the container
    }),

    html.Div(id='page-content'),
    html.Div(id='page-content-2'),
])

if __name__ == '__main__':
    app.run_server(debug=True)
