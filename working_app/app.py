# Created by: Pieter Barkema
# Date: February, 2022
# Description:
#    Users can access this online app to process their neuroimaging date
#    with normative modelling. It should return visualizations 
#    and results to users accessing from all over the world, 
#    It is hosted as a website from a remote gunicorn server.
    

from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
from flask import Flask
#import os, sys
import io, base64

# Make sure that this is necessary
#sys.path.insert(1, "/home/preclineu/piebar/Documents/PCN_directory/")
from apply_normative_models_app import apply_normative_model
# Create a flask server
server = Flask(__name__)
# Create  Dash app
app = Dash(server=server)

# -----------------------------------------------------------------
# The entire contents of the app.
app.layout = html.Div([
    html.Div(children=[
    
        # -----------------------------------------------------------------
        # The standard data input parameters
        html.Br(),
        html.Label('Email address for results: '),
        dcc.Input(value='', type='text'),
    
        html.Br(),
                html.Br(),
        html.Label('Data type'),
        dcc.Dropdown(options = ['Brain surface area', 'Average Thickness'], id='data-type'),
        
        html.Br(),
        html.Label('Normative Model'),
        dcc.Dropdown( options = ['please select data type first'], value = 'please select data type first', id='model-selection'),

        html.Br(),
        html.Label('Select data format'),
        dcc.Dropdown(['.csv', 'NIFTI', '[other formats]'], '.csv'),

        html.Br(),
        html.Hr(),
        html.Label('Upload test data'),
        html.Hr(),
        dcc.Upload([
            'Drag and Drop or ',
            html.A('Select a File')
        ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
        }
        , id= 'Upl_1'
        ),             
        # List the uploaded data file(s)
        html.Ul(id="list-data-file"),
        
        html.Hr(),
        dcc.Upload(html.A('Upload adaptation data')),
        html.Hr(),
        dcc.Upload([
            'Drag and Drop or ',
            html.A('Select a File')
        ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
        }
        , id= 'Upl_2'
        ),
        # List the uploaded covariate file(s)
        html.Ul(id="list-cov-file"),         
        # -----------------------------------------------------------------
        # The data submission and results retrieval section
        html.Div(
            style={'width':'10%', 'height':'100%','float':'right','position':'relative', 'top':'4%'},
            children=[
                html.Button("Submit", id="btn_csv"),
                html.Plaintext(id="submitted"),
                html.Br(),
                # Download your predictions in .csv format!
                html.Button("Download", id="results_onclick", disabled=True),
                # Store the results files so they can be downloaded on click, not instantly
                dcc.Store(id="csv_store_session", storage_type="session"),
                dcc.Download(id="download-dataframe-csv")
            ]
        ),

        # -----------------------------------------------------------------
        # Check lists with all options to control results output
        html.Div(
            style={'width':'10%', 'height':'100%','float':'right'},
            children=[
                dcc.Checklist(className ='checkbox_1',
                        options=[
                            {'label': 'raw data', 'value': 'I1ST2'},
                            {'label': 'raw data', 'value': 'I2ST2'},
                            {'label': 'raw data', 'value': 'I3ST2'},
                            {'label': 'raw data', 'value': 'I4ST2'}
                                ],
                        value=['I1ST2'],
                        labelStyle = {'display': 'block'}
                                )
            ]
        ),
        html.Div(
            style={'width':'15%', 'height':'100%','float':'right'},
            children=[
                dcc.Checklist(className ='checkbox_1',
                        options=[
                            {'label': 'visualization', 'value': 'I1MT'},
                            {'label': 'visualization', 'value': 'I2MT'},
                            {'label': 'visualization', 'value': 'I3MT'},
                            {'label': 'visualization', 'value': 'I4MT'}
                            ],
                        value=['I1MT'],
                        labelStyle = {'display': 'block'}
                                )
            ]
        ),
        html.Div(
        style={'width':'20%', 'height':'100%','float':'right'},
        children=[
            dcc.Checklist(className ='checkbox_1',
                    options=[
                        {'label': 'z-score brain space', 'value': 'I1ST1'},
                        {'label': 'Centile plots', 'value': 'I2ST1'},
                        {'label': 'Exp. Var. plots', 'value': 'I3ST1'},
                        {'label': '[other error measures]', 'value': 'I4ST1'}
                            ],
                    value=['I1ST1'],
                    labelStyle = {'display': 'block'}
                            ),
        ]
        ),

    ], style={'padding': 10, 'flex': 1}),

], style={'display': 'flex', 'flex-direction': 'row', 'height': '80%', 'width': '60%', 'position': 'relative', 'top':'40%', 'left':'20%' })
# -----------------------------------------------------------------
# Functions that handle input and output for the Dash components.

