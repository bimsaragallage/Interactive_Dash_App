from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import datetime as dt
from datetime import datetime, date


df = pd.read_csv('./datasets/pollution_2010_2023.csv')

def remove_outliers_iqr(df, columns, threshold=1.5):
        # Apply outlier removal to specified columns
        for column in columns:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        return df

external_stylesheets = ['assets/styles.css']

app = Dash(title="App", external_stylesheets=external_stylesheets)

tab1 = [
        html.Div(children="Atmospheric Watch: Pollution Over Time",
                 style={'color': 'blue', 'fontSize': 50, 'textAlign': 'center', 'marginBottom': '30px'}),
        html.Div("Time series analysis plays a crucial role in understanding air pollution in the USA by providing insights into the temporal patterns and trends of pollutant concentrations over time. By analyzing historical data collected from various monitoring stations across the country, researchers and policymakers can identify long-term trends, seasonal variations, and short-term fluctuations in air quality. This information enables the detection of pollution hotspots, the assessment of the effectiveness of pollution control measures, and the prediction of future air quality conditions. Time series analysis helps to uncover underlying patterns in pollution levels, aiding in the development of targeted interventions and policies to mitigate the adverse impacts of air pollution on public health and the environment.",
                 style={'fontSize': 20, 'textAlign': 'justify', 'marginBottom': '30px', 'marginLeft': '30px', 'marginRight': '30px'}),
        html.Div([
                dcc.Dropdown(options = [{'label': option, 'value': option} for option in df['Time_zone'].unique()],
                             value = 'Mountain Time Zone',
                             id='timezone_selector_dropdown',
                             className='dropdown_adjuster'),
                dcc.Dropdown(options = [
                                        {'label': 'Average Ozone (O3) Emissions', 'value': 'O3_Mean'},
                                        {'label': 'Average Sulfur Dioxide (SO2) Emissions', 'value': 'SO2_Mean'},
                                        {'label': 'Average Nitrogen Dioxide (NO2) Emissions', 'value': 'NO2_Mean'},
                                        {'label': 'Average Carbon Monoxide (CO) Emissions', 'value': 'CO_Mean'}],
                             value = 'O3_Mean',
                             id='gas_selector_dropdown',
                             className='dropdown_adjuster'),
                dcc.DatePickerRange(id='Time_series_date_picker',
                                    min_date_allowed=df['Date'].min(),
                                    max_date_allowed=df['Date'].max(),
                                    start_date=date(2010, 1, 1),
                                    end_date=date(2010, 1, 31),
                                    className='date_picker')],
                className='dropdown-set'),
        html.Div(className='graph-container',children=[dcc.Graph(id='date_gas_graph1')]),
        html.Div([
                html.Div(children=[
                                dcc.Graph(id='date_gas_Sunburst1',
                                        className='graph-container2'),
                                html.Div(id="date_gas_state1",
                                        className="statements")
                ], className="aligner")
            ])
        ]

