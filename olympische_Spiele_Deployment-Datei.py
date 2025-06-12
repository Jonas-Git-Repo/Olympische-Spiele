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

# Übersetzungstabelle Deutsch <-> Englisch für Sportarten
# Diese kannst du beliebig erweitern/ändern!
sport_translation = {
    'Aquatics': 'Wassersport',
    'Athletics': 'Leichtathletik',
    'Basketball': 'Basketball',
    'Boxing': 'Boxen',
    'Cycling': 'Radsport',
    'Fencing': 'Fechten',
    'Football': 'Fußball',
    'Gymnastics': 'Turnen',
    'Hockey': 'Hockey',
    'Rowing': 'Rudern',
    'Sailing': 'Segeln',
    'Shooting': 'Schießen',
    'Tennis': 'Tennis',
    'Weightlifting': 'Gewichtheben',
    'Wrestling': 'Ringen',
    # ... weitere Zuordnungen ...
}

# Rückwärts-Lookup für Deutsch -> Englisch
sport_translation_de_to_en = {v: k for k, v in sport_translation.items()}

# Sportarten-Liste für Dropdowns (übersetzt)
unique_sports_en = sorted(athlete_events['sport'].dropna().unique())
unique_sports_de = [
    sport_translation.get(s, s) for s in unique_sports_en
]
sport_options = [{'label': '🏆 Alle Sportarten', 'value': 'Alle'}] + [
    {'label': de, 'value': de} for de in unique_sports_de
]

region_options = [{'label': r, 'value': r} for r in sorted(athlete_events['region'].dropna().unique())]

# Layout
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
        dcc.Dropdown(id='sport-dropdown', options=sport_options, value='Alle'),
        html.Label("Geschlecht:"),
        dcc.Dropdown(
            id='gender-dropdown',
            options=[{'label': '👥 Alle', 'value': 'Alle'}, {'label': '👨 Männer', 'value': 'M'}, {'label': '👩 Frauen', 'value': 'F'}],
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
            html.Div(id="country-comparison-filters", children=[
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
                )
            ], style={'columnCount': 2, 'marginBottom': '20px'}),
            dcc.Graph(id='country-comparison-chart')
        ]),
    ]),

    # Faktenbereich zu Sportarten (unterhalb der Dashboards)
    html.H2("Fakten zu den Sportarten", style={'marginTop': '40px'}),
    html.Label("Wähle eine Sportart:"),
    dcc.Dropdown(
        id='sportart-fakten-dropdown',
        options=sport_options,
        value=sport_options[1]['value'],  # erste echte Sportart als Default
        clearable=False,
        style={'width': '60%'}
    ),
    html.Div(id='sportart-fakten-output', style={'fontSize': '18px', 'marginTop': '20px'})
])

# Sportarten-Dropdowns synchronisieren (bei Saisonwechsel)
@app.callback(
    Output('sport-dropdown', 'options'),
    Output('sport-dropdown', 'value'),
    Output('sportart-fakten-dropdown', 'options'),
    Output('sportart-fakten-dropdown', 'value'),
    Input('season-dropdown', 'value'),
    prevent_initial_call=False
)
def update_sport_options(season):
    sports_en = sorted(athlete_events[athlete_events['season'] == season]['sport'].dropna().unique())
    sports_de = [
        sport_translation.get(s, s) for s in sports_en
    ]
    options = [{'label': '🏆 Alle Sportarten', 'value': 'Alle'}] + [
        {'label': de, 'value': de} for de in sports_de
    ]
    # Default auf "Alle" und erste echte Sportart
    value_dropdown = 'Alle'
    value_fakten = sports_de[0] if sports_de else 'Alle'
    return options, value_dropdown, options, value_fakten