# Function to restrict model choice based on data type choice
@app.callback(
    Output(component_id='model-selection', component_property='options'),
    [Input(component_id='data-type', component_property='value')],
    prevent_initial_call=True
)
def update_dp(filter_value):
    if filter_value == 'Brain surface area':
        # here we could put a df with all available models
        model_selection_list = ['bsa BLR', 'bsa HBR']
    if filter_value == 'Average Thickness':
        model_selection_list = ['at BLR', 'at HBR']
   # df = {"model 1": "model 1", "model 2": "model 2"}
    return model_selection_list

# Load data into the model and store the .csv results on the website.
@app.callback(
    Output("csv_store_session", "data"),
    Output("submitted", "children"),
    Output("results_onclick", "disabled"),
    State("data-type", "value"),
    State("model-selection", "value"),
    State("Upl_1", "contents"),
    State("Upl_1", "filename"),
    State('Upl_1', 'last_modified'),
    State("Upl_2", "contents"),
    State("Upl_2", "filename"),
    State('Upl_2', 'last_modified'),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True
)
def update_output(data_type, algorithm, contents_test, name_test, date_test, 
                  contents_adapt, name_adapt, date_adapt, clicks):
    if contents_test is not None and contents_adapt is not None:
        # Convert input data to pandas
        app_test_data = parse_contents(contents_test, name_test, date_test)
        app_adapt_data = parse_contents(contents_adapt, name_adapt, date_adapt)
        # Compute scores with norm modelling, and output some scores
        # pseudocode
        if data_type == "Brain surface area":
            data_subdir = "SurfArea"
        if data_type == "Average Thickness":
            data_subdir = "ThickAvg"
        z_score_df = pd.DataFrame(apply_normative_model(algorithm, data_subdir, app_test_data, app_adapt_data))
        
        # Return downloadable results
        filename = "z-scores.csv"
        # Convert results dataframe back to .csv
        z_score_csv = dcc.send_data_frame(z_score_df.to_csv, filename)
        finished_message = "Normative modelling is complete!"
        # Modulate download button's disabled property
        disable_download = False
        return z_score_csv, finished_message, disable_download

# Convert input .csv to pandas dataframe
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        # elif 'xls' in filename:
        #     # Assume that the user uploaded an excel file
        #     df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df
# Download the results with a button.
@app.callback(
    Output("download-dataframe-csv", "data"),
    State("csv_store_session","data"),
    Input("results_onclick", "n_clicks")
)
def download_results(results_csv, clicks):
    return results_csv

# List uploaded data files (1)
@app.callback(
    Output("list-data-file", "children"),
    Input("Upl_1", "filename"),
    prevent_initial_call=True,
)
def list_data_file(data_name):
    return html.Li(data_name) 

# List uploaded data files (2)
@app.callback(
    Output("list-cov-file", "children"),
    Input("Upl_2", "filename"),
    prevent_initial_call=True,
)
def list_cov_file(cov_name):
    return html.Li(cov_name) 

# Serve the app upon running the script.
if __name__ == '__main__':
    app.run_server(debug=True)