tab2 = [
        html.Div(children="Decoding Air Quality",
                 style={'color': 'blue', 'fontSize': 50, 'textAlign': 'center', 'marginBottom': '30px'}),
        html.Div([
                html.Div(f"At the forefront of analyzing air quality lies a thorough examination of the USA's environmental well-being. This visualization offers a comprehensive display of air quality indices across states and cities, revealing insights into pollutant levels, trends, and geographical disparities. From scatter plots revealing correlations between pollutants to box plots illustrating regional variations, this exploration unveils the complex dynamics of air quality. By providing valuable information, it enables strategic interventions and promotes a healthier environment. Through meticulous data analysis, stakeholders can derive actionable insights, guiding targeted policies and initiatives to combat pollution and enhance public health across the nation.",
                        style={'fontSize': 20, 'textAlign': 'justify', 'marginLeft': '30px', 'marginRight': '30px'}),
                html.A("More details on Air Quality Index visit here", href='https://www.who.int/publications/i/item/9789240034228',
                       style={'fontSize': 20, 'textAlign': 'left', 'marginBottom': '30px', 'marginLeft': '30px', 'marginRight': '30px'})]),
        html.Div([
                dcc.Dropdown(df['State'].unique(),
                            value = "Arizona",
                            id='state_aqi_selector_dropdown',
                            className="dropdown_adjuster2"),
                dcc.RadioItems(options=[
                                    {'label': 'Carbon Monoxide (CO) Air Quality Index', 'value': 'CO_AQI'},
                                    {'label': 'Sulfur Dioxide (SO2) Air Quality Index', 'value': 'SO2_AQI'},
                                    {'label': 'Nitrogen Dioxide (NO2) Air Quality Index', 'value': 'NO2_AQI'}],
                            value = 'CO_AQI',
                            id='gas_aqi_selector_dropdown',
                            className="dropdown_adjuster2")],
                className='dropdown-set2'),
        html.Div(className='graph-container',children=[dcc.Graph(id = 'gas_aqi_graph')]),
        html.Div(className='aligner',
                 children=[
                           dcc.Graph(id='gas_aqi_graph2',className='graph-container2'),
                           dcc.Graph(id='gas_aqi_graph3',className='graph-container2')
                           ])
        ]

tab3 = [
        html.Div(children="Pollution Pathways: An Interactive Exploration",
                 style={'color': 'blue', 'fontSize': 50, 'textAlign': 'center', 'marginBottom': '30px'},
                 id='head3', className='head1'),
        html.Div("An Interactive Exploration of Emissions. This immersive experience delves into the intricate realm of time series analysis, unlocking insights into air pollution dynamics across the USA. By harnessing historical data from diverse monitoring stations nationwide, users gain real-time access to temporal patterns and trends in pollutant concentrations. Unveiling long-term trends, seasonal fluctuations, and short-term spikes, this interactive platform empowers researchers and policymakers to pinpoint pollution hotspots, evaluate intervention efficacy, and forecast future air quality scenarios. Through interactive tools and visualizations, users navigate through pollution pathways, unraveling underlying patterns to inform targeted policies and safeguard public health and the environment.",
                 style={'fontSize': 20, 'textAlign': 'justify', 'marginBottom': '30px', 'marginLeft': '30px', 'marginRight': '30px'}),
        html.Div([
                dcc.Dropdown(
                            options=[
                                {'label': 'Ozone (O3)', 'value': 'O3'},
                                {'label': 'Carbon Monoxide (CO)', 'value': 'CO'},
                                {'label': 'Nitrogen Dioxide (NO2)', 'value': 'NO2'},
                                {'label': 'Sulfur Dioxide (SO2)', 'value': 'SO2'}
                            ],
                            value='O3',
                            id='gas_selector_dropdown_2',
                            className="dropdown_adjuster2"),
                dcc.DatePickerRange(id='Time_series_date_picker2',
                                    min_date_allowed=df['Date'].min(),
                                    max_date_allowed=df['Date'].max(),
                                    start_date=date(2010, 1, 1),
                                    end_date=date(2010, 1, 31),
                                    className="date_picker")],
                className='dropdown-set2'),
        html.Div(className='graph-container',children=[dcc.Graph(id = 'interactive_graph')]),
        html.Div(className='aligner',
                 children=[
                           dcc.Graph(id='time_series_1',className='graph-container2'),
                           dcc.Graph(id='time_series_2',className='graph-container2')
                           ])
        ]

