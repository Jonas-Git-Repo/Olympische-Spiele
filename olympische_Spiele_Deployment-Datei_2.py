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
    
    # 🔹 Filter oben
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

    # 🔹 Tabs
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

    # 🔹 Sportarten-Fakten
    html.H2("Fakten zu den Sportarten", style={'marginTop': '40px'}),
    html.Label("Wähle eine Sportart:"),
    dcc.Dropdown(
        id='sportart-fakten-dropdown',
        options=sport_options,
        value=sport_options[1]['value'],  # erste echte Sportart als Default
        clearable=False,
        style={'width': '60%'}
    ),
    html.Div(id='sportart-fakten-output', style={'fontSize': '18px', 'marginTop': '20px'}),

    # 🔹 Olympiade-Fakten
    html.H2("📅 Olympiade-Fakten", style={'marginTop': '50px'}),
    html.Label("Jahr der Olympiade:"),
    dcc.Dropdown(
        id='olympiade-jahr-dropdown',
        options=[{'label': str(j), 'value': j} for j in sorted(athlete_events['year'].unique())],
        value=2016,
        style={'width': '40%'}
    ),
    html.Label("Saison:"),
    dcc.Dropdown(
        id='season-dropdown',
        options=[
            {'label': '☀️ Sommer', 'value': 'Summer'},
            {'label': '❄️ Winter', 'value': 'Winter'}
        ],
        value='Summer',
        style={'width': '40%', 'marginBottom': '20px'}
    ),
    html.Div(id='olympiade-fakten-output', style={'fontSize': '18px'})
])



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
