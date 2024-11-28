# Import required libraries
import pandas as pd # type: ignore
import dash # type: ignore
from dash import html, dcc # type: ignore
from dash.dependencies import Input, Output # type: ignore
import plotly.express as px # type: ignore

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard SB',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Task 1: create Drop-down input component for the Launch Site
    dcc.Dropdown(id='site-dropdown',  
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder='Select Launch Site please',
                 searchable=True),
    html.Br(),
    
    # Display in layout task 2
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    # Task 4: Add Range Slider to select Payload
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 11000, 2000)},
                    value=[min_payload, max_payload]),
    
    # Display in layout task 4
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Task 2: Creating a callback for pie chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Successful Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Total Success/Failure Launches for {entered_site}')
    return fig

# Task 4: Creating a callback for scatter chart
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    filtered_df['Booster Color'] = filtered_df['Booster Version'].apply(lambda version: version.split()[1])
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Color',
                         title='Correlation between Payload and Success for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Color',
                         title=f'Payload vs. Success for {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)