tab4 = [
        html.Div(children="Pollution Profiles: State and City Emission Distributions",
                 style={'color': 'blue', 'fontSize': 50, 'textAlign': 'center', 'marginBottom': '30px'},
                 id='head4', className='head1'),
        html.Div("Dive into Pollution Profiles, a comprehensive analysis revealing emission distributions across states and cities. This dynamic exploration illuminates the intricate patterns of pollution, integrating kernel density estimation (KDE) for states and histograms for cities. Unveiling the spatial nuances of pollution hotspots, the analysis highlights variations in emissions across different regions. From urban centers to rural landscapes, Pollution Profiles provides insights into the diverse landscapes of pollution, empowering stakeholders to devise targeted strategies for environmental conservation and public health. By scrutinizing emission patterns at both state and city levels, this analysis paves the way for informed decision-making and proactive measures to mitigate pollution's impact.",
                 style={'fontSize': 20, 'textAlign': 'justify', 'marginBottom': '30px', 'marginLeft': '30px', 'marginRight': '30px'}),
        html.Div([
                dcc.Dropdown(df['State'].unique(), 
                             value = 'Arizona',
                             id='State_selector_dropdown_3',
                             className="dropdown_adjuster2"),
                dcc.Dropdown(['O3', 'CO', 'NO2', 'SO2'], 'O3', 
                             id='gas_selector_dropdown_3',
                             className="dropdown_adjuster2")],
                className='dropdown-set2'),
        html.Div(className='graph-container',children=[dcc.Graph(id = 'kde_graph')]),
        html.Div(className='aligner',
                 children=[
                           dcc.Graph(id='kde_graph_sub1',className='graph-container2'),
                           dcc.Graph(id='kde_graph_sub2',className='graph-container2')
                           ]),
        html.Div(className='aligner',
                 children=[
                           dcc.Graph(id='kde_graph_sub3',className='graph-container2'),
                           dcc.Graph(id='kde_graph_sub4',className='graph-container2')
                           ])
        ]

footer = html.Div(
                children=[
                    html.Div(
                        [
                            html.P('CREATED BY:',
                                style={'font-size': '18px', 'text-align': 'center', 'font-weight': 'bold', 'color': 'black'}),
                            html.P('Bimsara - COHANDDS-012',
                                style={'font-size': '16px', 'text-align': 'center', 'font-weight': 'bold', 'color': 'black'}),
                            html.P('Yashodha - COHANDDS-013',
                                style={'font-size': '16px', 'text-align': 'center', 'font-weight': 'bold', 'color': 'black'}),
                        ],
                        className="footer1"
                    )
                ]
            )



app.layout = html.Div(
    className='container',
    children=[
        html.Div(
            className='tabs-wrapper',
            children=[
                dcc.Tabs(
                    className='tabs-container',
                    children=[
                        dcc.Tab(label='Time Series Analyse', value='tab_1', children=tab1, className='custom-tab'),
                        dcc.Tab(label='Air Quality Indexes', value='tab_2', children=tab2, className='custom-tab'),
                        dcc.Tab(label='Interactive Elements', value='tab_3', children=tab3, className='custom-tab'),
                        dcc.Tab(label='KDE visualization', value='tab_4', children=tab4, className='custom-tab')
                    ],
                    vertical=True
                )
            ]
        ),
        footer
    ]
)



#callback for tab1
@app.callback(
    Output(component_id='date_gas_graph1', component_property='figure'),
    Output(component_id='date_gas_Sunburst1', component_property='figure'),
    Output(component_id='date_gas_state1', component_property='children'),

        Input(component_id='timezone_selector_dropdown', component_property='value'),
        Input(component_id='gas_selector_dropdown', component_property='value'),
        Input(component_id='Time_series_date_picker', component_property='start_date'),
        Input(component_id='Time_series_date_picker', component_property='end_date')
)

