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

# Sportarten-Übersetzung (alle aus dem Datensatz)
unique_sports_en = sorted(athlete_events['sport'].dropna().unique())
# Individuelle Übersetzung aller Sportarten – bitte ggf. ergänzen/überarbeiten!
sport_translation = {
    'Alpinism': 'Alpinismus',
    'Aeronautics': 'Luftfahrt',
    'Aquatics': 'Wassersport',
    'Archery': 'Bogenschießen',
    'Athletics': 'Leichtathletik',
    'Badminton': 'Badminton',
    'Baseball': 'Baseball',
    'Basketball': 'Basketball',
    'Boxing': 'Boxen',
    'Canoeing': 'Kanu',
    'Cricket': 'Cricket',
    'Cross Country Skiing': 'Skilanglauf',
    'Curling': 'Curling',
    'Cycling': 'Radsport',
    'Diving': 'Wasserspringen',
    'Equestrianism': 'Reitsport',
    'Fencing': 'Fechten',
    'Figure Skating': 'Eiskunstlauf',
    'Football': 'Fußball',
    'Freestyle Skiing': 'Freestyle Skiing',
    'Golf': 'Golf',
    'Gymnastics': 'Turnen',
    'Handball': 'Handball',
    'Hockey': 'Hockey',
    'Ice Hockey': 'Eishockey',
    'Judo': 'Judo',
    'Lacrosse': 'Lacrosse',
    'Luge': 'Rodeln',
    'Modern Pentathlon': 'Moderner Fünfkampf',
    'Rhythmic Gymnastics': 'Rhythmische Sportgymnastik',
    'Rowing': 'Rudern',
    'Rugby': 'Rugby',
    'Sailing': 'Segeln',
    'Shooting': 'Schießen',
    'Short Track Speed Skating': 'Shorttrack',
    'Skeleton': 'Skeleton',
    'Ski Jumping': 'Skispringen',
    'Snowboarding': 'Snowboard',
    'Softball': 'Softball',
    'Speed Skating': 'Eisschnelllauf',
    'Swimming': 'Schwimmen',
    'Synchronized Swimming': 'Synchronschwimmen',
    'Table Tennis': 'Tischtennis',
    'Taekwondo': 'Taekwondo',
    'Tennis': 'Tennis',
    'Trampolining': 'Trampolinturnen',
    'Triathlon': 'Triathlon',
    'Tug-Of-War': 'Tauziehen',
    'Volleyball': 'Volleyball',
    'Water Polo': 'Wasserball',
    'Weightlifting': 'Gewichtheben',
    'Wrestling': 'Ringen',
    'Alpine Skiing': 'Ski Alpin',
    'Biathlon': 'Biathlon',
    'Bobsleigh': 'Bob',
    'Nordic Combined': 'Nordische Kombination',
    'Polo': 'Polo',
    'Rugby Sevens': 'Rugby Siebener',
    'Rugby Union': 'Rugby Union',
    'Art Competitions': 'Kunstwettbewerbe',
    'Basque Pelota': 'Pelota',
    'Military Ski Patrol': 'Militärpatrouille',
    'Motorboating': 'Motorbootsport',
    'Mountain Biking': 'Mountainbike',
    'Racquets': 'Rackets',
    'Roque': 'Roque',
    'Speed Skating': 'Eisschnelllauf',
    'Croquet': 'Krocket',
    'Jeu De Paume': 'Jeu de Paume',
    'Softball': 'Softball',
    'Tennis': 'Tennis',
    # ... ggf. weitere aus athlete_events['sport'].unique() ergänzen ...
}
# Rückwärts-Lookup
sport_translation_de_to_en = {v: k for k, v in sport_translation.items()}

