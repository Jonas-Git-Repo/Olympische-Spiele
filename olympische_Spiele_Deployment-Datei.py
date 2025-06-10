import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output
import gzip
import pickle

# Dash initialisieren
app = dash.Dash(__name__)
server = app.server

# Farben & Zeiträume
medal_colors = {'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32', 'Alle': '#8888FF'}
time_periods = {
    'Gesamt (1896–2016)': (1896, 2016),
    '1896–1936': (1896, 1936),
    '1948–1992': (1948, 1992),
    '1994–2016': (1994, 2016)
}

# Pickle-Datei laden (komprimiert)
with gzip.open("athlete_events.pkl.gz", "rb") as f:
    athlete_events = pickle.load(f)

region_options = [{'label': r, 'value': r} for r in sorted(athlete_events['region'].dropna().unique())]

# Layout mit Tabs
app.layout = html.Div([
    html.H1("🏅 Olympische Spiele Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Zeitraum:"),
        dcc.Dropdown(
            id='period-dropdown',
            options=[{'label': k, 'value': k} for k in time_periods],
            value='Gesamt (1896–2016)'
        ),
        html.Label("Saison:"),
        dcc.Dropdown(
            id='season-dropdown',
            options=[{'label': '☀️ Sommer', 'value': 'Summer'}, {'label': '❄️ Winter', 'value': 'Winter'}],
            value='Summer'
        ),
        html.Label("Land (einzeln):"),
        dcc.Dropdown(id='country-dropdown', options=region_options, value='Germany'),
        html.Label("Sportart:"),
        dcc.Dropdown(id='sport-dropdown', value='Alle'),
        html.Label("Geschlecht:"),
        dcc.Dropdown(
            id='gender-dropdown',
            options=[{'label': '👥 Alle', 'value': 'Alle'}, {'label': '👨 Männer', 'value': 'M'}, {'label': '👩 Frauen', 'value': 'F'}],
            value='Alle'
        ),
        html.Label("Länder (mehrfach):"),
        dcc.Dropdown(
            id='multi-country-dropdown',
            options=region_options,
            value=['Germany', 'USA'],
            multi=True
        ),
        html.Label("Medaillentyp:"),
        dcc.Dropdown(
            id='medal-dropdown',
            options=[{'label': m, 'value': m} for m in ['Alle', 'Gold', 'Silver', 'Bronze']],
            value='Alle'
        ),
    ], style={'columnCount': 2}),

    dcc.Tabs([
        dcc.Tab(label='🏅 Einzelvergleich', children=[
            dcc.Graph(id='medals-chart')
        ]),
        dcc.Tab(label='🔥 Heatmap', children=[
            dcc.Graph(id='heatmap-chart')
        ]),
        dcc.Tab(label='🌍 Ländervergleich', children=[
            dcc.Graph(id='country-comparison-chart')
        ])
    ])
])

# Dropdown: Sportarten aktualisieren
@app.callback(
    Output('sport-dropdown', 'options'),
    Input('season-dropdown', 'value')
)
def update_sport_options(season):
    sports = athlete_events[athlete_events['season'] == season]['sport'].dropna().unique()
    return [{'label': '🏆 Alle Sportarten', 'value': 'Alle'}] + [{'label': s, 'value': s} for s in sorted(sports)]

# Chart: Medaillen Barplot (Einzelland)
@app.callback(
    Output('medals-chart', 'figure'),
    Input('period-dropdown', 'value'),
    Input('season-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('sport-dropdown', 'value'),
    Input('gender-dropdown', 'value')
)
def update_medals_chart(period, season, country, sport, gender):
    start, end = time_periods[period]
    df = athlete_events[
        (athlete_events['year'].between(start, end)) &
        (athlete_events['season'] == season) &
        (athlete_events['region'] == country) &
        (athlete_events['medal'].notna())
    ]
    if sport != 'Alle':
        df = df[df['sport'] == sport]
    if gender != 'Alle':
        df = df[df['sex'] == gender]
    if df.empty:
        return go.Figure().add_annotation(text="⚠️ Keine Daten verfügbar", x=0.5, y=0.5, showarrow=False)

    count = df.groupby(['year', 'medal']).size().unstack(fill_value=0)
    fig = go.Figure()
    for m in ['Bronze', 'Silver', 'Gold']:
        if m in count:
            fig.add_trace(go.Bar(x=count.index, y=count[m], name=m, marker_color=medal_colors[m]))
    fig.update_layout(
        barmode='stack',
        title=f"{country} – {sport if sport != 'Alle' else 'alle Sportarten'} ({season}, {period})",
        xaxis_title='Jahr', yaxis_title='Medaillen'
    )
    return fig

# Chart: Heatmap
@app.callback(
    Output('heatmap-chart', 'figure'),
    Input('period-dropdown', 'value'),
    Input('season-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('gender-dropdown', 'value')
)
def update_heatmap(period, season, country, gender):
    start, end = time_periods[period]
    df = athlete_events[
        (athlete_events['year'].between(start, end)) &
        (athlete_events['season'] == season) &
        (athlete_events['region'] == country) &
        (athlete_events['medal'].notna())
    ]
    if gender != 'Alle':
        df = df[df['sex'] == gender]
    if df.empty:
        return go.Figure().add_annotation(text="⚠️ Keine Daten verfügbar", x=0.5, y=0.5, showarrow=False)

    matrix = df.groupby(['sport', 'year']).size().unstack(fill_value=0)
    fig = go.Figure(data=go.Heatmap(
        z=matrix.values, x=matrix.columns, y=matrix.index,
        colorscale='YlOrBr', colorbar=dict(title='Medaillen')
    ))
    fig.update_layout(
        title=f"Heatmap – {country} ({season}, {period})",
        xaxis_title='Jahr', yaxis_title='Sportart'
    )
    return fig

# Chart: Mehrere Länder im Vergleich
@app.callback(
    Output('country-comparison-chart', 'figure'),
    Input('period-dropdown', 'value'),
    Input('season-dropdown', 'value'),
    Input('multi-country-dropdown', 'value'),
    Input('medal-dropdown', 'value'),
    Input('gender-dropdown', 'value')
)
def update_country_comparison(period, season, countries, medal_type, gender):
    start, end = time_periods[period]
    df = athlete_events[
        (athlete_events['year'].between(start, end)) &
        (athlete_events['season'] == season) &
        (athlete_events['region'].isin(countries)) &
        (athlete_events['medal'].notna())
    ]
    if gender != 'Alle':
        df = df[df['sex'] == gender]
    if medal_type != 'Alle':
        df = df[df['medal'] == medal_type]
    if df.empty:
        return go.Figure().add_annotation(text="⚠️ Keine Medaillendaten für diese Auswahl", x=0.5, y=0.5, showarrow=False)

    counts = df.groupby('region').size().reindex(countries, fill_value=0)
    fig = go.Figure(data=[go.Bar(
        x=counts.index,
        y=counts.values,
        marker_color=medal_colors[medal_type],
        text=counts.values,
        textposition='auto'
    )])
    fig.update_layout(
        title=f"Medaillenvergleich ({medal_type}) – {season} {period}" + (f", Geschlecht: {gender}" if gender != 'Alle' else ""),
        xaxis_title="Land", yaxis_title="Anzahl Medaillen"
    )
    return fig

# App starten
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)