def time_series_creator1(timezone, gas_column, str_date, end_date):

    if str_date and end_date:
  
        filtered_data = df[(df['Time_zone'] == timezone) & (df['Date'] >= str_date) & (df['Date'] <= end_date)]

        state_data = filtered_data.groupby(['State','Date']).agg(O3_Mean=pd.NamedAgg(column="O3 Mean", aggfunc="sum"),
                                                                CO_Mean=pd.NamedAgg(column="CO Mean", aggfunc="sum"),
                                                                SO2_Mean=pd.NamedAgg(column="SO2 Mean", aggfunc="sum"),
                                                                NO2_Mean=pd.NamedAgg(column="NO2 Mean", aggfunc="sum")).reset_index()
        state_data2 = filtered_data.groupby(['State','City']).agg(O3_Mean=pd.NamedAgg(column="O3 Mean", aggfunc="sum"),
                                                                CO_Mean=pd.NamedAgg(column="CO Mean", aggfunc="sum"),
                                                                SO2_Mean=pd.NamedAgg(column="SO2 Mean", aggfunc="sum"),
                                                                NO2_Mean=pd.NamedAgg(column="NO2 Mean", aggfunc="sum")).reset_index()
        fig1 = px.line(state_data, x="Date", y=gas_column,
               color="State",
               title=f"{gas_column.replace('_', ' ').title()} Levels(ppm) Over Time by State",
               labels={"Date": "Date", gas_column: f"{gas_column.replace('_', ' ').title()} Level (ppm)"},
               )
        fig1.update_layout(title_font_size=18, xaxis_title_font_size=14, yaxis_title_font_size=14)
        
        formatted_date = pd.to_datetime(state_data['Date']).dt.strftime("%B %d, %Y")
        fig1.update_traces(hovertext=formatted_date)

        fig2 = px.sunburst(
                        state_data2, 
                        path=['State', 'City'],
                        color=gas_column,
                        color_continuous_scale='deep',
                        color_continuous_midpoint=round(np.average(state_data2[gas_column]),3),
                        title=f"{gas_column.replace('_', ' ').title()}(ppm) Distribution Across States and Cities",
                        labels={"State": "State", "City": "City", gas_column: f"{gas_column.replace('_', ' ').title()} Level"}
                        )
        fig2.update_layout(title_font_size=15)


        if not state_data.empty:

            max1 = state_data[gas_column].max()
            max_state = state_data[state_data[gas_column] == max1]['State'].iloc[0]
            max_date_str = state_data[state_data[gas_column] == max1]['Date'].iloc[0]
            max_date = dt.datetime.strptime(max_date_str, '%Y-%m-%d')
            max_month = max_date.month

            if max_month in [12, 1, 2]:
                max_season = "winter"
            elif max_month in [3, 4, 5]:
                max_season = "spring"
            elif max_month in [6, 7, 8]:
                max_season = "summer"
            elif max_month in [9, 10, 11]:
                max_season = "autumn"
            else:
                max_season = "Unknown"


            min1 = state_data[gas_column].min()
            min_state = state_data[state_data[gas_column] == min1]['State'].iloc[0]
            min_date = state_data[state_data[gas_column] == min1]['Date'].iloc[0]

            mean_value = state_data[gas_column].mean()
            median_value = state_data[gas_column].median()

            statement = [
                        f"The highest recorded level of {gas_column} was observed in {max_state}, reaching {max1:.3f}. This level signifies significant {gas_column} pollution. Time series analysis reveals seasonal fluctuations, particularly peaking during {max_season} months. For instance, on {max_date}, {gas_column} levels spiked to {max1:.3f}, emphasizing the health risks associated with elevated {gas_column} concentrations during {max_season} seasons. Conversely, {min_state} exhibits the lowest {gas_column} levels, recorded at {min1:.3f} on {min_date}, suggesting effective pollution control measures or geographical advantages. On average, across all states, {gas_column} levels remain around {mean_value:.3f}, with a median value of {median_value:.3f}, indicating the typical distribution of {gas_column} concentrations across the dataset."
                    ]
               
        else:
            statement = ["No data available.", "No data available."]
    
    figs = [fig1,fig2]

    for i in range(2):
        figs[i].update_layout(paper_bgcolor='rgba(255,255,255,0.5)', plot_bgcolor='rgba(255,255,255,0.5)')
        figs[i].update_layout(title_x=0.5)

    return fig1, fig2, statement


#callback for tab2
@app.callback(
Output(component_id='gas_aqi_graph', component_property='figure'),
Output(component_id='gas_aqi_graph2', component_property='figure'),
Output(component_id='gas_aqi_graph3', component_property='figure'),

    Input(component_id='state_aqi_selector_dropdown', component_property='value'),
    Input(component_id='gas_aqi_selector_dropdown', component_property='value')
)

