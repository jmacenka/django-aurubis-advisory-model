# Dash Module initialization for Advisory Frontend
# Created by Tobias Bosse @ ?? Sept 2023
# This file creates the initialization of the dash app and its configuration. It follow the factory-pattern approach where init_dash_app is invoked at the run-script.

# Library imports
from datetime import datetime, timedelta
import pandas as pd
from django_plotly_dash import DjangoDash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Module imports
from connectors import instantiated_osipiconnector as con
from utils.TimestampHandling import tz_aware_timestamp

# Configuration imports
from config import (
    CELOX_O2_DEFAULT_UPPER_THRESHHOLD,
    CELOX_O2_DEFAULT_LOWER_THRESHHOLD,
    CHARGE_START_HOUR,
)

# Integrate Dash app into Flask app
def create_dash_app():
    # Initiate the Dash app
    dash_app = DjangoDash('aurubis_advisory_model')

    # Create timestamps for initial data-loading
    initial_end_timestamp = datetime.utcnow()
    initial_start_timestamp = initial_end_timestamp - timedelta(days=1)

    parameter_to_display = 'ACTUAL_CELOX_O2'

    # Pull the data once
    df = con.get_data(
        start_time = initial_start_timestamp, 
        end_time = initial_end_timestamp,
    )

    df = df[df[parameter_to_display] <= 20000] # TODO: Create a dynamic threshhold handling

    #df[parameter_to_display].dt.tz_localize('UTC')

    filtered_df = df[(df[parameter_to_display] >= 0) ] 
        
    fig = px.line(filtered_df, y=parameter_to_display)

    dash_app.layout = html.Div([
        html.Div([  # Dieses div enthält die Elemente in der ersten Spalte (DatePicker, TimePickers)
            dcc.DatePickerRange(
                id='my-date-picker-range',
                start_date=initial_start_timestamp.date(),
                end_date=initial_end_timestamp.date(),
                display_format='YYYY-MM-DD',
            ),
            dcc.Input(
                id='start-time-picker',
                type='time',
                value='00:00',
            ),
            dcc.Input(
                id='end-time-picker',
                type='time',
                value='23:59',
            ),
            dcc.Graph(
                id='example-graph',
                config={'responsive': True},
                figure=fig
            ),
        ], style={'width': '70%', 'display': 'inline-block'}),

        html.Div([  # Dieses div enthält die Elemente in der zweiten Spalte (Graph, Checklist)
            
            dcc.Checklist(
                id="checklist",
                options=[{'label': str(row[parameter_to_display]), 'value': str(i)+"_"+str(row[parameter_to_display])} for i, row in df.iterrows()]
            )
        ], style={'width': '30%', 'display': 'inline-block', 'float': 'right'}),
    ], style={'width': '100%', 'height': '100%'})

    @dash_app.callback(
        Output('example-graph', 'figure'),
        Output('checklist', 'options'),
        [
            Input('my-date-picker-range', 'start_date'),
            Input('my-date-picker-range', 'end_date'),
            Input('start-time-picker', 'value'),
            Input('end-time-picker', 'value'),
            Input('checklist', 'value')  # Added input for checklist
        ]
    )
    def update_output(start_date, end_date, start_time, end_time, selected_values):

        start_datetime = datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(f"{end_date} {end_time}", '%Y-%m-%d %H:%M')

        start_datetime = tz_aware_timestamp(start_datetime)
        end_datetime = tz_aware_timestamp(end_datetime)

        df = con.get_data(
            start_time = start_datetime, 
            end_time = end_datetime,
        )

        filtered_df = df[(df.index >= pd.Timestamp(start_datetime)) & (df.index <= pd.Timestamp(end_datetime)) & (df[parameter_to_display] <= 20000) & (df[parameter_to_display] >= 0) ] 
        
        fig = px.line(filtered_df, y=parameter_to_display)
        opts = [{'label': str(row[parameter_to_display]), 'value': i} for i, row in filtered_df.iterrows()]
        return fig, opts

    return dash_app
