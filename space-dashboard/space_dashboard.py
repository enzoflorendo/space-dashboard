from space_functions import (
    GetMissionCountByCompany,
    GetSuccessRate,
    GetMissionsByDateRange,
    GetTopCompaniesByMissionCount,
    GetMissionStatusCount,
    GetMissionsByYear,
    GetMostUsedRocket,
    GetAverageMissionsPerYear,
    load_data
   )

import dash
from dash import html, dcc, dash_table, Input, Output
import plotly.express as px
import pandas as pd

data = load_data()
app = dash.Dash(__name__)

#VIS 1 - create bar chart for total missions by company
missions_per_company = data['Company'].value_counts().reset_index()
missions_per_company.columns = ['Company', 'Missions']

fig_company = px.bar(
    missions_per_company,
    title='Total Missions by Company',
    x='Company',
    y='Missions',
    text='Missions',
    color='Company',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
#customize layout for bar graph for better aesthetics
fig_company.update_layout(
    plot_bgcolor='#1e1e1e',
    paper_bgcolor='#1e1e1e',
    font_color='white',
    title={
        "text": "Total Missions by Company",
        "font": {"family": "Helvetica", "size": 24, "color": "white"},
        "x": 0.5,
    },
    xaxis=dict(title = "Company", title_font = dict(family = 'Helvetica', size = 20, color = 'white'),
               tickfont=dict(family='Helvetica', size=12, color='white')),
    yaxis=dict(title = "Missions", title_font = dict(family = 'Helvetica', size = 20, color = 'white'),
               tickfont=dict(family='Helvetica', size=12, color='white'))
)

#VIS 2 - create success over time line graph
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

data['Year'] = data['Date'].dt.year #year only

#success rate per year (lambda function?)
success_rate_per_year = (
    data.groupby('Year')['MissionStatus']
    .apply(lambda x: (x == 'Success').sum() / len(x) * 100)
    .reset_index(name='SuccessRate')
)

#create line graph for success over time
fig_success = px.line(
    success_rate_per_year,
    x='Year',
    y='SuccessRate',
    markers=True,  #show dots on each year
    title='Mission Success Rate Over Time'
)

#layout formatting like for bar graph, dark theme

fig_success.update_traces(
    line=dict(color='#DFC5FE', width=2),
    marker=dict(color='#DFC5FE', size=8)
)

fig_success.update_layout(
    plot_bgcolor='#1e1e1e',
    paper_bgcolor='#1e1e1e',
    font_color='white',
    title={
        "text": "Mission Success Rate Over Time", "font": {"family": "Helvetica", "size": 24, "color": "white"}, "x": 0.5},
    xaxis=dict(
        title="Year", title_font=dict(family='Helvetica', size=20, color='white'),
        tickfont=dict(family='Helvetica', size=14, color='white')),
    yaxis=dict(
        title="Success Rate (%)", title_font=dict(family='Helvetica', size=20, color='white'),
        tickfont=dict(family='Helvetica', size=14, color='white'))
)

#VIS 3 - pie chart is below in callback section.

#VIS 4 - the stacked bar chart for mission outcomes arranged by company
missions_by_company_outcome = data.groupby(['Company', 'MissionStatus']).size().reset_index(name='Count')

#define colors matching the pie chart. same hexcodes.
color_map = {
    "Success": "#6FCF97",
    "Failure": "#EB5757",
    "Partial Failure": "#F2C94C",
    "Prelaunch Failure": "#B77A50"
}

fig_stacked = px.bar(
    missions_by_company_outcome,
    x='Company',
    y='Count',
    color='MissionStatus',
    color_discrete_map=color_map,
    text='Count',
    title='Missions by Company and Outcome'
)

#layout styling to match dashboard
fig_stacked.update_layout(
    barmode='stack',
    plot_bgcolor='#1e1e1e',
    paper_bgcolor='#1e1e1e',
    font_color='white',
    title={"text": "Missions by Company and Outcome", "x": 0.5,
           "font": {"family": "Helvetica", "size": 24, "color": "white"}},
    xaxis=dict(title="Company",
               title_font=dict(family='Helvetica', size=20, color='white'),
               tickfont=dict(family='Helvetica', size=14, color='white')),
    yaxis=dict(title="Missions",
               title_font=dict(family='Helvetica', size=20, color='white'),
               tickfont=dict(family='Helvetica', size=14, color='white')),
    legend=dict(title="Mission Outcome", font=dict(family="Helvetica", size=12, color="white"))
)

app.layout = html.Div(
    [
        #three circles overlapping, top left of dashboard
        html.Div([
            html.Div(style={
                "height": "40px",
                "width": "40px",
                "opacity": 0.8,
                "backgroundColor": "#DFC5FE",
                "borderRadius": "50%",
                "position": "absolute",
                "top": "10px",
                "left": "10px"
            }),
            html.Div(style={
                "height": "40px",
                "width": "40px",
                "opacity": 0.8,
                "backgroundColor": "#DFC5FE",
                "borderRadius": "50%",
                "position": "absolute",
                "top": "10px",
                "left": "35px"
            }),
            html.Div(style={
                "height": "40px",
                "width": "40px",
                "opacity": 0.8,
                "backgroundColor": "#DFC5FE",
                "borderRadius": "50%",
                "position": "absolute",
                "top": "10px",
                "left": "60px"
            }),
        ], style={"position": "relative", "height": "50px"}),

        #main title for dashboard
        html.H1("Space Missions Dashboard", style={
            "textAlign": "center",
            "color": "#DFC5FE",
            "fontFamily": "Helvetica",
            "fontSize": "50px",
        }),
        
        #main table title
        html.H2("All Space Missions Database", style={"color": "white", "marginTop": "24px", "fontFamily": "Helvetica", "textAlign": "center"}),

        #add data table with "sorting and filtering capabilities"
        dash_table.DataTable(
            id='missions-table',
            columns=[{"name": i, "id": i} for i in data.columns], #column headers for clarity
            data=data.to_dict('records'), #imported rows from the csv file                    #type: ignore
            page_size=10,
            sort_action="native",  #sorting by column
            filter_action="native",  #filtering/search capabilities
            style_table={"overflowX": "auto"},  #horizontal scroll
            style_cell={
                "textAlign": "left", "backgroundColor": "#2e2e2e",  #table bg color, different from the main bg color
                "color": "white" },
            style_filter={
            "backgroundColor": "#DFC5FE", "color": "black", "border": "none"},
            style_header={
                "backgroundColor": "#444444", "fontWeight": "bold" }),
    
    #put the bar chart in below data table
        dcc.Graph(id='missions-per-company', figure=fig_company, style={"marginTop": "50px", "marginBottom": "100px", "height": "700px", "border": "2px solid #DFC5FE", "borderRadius": "10px"}),

    #interactivity for line graph
    #dropdown filter for company filtering
dcc.Dropdown(
    id='line-company-dropdown',
    options=[{'label': c, 'value': c} for c in sorted(data['Company'].unique())],
    value=None,  #default = all companies displayed
    placeholder="Select a company for the line graph",
    multi=False,
    style={"color": "black",
           "backgroundColor": "#DFC5FE", #background color matches dark/lavender theme
            "fontFamily": "Helvetica",    
            "fontSize": "14px",
            "width": "260px",
            "marginBottom": "20px"}
),

#slider for the year range filter
dcc.RangeSlider(
    id='year-range-slider',
    min=int(data['Year'].min()),
    max=int(data['Year'].max()),
    step=1,
    value=[int(data['Year'].min()), int(data['Year'].max())],
    marks={year: str(year) for year in range(int(data['Year'].min()), int(data['Year'].max())+1, 5)},
    tooltip={"placement": "bottom", "always_visible": True},
   ),

   #text to describe the slider's current selections. updates in real time with user input.
   html.Div(
    id='slider-text',
    style={
        "color": "white",
        "fontFamily": "Helvetica",
        "fontSize": "12px",
        "fontStyle": "italic",
        "marginTop": "20px",
        "textAlign": "center"
    }
),

    #put the line graph in below the bar chart
        dcc.Graph(id='success-rate-over-time', figure=fig_success, style={"marginTop": "20px", "marginBottom": "100px", "height": "700px", "border": "2px solid #DFC5FE", "borderRadius": "10px"}),

#interactivity for pie chart
#dropdown filter for pie chart
html.Div([
    
    #dropdown placed above the pie chart
    dcc.Dropdown(
        id='pie-company-dropdown',
        options=[{'label': c, 'value': c} for c in sorted(data['Company'].unique())],
        value=None,  #should default to all companies being shown.
        placeholder="Select a company for the pie chart",
        multi=False,
        style={
            "color": "black",
            "backgroundColor": "#DFC5FE",
            "fontFamily": "Helvetica",
            "fontSize": "14px",
            "width": "260px", #width of dropdown - note to self adjust as needed with respect to placeholder text
            "marginBottom": "20px",
            "marginTop": "50px"
           
        }
    ),

    #pie chart container with lavender border
    html.Div([
        dcc.Graph(
            id="outcome-pie",
            style={
                "marginTop": "20px",
                "marginBottom": "40px",
                "height": "600px",
                "border": "2px solid #DFC5FE",
                "borderRadius": "10px",
                "paddingTop": "30px",
                "paddingBottom": "20px",
                "paddingLeft": "20px",
                "paddingRight": "20px"
            }
        )
    ])

], style={
    "marginTop": "30px",
    "marginBottom": "80px"
}),

#dropdown for stacked bar chart
dcc.Dropdown(
    id='stacked-bar-company-dropdown',
    options=[{'label': c, 'value': c} for c in sorted(data['Company'].unique())],
    value=None,  #default should be all companies displayed
    placeholder="Select one or more companies for the stacked bar chart",
    multi=True,
    style={
        "color": "black",
        "backgroundColor": "#DFC5FE",
        "fontFamily": "Helvetica",
        "fontSize": "14px",
        "marginBottom": "20px",
        "marginTop": "50px",
        "display": "block",
        "marginLeft": "auto",
        "marginRight": "auto" #width of entire screen, since it has the option to select multiple at once. needs more room.
    }
),
 #put the stacked bar chart in below the pie chart
        dcc.Graph(
            id='missions-stacked-bar',
            figure=fig_stacked,
            style={"marginTop": "20px", "marginBottom": "50px", "height": "700px", 
                "border": "2px solid #DFC5FE", "borderRadius": "10px"}
)

    ], #final closing bracket for html.Div -------------------------------------------------------------------------------------
    
    #main style for the entire dashboard
    style={
        "backgroundColor": "#1e1e1e",  #dark gray? space theme?
        "color": "white", 
        "padding": "20px"
    }
)
#callback for interactivity of line graph
@app.callback(
    Output('success-rate-over-time', 'figure'),
    Input('line-company-dropdown', 'value'),
    Input('year-range-slider', 'value')
)
def update_success_chart(selected_company, selected_years):
    filtered_data = data.copy()
    if selected_company:
        filtered_data = filtered_data[filtered_data['Company'] == selected_company]
    
    filtered_data = filtered_data[
        (filtered_data['Year'] >= selected_years[0]) &
        (filtered_data['Year'] <= selected_years[1])
    ]
    
    success_rate_per_year = (
        filtered_data.groupby('Year')['MissionStatus']
        .apply(lambda x: (x == 'Success').sum() / len(x) * 100)
        .reset_index(name='SuccessRate')
    )
    
    fig = px.line(
        success_rate_per_year,
        x='Year',
        y='SuccessRate',
        markers=True,
        title='Mission Success Rate Through the Years'
    )
    
    fig.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font_color='white',
        title={"text": "Mission Success Rate Through the Years", "x": 0.5,
               "font":{"family":"Helvetica","size":24,"color":"white"}},
        xaxis=dict(title="Year",
                   title_font=dict(family='Helvetica', size=20, color='white'),
                   tickfont=dict(family='Helvetica', size=14, color='white')),
        yaxis=dict(title="Success Rate (%)",
                   title_font=dict(family='Helvetica', size=20, color='white'),
                   tickfont=dict(family='Helvetica', size=14, color='white'))
    )
    
    fig.update_traces(
    line=dict(color='#DFC5FE', width=2),
    marker=dict(color='#DFC5FE', size=8)
)
    return fig