def scatter_creator(cho_state, gas_type):
    
    state_selector = df[df['State'] == cho_state]

    state_data_aqi = state_selector.groupby(['City','Date']).agg(O3_AQI=pd.NamedAgg(column="O3 AQI", aggfunc="mean"),
                                                                CO_AQI=pd.NamedAgg(column="CO AQI", aggfunc="mean"),
                                                                SO2_AQI=pd.NamedAgg(column="SO2 AQI", aggfunc="mean"),
                                                                NO2_AQI=pd.NamedAgg(column="NO2 AQI", aggfunc="mean")).reset_index()

    columns_to_clean = ["O3_AQI", "CO_AQI", "SO2_AQI", "NO2_AQI"]
    state_data_aqi = remove_outliers_iqr(state_data_aqi, columns_to_clean)
    # Extract gas name from gas type
    gas_name = gas_type.split('_')[0]

    correlation = round(state_data_aqi['O3_AQI'].corr(state_data_aqi[gas_type]),3)

    # Scatter plot (fig1) modifications
    fig1 = px.scatter(state_data_aqi, x="O3_AQI", y=gas_type, color="City", trendline="ols")
    fig1.update_layout(
        title=f"{gas_name} AQI vs Ozone (O3) AQI Across Cities (Overall Correlattion: {correlation})",
        xaxis_title="Ozone (O3) Air Quality Index (AQI)",
        yaxis_title=f"{gas_name} Air Quality Index (AQI)"
    )

    # Box plot (fig2) modifications
    fig2 = px.box(state_data_aqi, x="City", y="O3_AQI", color="City")
    fig2.update_layout(
        title=f"Variation in Ozone (O3) AQI Across Cities",
        xaxis_title="City",
        yaxis_title="Ozone (O3) Air Quality Index (AQI)"
    )

    # Another Box plot (fig3) modifications
    fig3 = px.box(state_data_aqi, x="City", y=gas_type, color="City")
    fig3.update_layout(
        title=f"Variation in {gas_name} AQI Across Cities",
        xaxis_title="City",
        yaxis_title=f"{gas_name} Air Quality Index (AQI)"
    )

    figs = [fig1, fig2, fig3]

    for i in range(3):
        figs[i].update_layout(paper_bgcolor='rgba(255,255,255,0.5)', plot_bgcolor='rgba(255,255,255,0.5)')
        figs[i].update_layout(title_x=0.5)

    return fig1, fig2, fig3



#callback for tab3
@app.callback(
    Output(component_id='interactive_graph', component_property='figure'),
    Output('time_series_1', 'figure'),
    Output('time_series_2', 'figure'),
        Input(component_id='gas_selector_dropdown_2', component_property='value'),
        Input(component_id='Time_series_date_picker2', component_property='start_date'),
        Input(component_id='Time_series_date_picker2', component_property='end_date'),
        Input(component_id='interactive_graph', component_property='hoverData')
)