# Länder-Übersetzung (Beispiel: nur ein kleiner Auszug, bitte ggf. mit vollständiger ISO-Liste ersetzen)
country_translation = {
    "Albania": "Albanien",
    "Algeria": "Algerien",
    "American Samoa": "Amerikanisch-Samoa",
    "Antigua": "Antigua und Barbuda",
    "Argentina": "Argentinien",
    "Armenia": "Armenien",
    "Australia": "Australien",
    "Austria": "Österreich",
    "Azerbaijan": "Aserbaidschan",
    "Bangladesh": "Bangladesch",
    "Belgium": "Belgien",
    "Boliva": "Bolivien",
    "Bosnia and Herzegovina": "Bosnien und Herzegowina",
    "Botswana": "Botswana",
    "Brazil": "Brasilien",
    "Bulgaria": "Bulgarien",
    "Cambodia": "Kambodscha",
    "Cameroon": "Kamerun",
    "Canada": "Kanada",
    "Cape Verde": "Kap Verde",
    "Cayman Islands": "Kaimaninseln",
    "Central African Republic": "Zentralafrikanische Republik",
    "Chad": "Tschad",
    "Colombia": "Kolumbien",
    "Comoros": "Komoren",
    "Cook Islands": "Cookinseln",
    "Croatia": "Kroatien",
    "Cuba": "Kuba",
    "Curacao": "Curaçao",
    "Cyprus": "Zypern",
    "Czech Republic": "Tschechien",
    "Democratic Republic of the Congo": "Demokratische Republik Kongo",
    "Denmark": "Dänemark",
    "Djibouti": "Dschibuti",
    "Dominican Republic": "Dominikanische Republik",
    "Egypt": "Ägypten",
    "Equatorial Guinea": "Äquatorialguinea",
    "Estonia": "Estland",
    "Ethiopia": "Äthiopien",
    "Fiji": "Fidschi",
    "Finland": "Finnland",
    "France": "Frankreich",
    "Gabon": "Gabun",
    "Georgia": "Georgien",
    "Germany": "Deutschland",
    "Greece": "Griechenland",
    "Hungary": "Ungarn",
    "Iceland": "Island",
    "India": "Indien",
    "Individual Olympic Athletes": "Einzelne Olympische Athleten",
    "Indonesia": "Indonesien",
    "Iraq": "Irak",
    "Ireland": "Irland",
    "Italy": "Italien",
    "Ivory Coast": "Elfenbeinküste",
    "Jamaica": "Jamaika",
    "Jordan": "Jordanien",
    "Kazakhstan": "Kasachstan",
    "Kenya": "Kenia",
    "Kyrgyzstan": "Kirgisistan",
    "Latvia": "Lettland",
    "Lebanon": "Libanon",
    "Libya": "Libyen",
    "Lithuania": "Litauen",
    "Luxembourg": "Luxemburg",
    "Macedonia": "Nordmazedonien",
    "Madagascar": "Madagaskar",
    "Maldives": "Malediven",
    "Marshall Islands": "Marshallinseln",
    "Mauritania": "Mauretanien",
    "Mexico": "Mexiko",
    "Micronesia": "Mikronesien",
    "Moldova": "Moldau",
    "Mongolia": "Mongolei",
    "Morocco": "Marokko",
    "Mozambique": "Mosambik",
    "Netherlands": "Niederlande",
    "New Zealand": "Neuseeland",
    "North Korea": "Nordkorea",
    "Norway": "Norwegen",
    "Palestine": "Palästina",
    "Papua New Guinea": "Papua-Neuguinea",
    "Philippines": "Philippinen",
    "Poland": "Polen",
    "Qatar": "Katar",
    "Republic of Congo": "Republik Kongo",
    "Romania": "Rumänien",
    "Russia": "Russland",
    "Rwanda": "Ruanda",
    "Saint Kitts": "St. Kitts und Nevis",
    "Saint Lucia": "St. Lucia",
    "Saint Vincent": "St. Vincent und die Grenadinen",
    "Sao Tome and Principe": "São Tomé und Príncipe",
    "Saudi Arabia": "Saudi-Arabien",
    "Serbia": "Serbien",
    "Seychelles": "Seychellen",
    "Slovakia": "Slowakei",
    "Slovenia": "Slowenien",
    "Solomon Islands": "Salomonen",
    "South Africa": "Südafrika",
    "South Korea": "Südkorea",
    "South Sudan": "Südsudan",
    "Spain": "Spanien",
    "Swaziland": "Eswatini",
    "Sweden": "Schweden",
    "Switzerland": "Schweiz",
    "Syria": "Syrien",
    "Tajikistan": "Tadschikistan",
    "Tanzania": "Tansania",
    "Timor-Leste": "Osttimor",
    "Trinidad": "Trinidad und Tobago",
    "Tunisia": "Tunesien",
    "Turkey": "Türkei",
    "UK": "Vereinigtes Königreich",
    "United Arab Emirates": "Vereinigte Arabische Emirate",
    "Uzbekistan": "Usbekistan",
    "Virgin Islands, British": "Britische Jungferninseln",
    "Virgin Islands, US": "Amerikanische Jungferninseln",
    "Yemen": "Jemen",
    "Zambia": "Sambia",
    "Zimbabwe": "Simbabwe",
}
country_translation_de_to_en = {v: k for k, v in country_translation.items()}