# Medaillen-Barplot (Einzelland)
@app.callback(
    Output('medals-chart', 'figure'),
    Input('period-dropdown', 'value'),
    Input('season-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('sport-dropdown', 'value'),
    Input('gender-dropdown', 'value')
)
def update_medals_chart(period, season, country, sport_de, gender):
    start, end = time_periods[period]
    df = athlete_events[
        (athlete_events['year'].between(start, end)) &
        (athlete_events['season'] == season) &
        (athlete_events['region'] == country) &
        (athlete_events['medal'].notna())
    ]
    # Übersetze die ausgewählte Sportart zurück ins Englische für die Filterung
    if sport_de != 'Alle':
        sport_en = sport_translation_de_to_en.get(sport_de, sport_de)
        df = df[df['sport'] == sport_en]
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
        title=f"{country} – {sport_de if sport_de != 'Alle' else 'alle Sportarten'} ({season}, {period})",
        xaxis_title='Jahr',
        yaxis_title='Medaillen',
        yaxis=dict(tickformat=".0f")
    )
    return fig

# Heatmap
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
    # Sportarten auf Deutsch für die Heatmap
    matrix = df.copy()
    matrix['sport_de'] = matrix['sport'].map(lambda x: sport_translation.get(x, x))
    mat = matrix.groupby(['sport_de', 'year']).size().unstack(fill_value=0)
    fig = go.Figure(data=go.Heatmap(
        z=mat.values, x=mat.columns, y=mat.index,
        colorscale='YlOrBr',
        colorbar=dict(title='Medaillen'),
        hovertemplate='Disziplin: %{y}<br>Jahr: %{x}<br>Anzahl: %{z}<extra></extra>'
    ))
    fig.update_layout(
        title=f"Heatmap – {country} ({season}, {period})",
        xaxis_title='Jahr',
        yaxis_title='Sportart'
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
        xaxis_title="Land",
        yaxis_title="Anzahl Medaillen",
        yaxis=dict(tickformat=".0f")
    )
    return fig

# Fakten zu Sportarten
@app.callback(
    Output('sportart-fakten-output', 'children'),
    Input('sportart-fakten-dropdown', 'value'),
    Input('season-dropdown', 'value')
)
def sportart_fakten(sportart_de, season):
    # Übersetze zurück ins Englische für Filterung
    if sportart_de == 'Alle':
        return html.Div("Bitte eine konkrete Sportart auswählen.")
    sport_en = sport_translation_de_to_en.get(sportart_de, sportart_de)
    df = athlete_events[(athlete_events['sport'] == sport_en) & (athlete_events['season'] == season)]
    if df.empty:
        return html.Div("Keine Daten für diese Kombination.")
    austragungen = df['year'].nunique()
    first_year = df['year'].min()
    last_year = df['year'].max()
    teilnahmen_athlet = df.groupby('name').size()
    if not teilnahmen_athlet.empty:
        top_athlet = teilnahmen_athlet.idxmax()
        top_athlet_count = teilnahmen_athlet.max()
    else:
        top_athlet = "Keine Daten"
        top_athlet_count = 0
    teilnahmen_land = df.groupby('region').size()
    if not teilnahmen_land.empty:
        top_land = teilnahmen_land.idxmax()
        top_land_count = teilnahmen_land.max()
    else:
        top_land = "Keine Daten"
        top_land_count = 0
    unique_athletes = df['name'].nunique()
    unique_countries = df['region'].nunique()
    if 'event' in df.columns:
        top_event = df['event'].value_counts().idxmax()
        top_event_count = df['event'].value_counts().max()
    else:
        top_event = "Keine Daten"
        top_event_count = 0

    return html.Div([
        html.H4(f"Fakten zur Sportart: {sportart_de} ({season})"),
        html.Ul([
            html.Li(f"Anzahl der Olympischen Spiele mit {sportart_de}: {austragungen} ({first_year}–{last_year})"),
            html.Li(f"Meistteilnehmender Sportler: {top_athlet} ({top_athlet_count} Teilnahmen)"),
            html.Li(f"Land mit den meisten Teilnahmen: {top_land} ({top_land_count} Teilnahmen)"),
            html.Li(f"Anzahl verschiedener Athleten: {unique_athletes}"),
            html.Li(f"Anzahl teilnehmender Länder: {unique_countries}"),
            html.Li(f"Häufigste Disziplin: {top_event} ({top_event_count} Teilnahmen)")
        ])
    ])

# App starten
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