def interactive_creator(cho_gas,date_str,date_end,hoverData):

    mean_column = f"{cho_gas} Mean"
    max_hour_column = f"{cho_gas} 1st Max Hour"
    
    state_group = df.groupby(['State']).agg(
        **{
            f"{cho_gas}_Mean": pd.NamedAgg(column=mean_column, aggfunc="sum"),
            f"{cho_gas}_1st_Max_Hour": pd.NamedAgg(column=max_hour_column, aggfunc="mean")
        }
    ).reset_index()

    fig = px.scatter(
                    state_group, 
                    x=f"{cho_gas}_Mean", 
                    y=f"{cho_gas}_1st_Max_Hour", 
                    color="State",
                    labels={
                        f"{cho_gas}_Mean": f"{cho_gas} Concentration (ppm,Sum)",
                        f"{cho_gas}_1st_Max_Hour": f"{cho_gas} First Max Hour",
                        "State": "State"
                    },
                    title=f"Scatter Plot of {cho_gas} Mean Concentration vs First Max Hour by State"
                )


    fig1 = go.Figure()
    fig2 = go.Figure()
    
    if date_str is not None and date_end is not None and hoverData is not None:        

        filtered_df = df[(df['Date'] >= date_str) & (df['Date'] <= date_end)]
        state_number = hoverData['points'][0]['curveNumber']
        state_name = state_group['State'][state_number] 
        state_df = filtered_df[filtered_df['State'] == state_name]

        # Define aggregation specifications
        agg_spec = {
            f"{cho_gas}_Mean": pd.NamedAgg(column=f"{cho_gas} Mean", aggfunc="sum"),
            f"{cho_gas}_1st_Max_Hour": pd.NamedAgg(column=f"{cho_gas} 1st Max Hour", aggfunc="mean")
        }
        
        # Group by date within the selected state and aggregate
        state_group_df = state_df.groupby(['Date']).agg(**agg_spec).reset_index()

        # Generate plots
        fig1 = px.line(state_group_df, x='Date', y=f'{cho_gas}_Mean', 
                    title=f"Avarage {cho_gas} (ppm) for {state_name}")
        fig2 = px.line(state_group_df, x='Date', y=f'{cho_gas}_1st_Max_Hour', 
                    title=f"{cho_gas} 1st Max Hour for {state_name}")
        
    figs = [fig,fig1,fig2]

    for i in range(3):
        figs[i].update_layout(paper_bgcolor='rgba(255,255,255,0.5)', plot_bgcolor='rgba(255,255,255,0.5)')
        figs[i].update_layout(title_x=0.5)

    return fig, fig1, fig2


#callback for tab4
@app.callback(
    Output(component_id='kde_graph', component_property='figure'),
    Output(component_id='kde_graph_sub1', component_property='figure'),
    Output(component_id='kde_graph_sub2', component_property='figure'),
    Output(component_id='kde_graph_sub3', component_property='figure'),
    Output(component_id='kde_graph_sub4', component_property='figure'),

        Input(component_id='kde_graph', component_property='clickData'),
        Input(component_id='State_selector_dropdown_3', component_property='value'),
        Input(component_id='gas_selector_dropdown_3', component_property='value')

)

def kde_creator(click_data,state_selected,cho_gas):

    cal_data = df[df['State'] == state_selected]
        
    data = []
    labels = []

    column_gas = f'{cho_gas} 1st Max Hour'
    
    grouped = cal_data.groupby('City')
        
    for city, group in grouped:
        data.append(group[column_gas].values)
        labels.append(city)

    bin_size = [1 for _ in data]
    
    fig = ff.create_distplot(data, labels, bin_size=bin_size, show_rug=False)

    for trace in fig['data']:
        trace['opacity'] = 0.75
    
    fig.update_layout(paper_bgcolor='rgba(255,255,255,0.5)', plot_bgcolor='rgba(255,255,255,0.5)')
    fig.update_layout(title_x=0.5)
    fig.update_layout(
                    title={
                        'text': f"Distribution of {cho_gas} 1st Max Hour in {state_selected}",
                        'x':0.5
                    },
                    xaxis_title=f"{cho_gas} 1st Max Hour",
                    yaxis_title="Density")

    figs = [go.Figure() for _ in range(4)]

    if click_data is not None:
        city_number = click_data['points'][0]['curveNumber']
        city_names = list(grouped.groups.keys())
        city_name = city_names[city_number] 
        city_df = cal_data[cal_data['City'] == city_name]

        for i, gas_type in enumerate(['O3', 'NO2', 'SO2', 'CO']):
            figs[i] = px.histogram(city_df,
                                    x=f"{gas_type} 1st Max Hour",
                                    title=f"Hourly Distribution of {gas_type} Peaks in {city_name}",
                                    labels={'x': f"{gas_type} First Max Hour", 'count': 'Frequency'},
                                    color_discrete_sequence=['turquoise'])

            
    for i in range(4):
        i -= 1
        figs[i].update_layout(paper_bgcolor='rgba(255,255,255,0.5)', plot_bgcolor='rgba(255,255,255,0.5)')
        figs[i].update_layout(title_x=0.5)

    return fig, figs[0], figs[1], figs[2], figs[3]


if __name__ == '__main__':
    app.run(debug=True)