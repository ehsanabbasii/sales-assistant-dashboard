# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 23:56:43 2023

@author: Ehsan
"""

import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
   
    html.H1("عهی روزگار", style= {"fontFamily": "Shabnam"}),
    html.H1("عهی روزگار",  style= {"fontFamily": "Vazir"}),
])

if __name__ == '__main__':
    app.run_server(debug=True, port = 8094)