#callback for updating the slider text below the year range slider
@app.callback(
    Output('slider-text', 'children'),
    Input('year-range-slider', 'value'),
    Input('line-company-dropdown', 'value')  # add this input
)
def update_slider_text(year_range, selected_company):
    start_year, end_year = year_range

    #determine company text depending on what the user has selected in the dropdown menu above it.
    if selected_company:
        company_text = selected_company
    else:
        company_text = "all companies"

    return f"Now showing mission success rate from {start_year} to {end_year} for {company_text}."

#callback for pie chart, as well as creation of pie chart
@app.callback(
    Output("outcome-pie", "figure"),
    Input("pie-company-dropdown", "value")
)
def update_pie(selected_company):
    #begin with full dataset to be filtered
    df_filtered = data.copy()

    #filter by company if a specific one is selected
    if selected_company and selected_company != "All":
        df_filtered = df_filtered[df_filtered["Company"] == selected_company]

    #count outcomes
    outcome_counts = df_filtered["MissionStatus"].value_counts().reset_index()
    outcome_counts.columns = ["Outcome", "Count"]

    #pie chart
    fig = px.pie(
        outcome_counts,
        names="Outcome",
        values="Count",
        hole=0.4  # donut style
    )

    #color mapping to each status, custom colors since they're nicer.
    color_map = {
        "Success": "#6FCF97",        
        "Failure": "#EB5757",        
        "Partial Failure": "#F2C94C",
        "Prelaunch Failure": "#B77A50" 
    }

    fig.update_traces(
        textinfo="percent+label",
        marker=dict(colors=[color_map.get(o, "#DFC5FE") for o in outcome_counts["Outcome"]]),
        pull=[0.05] * len(outcome_counts)
    )

    fig.update_layout(
        title={"text": "Mission Outcome Breakdown",
                "x": 0.5,
                "y": 0.9999,
                "font": {"family": "Helvetica", "size": 26, "color": "white"}},
        font=dict(family="Helvetica", size=14, color="white"),
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return fig

#callback for stacked bar chart, interactivity

@app.callback(
    Output('missions-stacked-bar', 'figure'),
    Input('stacked-bar-company-dropdown', 'value')
)
def update_stacked_bar(selected_companies):
    #if nothing is selected then show all companies by default.
    if not selected_companies or 'All' in selected_companies:
        filtered_data = data.copy()
    else:
        #filter for multiple selected companies, multi = True
        filtered_data = data[data['Company'].isin(selected_companies)]
    
    #group by 'Company' and 'MissionStatus'
    missions_by_company_outcome = (
        filtered_data.groupby(['Company', 'MissionStatus'])
        .size()
        .reset_index(name='Count')
    )

    #same pie chart colors. very clean.
    color_map = {
        "Success": "#6FCF97",
        "Failure": "#EB5757",
        "Partial Failure": "#F2C94C",
        "Prelaunch Failure": "#B77A50"
    }

    fig_stacked = px.bar(
        missions_by_company_outcome,
        x='Company',
        y='Count',
        color='MissionStatus',
        color_discrete_map=color_map,
        text='Count',
        title='Missions by Company and Outcome'
    )

    fig_stacked.update_layout(
        barmode='stack',
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font_color='white',
        title={"text": "Missions by Company and Outcome", "x": 0.5,
               "font": {"family": "Helvetica", "size": 24, "color": "white"}},
        xaxis=dict(title="Company",
                   title_font=dict(family='Helvetica', size=20, color='white'),
                   tickfont=dict(family='Helvetica', size=14, color='white')),
        yaxis=dict(title="Missions",
                   title_font=dict(family='Helvetica', size=20, color='white'),
                   tickfont=dict(family='Helvetica', size=14, color='white')),
        legend=dict(title="Mission Outcome", font=dict(family="Helvetica", size=12, color="white"))
    )

    return fig_stacked

#run the app :)

if __name__ == "__main__":
    app.run(debug=True)
