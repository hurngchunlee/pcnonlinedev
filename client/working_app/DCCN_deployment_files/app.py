# Created by: Pieter Barkema
# Date: February, 2022
# Description:
#    Users can access this online app to process their neuroimaging data
#    with normative modelling. It should return z-score results, by uploading them to SURFdrive
#    and emailing the download link to the user. 
#    It is hosted as a website from a remote gunicorn server.

from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from subprocess import PIPE, Popen, run, call, check_output
from flask import Flask
#import os, sys
import io, os, base64

# Create a flask server
server = Flask(__name__)
# Create  Dash app
app = Dash(server=server, external_stylesheets=[dbc.themes.MATERIA])

# Function to list available data types and models directly from directories.
def retrieve_options(data_type=None):
    import ast
    # can be models dir or models/data_type subdir
    chosen_dir = "models"
    if data_type is not None:
        chosen_dir = os.path.join("models", data_type)
    list_dirs = ["python", "/project_cephfs/3022051.01/list_subdirs.py", "{chosen_dir}".format(chosen_dir=chosen_dir)]
    
    p = Popen(list_dirs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    # is this helpful? gives the return code of the command
    # rc = p.returncode

    # strip, to get rid of (/n)
    byte_to_string = str(output, encoding='UTF-8').strip()
    print(f'{byte_to_string}')
    string_to_list = ast.literal_eval(byte_to_string)

    return string_to_list

# -----------------------------------------------------------------
# The entire HTML contents of the app.
# -----------------------------------------------------------------
app.layout = html.Div([
    dbc.Col(
    html.Div(children=[
        html.Br(),
        html.Label('Email address for results: '),
        html.Br(),
        dcc.Input(value='', type='text', id='email_address'),
    
        html.Br(),
        html.Br(),
        html.Label('Data type'),
        dcc.Dropdown(options = retrieve_options(), id='data-type'),
        
        html.Br(),
        html.Label('Normative Model'),
        dcc.Dropdown( options = ['please select data type first'], value = 'please select data type first', id='model-selection'),

        html.Br(),
        html.Label('Select data format'),
        dcc.Dropdown(['.csv'], '.csv'), #['.csv', 'NIFTI', '[other formats]']

        html.Br(),
        html.Hr(),
        html.Label('Upload test data'),
        html.Hr(),
        dcc.Upload([
            'Drag and Drop or ',
            html.A('Select a File')
        ], style={
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
        
        html.Div(
            children=[
                # -----------------------------------------------------------------
                # To-do: add functionality for checklists that control results output
                dcc.Checklist(className ='checkbox_1',
                            style={'margin-right': '15px'},
                            options=[
                                {'label': 'raw data', 'value': 'I1ST2', 'disabled': 'True'},
                                {'label': 'raw data', 'value': 'I2ST2', 'disabled': 'True'},
                                {'label': 'raw data', 'value': 'I3ST2', 'disabled': 'True'},
                                {'label': 'raw data', 'value': 'I4ST2', 'disabled': 'True'}
                                    ],
                            value=['I1ST2'],
                            labelStyle = {'display': 'block'}
                                    ),
                dcc.Checklist(className ='checkbox_1',
                              style={'margin-right': '15px'},
                            options=[
                                {'label': 'visualization', 'value': 'I1MT', 'disabled': 'True'},
                                {'label': 'visualization', 'value': 'I2MT', 'disabled': 'True'},
                                {'label': 'visualization', 'value': 'I3MT', 'disabled': 'True'},
                                {'label': 'visualization', 'value': 'I4MT', 'disabled': 'True'}
                                ],
                            value=[],
                            labelStyle = {'display': 'block'}
                                    ),
                dcc.Checklist(className ='checkbox_1',
                              style={'margin-right': '15px'},
                        options=[
                            {'label': 'z-score brain space', 'value': 'I1ST1', 'disabled': 'True'},
                            {'label': 'Centile plots', 'value': 'I2ST1', 'disabled': 'True'},
                            {'label': 'Exp. Var. plots', 'value': 'I3ST1', 'disabled': 'True'},
                            {'label': '[other error measures]', 'value': 'I4ST1', 'disabled': 'True'}
                                ],
                        value=['I1ST1'],
                        labelStyle = {'display': 'block'}
                                ),
                # -----------------------------------------------------------------
                # Submit computation request
                html.Div(
                    style={'float':'right'},
                    children=[
                        html.Button("Submit", id="btn_csv"),
                        html.Plaintext(id="submitted"),
                        # To-do: make it downloadable onclick. this works together with disable_download also commented out.
                        # Download your predictions in .csv format!
                        #html.Button("Download", id="results_onclick", disabled=True),
                        # Store the results files so they can be downloaded on click, not instantly
                        #dcc.Store(id="csv_store_session", storage_type="session"),
                        #dcc.Download(id="download-dataframe-csv")
                    ]
                )
                ]
            , style={'float': 'right', 'display':'flex'}
            )
    ], style={'padding': 10, 'flex': 1})),
], style={'display': 'flex', 'flex-direction': 'row', 'height': '80%', 'width': '60%', 'position': 'relative', 'top':'40%', 'left':'20%' })

# -----------------------------------------------------------------
# Functions that handle input and output for the Dash components.
# -----------------------------------------------------------------

# Function to restrict model choice based on data type choice
@app.callback(
    Output(component_id='model-selection', component_property='options'),
    [Input(component_id='data-type', component_property='value')],
    prevent_initial_call=True
)
# Use pre-defined function to list available options.
def update_dp(data_type):
    model_selection_list = retrieve_options(data_type)
    return model_selection_list

# Transfer data to server side for computation
# TO-DO: and store the .csv results on the website.
@app.callback(
    #Output("csv_store_session", "data"),
    Output("submitted", "children"),
    #Output("results_onclick", "disabled"),
    State("email_address", "value"),
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
def update_output(email_address, data_type_dir, model_name, contents_test, name_test, date_test, 
                  contents_adapt, name_adapt, date_adapt, clicks):
    import subprocess
    # TO-DO this if could use an 'else'
    if contents_test is not None and contents_adapt is not None:
        # Convert input csv data to pandas
        test_data_pd = parse_contents(contents_test, name_test, date_test)
        adapt_data_pd = parse_contents(contents_adapt, name_adapt, date_adapt)
        # Remote working_dir
        
        test_path = "/home/user/test.pkl"
        adapt_path = "/home/user/adapt.pkl"
        test_data_pd.to_pickle(test_path)
        adapt_data_pd.to_pickle(adapt_path)
        
        # execute a bash script that qsubs an apply_model to the cluster
        # create random session integer as name
        import random
        session_id = "session_id" + str(random.randint(100000,999999))
        # project_folder, can hardcode this in bash script
        project_dir = "/project_cephfs/3022051.01"
        # start restructuring dirs here!
        session_dir = os.path.join(project_dir, "sessions", session_id)
        # create session dir and transfer data there
        scp = """mkdir -p {session_dir} && 
        mv {test} {adapt} {session_dir}""".format(session_dir = session_dir, test=test_path, adapt=adapt_path)
        
        subprocess.call(scp, shell=True)
        algorithm = model_name.split("_")[0]
        execute = 'bash execute_modelling.sh {project_dir} {model_name} {data_type_dir} {session_id} {algorithm} {email_address}'.format(project_dir = project_dir, model_name=model_name, data_type_dir = data_type_dir, session_id=session_id, algorithm=algorithm, email_address = email_address) 
        subprocess.call(execute, shell=True)
        
        finished_message = "Your computation request has been sent!"
        # Now disabled because downloading is pointless when we email results
        #disable_download = True
        return finished_message#z_score_csv, disable_download

# Convert input .csv to pandas dataframe (currently unused).
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

# Download the results with a button (currently unused).
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