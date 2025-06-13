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
        dcc.Dropdown(id='country-dropdown', options=region_options, value='Deutschland'),
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
                    value=['Deutschland', 'Vereinigte Staaten'],
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
    sports_de = [sport_translation.get(s, s) for s in sports_en]
    options = [{'label': '🏆 Alle Sportarten', 'value': 'Alle'}] + [
        {'label': de, 'value': de} for de in sports_de
    ]
    value_dropdown = 'Alle'
    value_fakten = sports_de[0] if sports_de else 'Alle'
    return options, value_dropdown, options, value_fakten

# Land Dropdown: Deutsch -> Englisch für Filterung
def country_de_to_en(de):
    return country_translation_de_to_en.get(de, de)

# Sport Dropdown: Deutsch -> Englisch für Filterung
def sport_de_to_en(de):
    return sport_translation_de_to_en.get(de, de)

@app.callback(
    Output('medals-chart', 'figure'),
    Input('period-dropdown', 'value'),
    Input('season-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('sport-dropdown', 'value'),
    Input('gender-dropdown', 'value')
)
def update_medals_chart(period, season, country_de, sport_de, gender):
    start, end = time_periods[period]
    country_en = country_de_to_en(country_de)
    df = athlete_events[
        (athlete_events['year'].between(start, end)) &
        (athlete_events['season'] == season) &
        (athlete_events['region'] == country_en) &
        (athlete_events['medal'].notna())
    ]
    if sport_de != 'Alle':
        sport_en = sport_de_to_en(sport_de)
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
        title=f"{country_de} – {sport_de if sport_de != 'Alle' else 'alle Sportarten'} ({season}, {period})",
        xaxis_title='Jahr',
        yaxis_title='Medaillen',
        yaxis=dict(tickformat=".0f")
    )
    return fig

@app.callback(
    Output('heatmap-chart', 'figure'),
    Input('period-dropdown', 'value'),
    Input('season-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('gender-dropdown', 'value')
)
def update_heatmap(period, season, country_de, gender):
    start, end = time_periods[period]
    country_en = country_de_to_en(country_de)
    df = athlete_events[
        (athlete_events['year'].between(start, end)) &
        (athlete_events['season'] == season) &
        (athlete_events['region'] == country_en) &
        (athlete_events['medal'].notna())
    ]
    if gender != 'Alle':
        df = df[df['sex'] == gender]
    if df.empty:
        return go.Figure().add_annotation(text="⚠️ Keine Daten verfügbar", x=0.5, y=0.5, showarrow=False)
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
        title=f"Heatmap – {country_de} ({season}, {period})",
        xaxis_title='Jahr',
        yaxis_title='Sportart'
    )
    return fig

@app.callback(
    Output('country-comparison-chart', 'figure'),
    Input('period-dropdown', 'value'),
    Input('season-dropdown', 'value'),
    Input('multi-country-dropdown', 'value'),
    Input('medal-dropdown', 'value'),
    Input('gender-dropdown', 'value')
)
def update_country_comparison(period, season, countries_de, medal_type, gender):
    start, end = time_periods[period]
    countries_en = [country_de_to_en(c) for c in countries_de]
    df = athlete_events[
        (athlete_events['year'].between(start, end)) &
        (athlete_events['season'] == season) &
        (athlete_events['region'].isin(countries_en)) &
        (athlete_events['medal'].notna())
    ]
    if gender != 'Alle':
        df = df[df['sex'] == gender]
    if medal_type != 'Alle':
        df = df[df['medal'] == medal_type]
    if df.empty:
        return go.Figure().add_annotation(text="⚠️ Keine Medaillendaten für diese Auswahl", x=0.5, y=0.5, showarrow=False)
    counts = df.groupby('region').size().reindex(countries_en, fill_value=0)
    # Achsen wieder auf Deutsch
    countries_de_axis = [country_translation.get(c, c) for c in counts.index]
    fig = go.Figure(data=[go.Bar(
        x=countries_de_axis,
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
    Input('sportart-fakten-dropdown', 'value'),
    Input('season-dropdown', 'value')
)
def sportart_fakten(sportart_de, season):
    if sportart_de == 'Alle':
        return html.Div("Bitte eine konkrete Sportart auswählen.")
    sport_en = sport_de_to_en(sportart_de)
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
        top_land_en = teilnahmen_land.idxmax()
        top_land = country_translation.get(top_land_en, top_land_en)
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
@app.callback(
    Output('olympiade-fakten-output', 'children'),
    Input('olympiade-jahr-dropdown', 'value'),
    Input('season-dropdown', 'value')
)
def olympiade_fakten(jahr, season):
    df = athlete_events[(athlete_events['year'] == jahr) & (athlete_events['season'] == season)]
    
    if df.empty:
        return html.Div("Keine Daten für diese Olympiade.")

    n_sportarten = df['sport'].nunique()
    n_events = df['event'].nunique()
    n_athleten = df['name'].nunique()

    teilnahmen_land = df['region'].value_counts()
    top_land = teilnahmen_land.idxmax()
    top_land_de = country_translation.get(top_land, top_land)
    top_land_count = teilnahmen_land.max()

    medal_df = df[df['medal'].notna()]
    if not medal_df.empty:
        erfolgreichstes_land = medal_df['region'].value_counts().idxmax()
        erfolgreichstes_land_de = country_translation.get(erfolgreichstes_land, erfolgreichstes_land)
        erfolgreichstes_land_medals = medal_df['region'].value_counts().max()
        häufigste_medaille = medal_df['medal'].value_counts().idxmax()
    else:
        erfolgreichstes_land_de = "Keine Daten"
        erfolgreichstes_land_medals = 0
        häufigste_medaille = "Keine Medaillen"

    return html.Div([
        html.H4(f"Fakten zu den Olympischen Spielen {jahr} ({season})"),
        html.Ul([
            html.Li(f"Anzahl Sportarten: {n_sportarten}"),
            html.Li(f"Anzahl Disziplinen (Events): {n_events}"),
            html.Li(f"Anzahl Athletinnen und Athleten: {n_athleten}"),
            html.Li(f"Land mit den meisten Teilnahmen: {top_land_de} ({top_land_count})"),
            html.Li(f"Erfolgreichstes Land: {erfolgreichstes_land_de} ({erfolgreichstes_land_medals} Medaillen)"),
            html.Li(f"Häufigste Medaille: {häufigste_medaille}")
        ])
        dcc.Dropdown(
            id='olympiade-jahr-dropdown',
            options=[{'label': str(j), 'value': j} for j in sorted(athlete_events['year'].unique())],
            value=2016
)
        html.Div(id='olympiade-fakten-output')


    ])



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
