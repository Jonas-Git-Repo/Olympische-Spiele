import pandas as pd
import plotly.graph_objects as go
import dash
import gzip
import pickle
from dash import dcc, html, Input, Output
import os

medal_colors = {'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'}
time_periods = {
    '1896–1936': (1896, 1936),
    '1948–1992': (1948, 1992),
    '1994–2016': (1994, 2016)
}

app = dash.Dash(__name__)
server = app.server  # Wichtig für Deployment!

with gzip.open("athlete_events.pkl.gz", "rb") as f:
    athlete_events = pickle.load(f)

region_options = [{'label': region, 'value': region} 
                 for region in sorted(athlete_events['region'].dropna().unique())]

app.layout = html.Div([
    html.Div([
        html.H1("🏅 Olympische Medaillen Dashboard", 
                style={'textAlign': 'center', 'marginBottom': 10, 'color': '#2c3e50', 'fontSize': '2.5em'}),
        html.P("Interaktive Analyse der olympischen Medaillen", 
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '1.2em', 'marginBottom': 30})
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': 30}),
    
    html.Div([
        html.H3("🔍 Filter", style={'marginBottom': 20, 'color': '#34495e'}),
        
        html.Div([
            html.Div([
                html.Label("Zeitraum:", style={'fontWeight': 'bold', 'fontSize': '14px', 'marginBottom': '5px', 'display': 'block'}),
                dcc.Dropdown(
                    id='period-dropdown',
                    options=[{'label': k, 'value': k} for k in time_periods.keys()],
                    value=list(time_periods.keys())[2],
                    style={'fontSize': '12px'}
                )
            ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
            
            html.Div([
                html.Label("Saison:", style={'fontWeight': 'bold', 'fontSize': '14px', 'marginBottom': '5px', 'display': 'block'}),
                dcc.Dropdown(
                    id='season-dropdown',
                    options=[
                        {'label': '☀️ Sommer', 'value': 'Summer'},
                        {'label': '❄️ Winter', 'value': 'Winter'}
                    ],
                    value='Summer',
                    style={'fontSize': '12px'}
                )
            ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
            
            html.Div([
                html.Label("Land:", style={'fontWeight': 'bold', 'fontSize': '14px', 'marginBottom': '5px', 'display': 'block'}),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=region_options,
                    value=region_options[0]['value'] if region_options else 'Germany',
                    style={'fontSize': '12px'}
                )
            ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
            
            html.Div([
                html.Label("Sportart:", style={'fontWeight': 'bold', 'fontSize': '14px', 'marginBottom': '5px', 'display': 'block'}),
                dcc.Dropdown(
                    id='sport-dropdown',
                    value='Alle',
                    style={'fontSize': '12px'}
                )
            ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
            
            html.Div([
                html.Label("Geschlecht:", style={'fontWeight': 'bold', 'fontSize': '14px', 'marginBottom': '5px', 'display': 'block'}),
                dcc.Dropdown(
                    id='gender-dropdown',
                    options=[
                        {'label': '👥 Alle', 'value': 'Alle'},
                        {'label': '👨 Männer', 'value': 'M'},
                        {'label': '👩 Frauen', 'value': 'F'}
                    ],
                    value='Alle',
                    style={'fontSize': '12px'}
                )
            ], style={'width': '19%', 'display': 'inline-block'})
        ])
    ], style={'marginBottom': 30, 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'}),
    
    html.Div([
        dcc.Graph(id='medals-chart', style={'height': '600px'})
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'}),
    
    html.Div([
        html.Hr(),
        html.P([
            "📊 Olympische Medaillen Dashboard | ",
            html.A("Datenquelle: Olympics Dataset", href="#", style={'color': '#3498db'})
        ], style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '12px', 'marginTop': 30})
    ])
    
], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px', 'fontFamily': 'Arial, sans-serif'})

@app.callback(
    Output('sport-dropdown', 'options'),
    Input('season-dropdown', 'value')
)
def update_sport_options(selected_season):
    sports_for_season = athlete_events[
        athlete_events['season'] == selected_season
    ]['sport'].dropna().unique()
    options = [{'label': '🏆 Alle Sportarten', 'value': 'Alle'}] + \
             [{'label': sport, 'value': sport} for sport in sorted(sports_for_season)]
    return options

@app.callback(
    Output('medals-chart', 'figure'),
    [Input('period-dropdown', 'value'),
     Input('season-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('sport-dropdown', 'value'),
     Input('gender-dropdown', 'value')]
)
def update_chart(period_label, season, country, sport, gender):
    start, end = time_periods[period_label]
    df_filtered = athlete_events[
        (athlete_events['year'].between(start, end)) &
        (athlete_events['season'] == season) &
        (athlete_events['medal'].notna()) &
        (athlete_events['region'] == country)
    ]
    
    if sport != 'Alle':
        df_filtered = df_filtered[df_filtered['sport'] == sport]
    if gender != 'Alle':
        df_filtered = df_filtered[df_filtered['sex'] == gender]
    
    fig = go.Figure()
    
    if df_filtered.empty:
        fig.add_annotation(
            text=f"⚠️ Keine Medaillen für {country}<br>in {sport} ({season} {period_label})<br>Geschlecht: {gender}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, 
            font=dict(size=18, color='#e74c3c'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#e74c3c',
            borderwidth=2
        )
    else:
        medals_per_year = (
            df_filtered
            .groupby(['year', 'medal'])
            .size()
            .unstack(fill_value=0)
            .sort_index()
        )
        
        for medal in ['Bronze', 'Silver', 'Gold']:
            if medal in medals_per_year.columns:
                fig.add_trace(go.Bar(
                    name=f"{medal} ({medals_per_year[medal].sum()})",
                    x=medals_per_year.index,
                    y=medals_per_year[medal],
                    marker_color=medal_colors[medal],
                    hovertemplate=f'<b>{medal}</b><br>Jahr: %{{x}}<br>Anzahl: %{{y}}<br><extra></extra>'
                ))
    
    titel_sport = "alle Sportarten" if sport == "Alle" else sport
    titel_geschlecht = {"Alle": "", "M": " – Männer", "F": " – Frauen"}[gender]
    
    fig.update_layout(
        title={
            'text': f"{country} – {titel_sport}{titel_geschlecht}<br><sub>{season} {period_label}</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title='Jahr',
        yaxis_title='Anzahl Medaillen',
        barmode='stack',
        template='plotly_white',
        font=dict(size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)


# In[ ]:





