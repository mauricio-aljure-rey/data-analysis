import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

def launch_dash_app(df, port=8050):
    app = dash.Dash(__name__)

    # Create a filter for each column in the dataframe
    filters = []
    for col in df.columns:
        filters.append(html.Div([
            html.Label(f'Filter by {col}:'),
            dcc.Dropdown(
                id=f'filter-{col}',
                options=[{'label': 'All', 'value': 'All'}] + [{'label': val, 'value': val} for val in df[col].unique()],
                multi=True,
                placeholder=f'Select values for {col}'
            )
        ], style={'display': 'inline-block', 'margin-right': '10px', 'width': '250px'}))  # Width is set here

    app.layout = html.Div([
        html.Div(filters, style={'display': 'flex', 'flex-wrap': 'wrap'}),
        html.Div([
            html.Div([
                html.Label('Select x-axis:'),
                dcc.Dropdown(
                    id='x-axis',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    value=df.columns[0],
                    #placeholder='Select x-axis'
                )
            ], style={'display': 'inline-block', 'margin-right': '10px', 'width': '300px'}),  # Width is set here
            html.Div([
                html.Label('Select y-axis:'),
                dcc.Dropdown(
                    id='y-axis',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    value=df.columns[1],
                    #placeholder='Select y-axis'
                )
            ], style={'display': 'inline-block', 'margin-right': '10px', 'width': '300px'})  # Width is set here
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'margin-top': '10px'}),
        html.Div([
            html.Label('Select color:'),
            dcc.Dropdown(
                id='color',
                options=[{'label': 'None', 'value': 'None'}] + [{'label': col, 'value': col} for col in df.columns],
                value="None",
                # placeholder='Select color'
            )
        #], style={'display': 'flex', 'flex-wrap': 'wrap', 'margin-top': '10px'}),
        
        ], style={'display': 'inline-block', 'margin-right': '10px', 'width': '300px'}),  # Width is set here
        html.Div([
            html.Label('X-axis label:'),
            dcc.Input(id='x-axis-label', type='text', placeholder='Enter x-axis label'),
            html.Label('Y-axis label:'),
            dcc.Input(id='y-axis-label', type='text', placeholder='Enter y-axis label'),
            html.Label('Plot title:'),
            dcc.Input(id='plot-title', type='text', placeholder='Enter plot title'),
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'margin-top': '10px'}),
        # html.Div([
        dcc.Graph(id='graph')
        # ], style={'display': 'inline-block', 'margin-right': '10px', 'width': '1000px'}),  # Width is set here
        
        #], style={'display': 'inline-block', 'margin-right': '10px', 'width': '300px'}),  # Width is set here
    ])

    @app.callback(
        Output('graph', 'figure'),
        [Input(f'filter-{col}', 'value') for col in df.columns] +
        [Input('x-axis', 'value'),
         Input('y-axis', 'value'),
         Input('color', 'value'),
         Input('x-axis-label', 'value'),
         Input('y-axis-label', 'value'),
         Input('plot-title', 'value')]
    )
    def update_graph(*args):
        filter_values = args[:len(df.columns)]
        x_axis = args[len(df.columns)]
        y_axis = args[len(df.columns) + 1]
        color = args[len(df.columns) + 2]
        x_axis_label = args[len(df.columns) + 3]
        y_axis_label = args[len(df.columns) + 4]
        plot_title = args[len(df.columns) + 5]

        filtered_df = df
        for i, col in enumerate(df.columns):
            if filter_values[i] and 'All' not in filter_values[i]:
                filtered_df = filtered_df[filtered_df[col].isin(filter_values[i])]

        if color == 'None':
            color = None

        fig = px.scatter(filtered_df, x=x_axis, y=y_axis, color=color)
        fig.update_layout(
            title=plot_title,
            xaxis_title=x_axis_label,
            yaxis_title=y_axis_label
        )
        return fig

    app.run_server(debug=True, port=port)

# Example usage:
df = pd.read_csv('deaths_all/data_deaths.csv')
launch_dash_app(df, port=8050)
