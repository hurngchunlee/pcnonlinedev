from dash import Dash, html, dcc, Input, Output, State, dash_table
import pandas as pd
import datetime, io, base64

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children=[
            
        html.Br(),
        html.Label('Email address for results: '),
        dcc.Input(value='', type='text'),
    
        html.Br(),
        html.Br(),
        html.Label('Normative Model'),
        dcc.Dropdown(['GPR type A', 'GPR type B','BLR type A', 'BLR type B', 'HBR type A', 'HBR type B'], 'GPR type A'),
        html.Br(),
        html.Label('Select data format'),
        dcc.Dropdown(['.csv', 'NIFTI', '[other formats]'], '.csv'),

#        dcc.Upload(html.Button('Upload File')),
        html.Br(),
        html.Hr(),
        html.Label('Upload Data File'),
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
       
        html.Ul(id="list-data-file"),
        
        html.Hr(),
        dcc.Upload(html.A('Upload Covariates')),
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
        html.Ul(id="list-cov-file"),         
        
        html.Div(
            style={'width':'5%', 'height':'100%','float':'right','position':'relative', 'top':'4%'},
            children=[
                html.Button("Submit", id="btn_csv"),
                html.Plaintext(id="submitted"),
            ]
        ),
        
        # Download is a placeholder for send-to-server.
        # Download is a placeholder for send-to-server.
#        dcc.Download(id="download-dataframe-csv"),
#        dcc.Download(id="download-dataframe-csv2"),
        

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
        

        #html.Br(),
        #html.Label('Radio Items'),
        #dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
    ], style={'padding': 50, 'flex': 1, 'width': '40%'}),

    html.Div(id='output-data-upload'),
    html.Div(id='output-cov-upload')
#    html.Div(children=[
#        
#        
#        #dcc.Store(id='local_store', storage_type='local')
#    
#    ], style={'padding':20, 'flex': 1, 'position': 'relative', 'top':'200px', 'left':'200px'})
    
], style={'display': 'flex', 'flex-direction': 'row', 'height': '80%', 'width': '80%', 'position': 'relative', 'top':'40%', 'left':'0%' })


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8'))).head()
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

# cmd commands to connect to serverside
#def run_docker(contents, filename):
#        docker = subprocess.Popen(["docker run, "-i .ssh/id_rsa", "user@host"],
#                                stdin =subprocess.PIPE,
#                                stdout=subprocess.PIPE,
#                                stderr=subprocess.PIPE,
#                                universal_newlines=True,
#                                bufsize=0)
#         
#        # Send ssh commands to stdin
#        ssh.stdin.write("uname -a\n")
#        ssh.stdin.write("uptime\n")
#        ssh.stdin.close()
#        
#        # Fetch output
#        for line in ssh.stdout:
#            print(line.strip())

# run docker apply normative models with my current csv.file

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

       # html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
#        html.Div('Raw Content'),
#        html.Pre(contents[0:10] + '...', style={
#            'whiteSpace': 'pre-wrap',
#            'wordBreak': 'break-all'
#        })
    ])

#df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 1, 5, 6], "c": ["x", "x", "y", "y"]})
        # 2 functions, where one puts uploda to download data, and one sends click to download
@app.callback(
    Output("output-data-upload", "children"),
    State("Upl_1", "contents"),
    State("Upl_1", "filename"),
    State('Upl_1', 'last_modified'),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def update_output(list_of_contents, list_of_names, list_of_dates, n_clicks):
    if list_of_contents is not None:
        children = parse_contents(list_of_contents, list_of_names, list_of_dates)
        return children

#@app.callback(
#    Output("output-cov-upload", "children"),
#    State("Upl_2", "contents"),
#    State("Upl_2", "filename"),
#    Input("btn_csv", "n_clicks"),
#    prevent_initial_call=True,
#)
#
#def submit_covs(covs_contents, covs_filename, n_clicks):
#    return dict(content=covs_contents, filename=covs_filename)

@app.callback(
    Output("submitted", "children"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def submitted(clicked):
    return html.Plaintext("Submitted!")

@app.callback(
    Output("list-data-file", "children"),
    Input("Upl_1", "filename"),
    prevent_initial_call=True,
)
def list_data_file(data_name):
    return html.Li(data_name) 

@app.callback(
    Output("list-cov-file", "children"),
    Input("Upl_2", "filename"),
    prevent_initial_call=True,
)
def list_cov_file(cov_name):
    return html.Li(cov_name) 

#@app.callback(
#    Output("download-dataframe-csv", "data"),
#    Input("btn_csv", "n_clicks"),
#    prevent_initial_call=True,
#)
#def func2(n_clicks):
#    return dict(content=upload_data, filename="test.txt") 

if __name__ == '__main__':
    app.run_server(debug=True)