# Sportarten und Länder auf Deutsch für Dropdowns
unique_sports_de = [sport_translation.get(s, s) for s in unique_sports_en]
sport_options = [{'label': '🏆 Alle Sportarten', 'value': 'Alle'}] + [
    {'label': de, 'value': de} for de in unique_sports_de
]
unique_countries_en = sorted(athlete_events['region'].dropna().unique())
unique_countries_de = [country_translation.get(c, c) for c in unique_countries_en]
region_options = [{'label': de, 'value': de} for de in unique_countries_de]

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
        dcc.Dropdown(id='sport-dropdown', options=[{'label': 'Alle', 'value': 'Alle'}] + sport_options, value='Alle'),
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
        ])
    ]),
    html.H2("Fakten zu Sportarten & Events", style={'marginTop': '40px'}),
    html.Div([
        html.Div([
            html.Label("Sportart:"),
            dcc.Dropdown(
                id='sportart-fakten-dropdown',
                options=[{'label': s, 'value': s} for s in unique_sports],
                value=unique_sports[0],
                clearable=False,
                style={'width': '95%'}
            ),
            html.Div(id='sportart-fakten-output', style={'fontSize': '18px', 'marginTop': '20px'}),
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        html.Div([
            html.Label("Disziplin (Event):"),
            dcc.Dropdown(
                id='event-dropdown',
                options=[],
                value=None,
                clearable=False,
                style={'width': '95%'}
            ),
            html.Div(id='event-fakten-output', style={'fontSize': '18px', 'marginTop': '20px'}),
        ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%', 'verticalAlign': 'top'}),
    ], style={'width': '100%', 'display': 'flex'}),
])

# Dropdown: Sportarten aktualisieren
@app.callback(
    Output('sport-dropdown', 'options'),
    Input('season-dropdown', 'value')
)
def update_sport_options(season):
    sports = athlete_events[athlete_events['season'] == season]['sport'].dropna().unique()
    return [{'label': 'Alle', 'value': 'Alle'}] + [{'label': s, 'value': s} for s in sorted(sports)]

# Event-Dropdown je nach gewählter Sportart aktualisieren
@app.callback(
    Output('event-dropdown', 'options'),
    Output('event-dropdown', 'value'),
    Input('sportart-fakten-dropdown', 'value')
)
def update_event_options(sport):
    if not sport or sport == "Alle":
        return [], None
    event_opts = get_event_options(sport)
    return event_opts, event_opts[0]['value'] if event_opts else ([], None)

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
        xaxis_title='Jahr',
        yaxis_title='Medaillen',
        yaxis=dict(tickformat=".0f")
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

@app.callback(
    Output('sportart-fakten-output', 'children'),
    Input('sportart-fakten-dropdown', 'value')
)
def sportart_fakten(sportart):
    df = athlete_events[athlete_events['sport'] == sportart]

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
        html.H4(f"Fakten zur Sportart: {sportart}"),
        html.Ul([
            html.Li(f"Anzahl der Olympischen Spiele mit {sportart}: {austragungen} ({first_year}–{last_year})"),
            html.Li(f"Meistteilnehmender Sportler: {top_athlet} ({top_athlet_count} Teilnahmen)"),
            html.Li(f"Land mit den meisten Teilnahmen: {top_land} ({top_land_count} Teilnahmen)"),
            html.Li(f"Anzahl verschiedener Athleten: {unique_athletes}"),
            html.Li(f"Anzahl teilnehmender Länder: {unique_countries}"),
            html.Li(f"Häufigste Disziplin: {top_event} ({top_event_count} Teilnahmen)")
        ])
    ])

@app.callback(
    Output('event-dropdown', 'options'),
    Output('event-dropdown', 'value'),
    Input('sportart-fakten-dropdown', 'value')
)
def update_event_dropdown(sportart):
    if not sportart:
        return [], None
    events = athlete_events[athlete_events['sport'] == sportart]['event'].dropna().unique()
    if len(events) == 0:
        return [], None
    return [{'label': e, 'value': e} for e in sorted(events)], sorted(events)[0]

@app.callback(
    Output('event-fakten-output', 'children'),
    Input('event-dropdown', 'value'),
    Input('sportart-fakten-dropdown', 'value')
)
def event_fakten(event, sportart):
    if not event or not sportart:
        return ""
    df = athlete_events[(athlete_events['sport'] == sportart) & (athlete_events['event'] == event)]
    if df.empty:
        return "Keine Daten für diese Disziplin."
    teilnehmer = df['name'].nunique()
    medals = df[df['medal'].notna()].groupby('name').size()
    if not medals.empty:
        top_medalist = medals.idxmax()
        top_medalist_count = medals.max()
    else:
        top_medalist = "Keine Daten"
        top_medalist_count = 0
    if df['height'].notna().any():
        groesster = df.loc[df['height'].idxmax()]
        groesster_name = groesster['name']
        groesster_value = groesster['height']
    else:
        groesster_name = "Keine Daten"
        groesster_value = "?"
    if df['height'].notna().any():
        kleinster = df.loc[df['height'].idxmin()]
        kleinster_name = kleinster['name']
        kleinster_value = kleinster['height']
    else:
        kleinster_name = "Keine Daten"
        kleinster_value = "?"
    if df['age'].notna().any():
        aeltester = df.loc[df['age'].idxmax()]
        aeltester_name = aeltester['name']
        aeltester_value = aeltester['age']
    else:
        aeltester_name = "Keine Daten"
        aeltester_value = "?"
    if df['age'].notna().any():
        juengster = df.loc[df['age'].idxmin()]
        juengster_name = juengster['name']
        juengster_value = juengster['age']
    else:
        juengster_name = "Keine Daten"
        juengster_value = "?"

    return html.Div([
        html.H4(f"Fakten zur Disziplin: {event}"),
        html.Ul([
            html.Li(f"Teilnehmerzahl (unique Athleten): {teilnehmer}"),
            html.Li(f"Meiste Medaillen im Event: {top_medalist} ({top_medalist_count} Medaillen)"),
            html.Li(f"Größter Teilnehmer: {groesster_name} ({groesster_value} cm)"),
            html.Li(f"Kleinster Teilnehmer: {kleinster_name} ({kleinster_value} cm)"),
            html.Li(f"Ältester Teilnehmer: {aeltester_name} ({aeltester_value} Jahre)"),
            html.Li(f"Jüngster Teilnehmer: {juengster_name} ({juengster_value} Jahre)")
        ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
