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
html.H2("Fakten zu Sportarten und Events", 
            style={
                'marginTop': '40px', 
                'textAlign': 'center',
                'color': '#2c3e50',
                'fontWeight': '300',
                'fontSize': '2.2em',
                'marginBottom': '30px'
            }),
    
    html.Div([
        # Linke Spalte: Fakten zur Sportart
        html.Div([
            html.Label("🏃‍♂️ Sportart:", 
                      style={'fontSize': '18px', 'fontWeight': '600', 'color': '#2c3e50', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='sportart-fakten-dropdown',
                options=sport_options,
                value=unique_sports_de[0],
                clearable=False,
                style={
                    'width': '100%',
                    'fontSize': '16px'
                },
                placeholder="Sportart auswählen..."
            ),
            html.Div(id='sportart-fakten-output', 
                    style={
                        'fontSize': '16px', 
                        'marginTop': '25px',
                        'background': 'rgba(255, 255, 255, 0.9)',
                        'padding': '20px',
                        'borderRadius': '12px',
                        'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.1)',
                        'border': '1px solid rgba(102, 126, 234, 0.2)'
                    }),
        ], style={
            'width': '48%', 
            'display': 'inline-block', 
            'verticalAlign': 'top',
            'background': 'rgba(255, 255, 255, 0.7)',
            'padding': '25px',
            'borderRadius': '15px',
            'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)',
            'backdropFilter': 'blur(10px)',
            'border': '1px solid rgba(255, 255, 255, 0.3)'
        }),
        
        # Rechte Spalte: Event-Dropdown und Fakten
        html.Div([
            html.Label("🏅 Event (Spiele & Stadt):", 
                      style={'fontSize': '18px', 'fontWeight': '600', 'color': '#2c3e50', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='event-dropdown',
                options=[],
                value=None,
                clearable=False,
                style={
                    'width': '100%',
                    'fontSize': '16px'
                },
                placeholder="Event auswählen..."
            ),
            html.Div(id='event-fakten-output', 
                    style={
                        'fontSize': '16px', 
                        'marginTop': '25px',
                        'background': 'rgba(255, 255, 255, 0.9)',
                        'padding': '20px',
                        'borderRadius': '12px',
                        'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.1)',
                        'border': '1px solid rgba(102, 126, 234, 0.2)'
                    }),
        ], style={
            'width': '48%', 
            'display': 'inline-block', 
            'marginLeft': '4%', 
            'verticalAlign': 'top',
            'background': 'rgba(255, 255, 255, 0.7)',
            'padding': '25px',
            'borderRadius': '15px',
            'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)',
            'backdropFilter': 'blur(10px)',
            'border': '1px solid rgba(255, 255, 255, 0.3)'
        }),
    ], style={
        'width': '100%', 
        'display': 'flex',
        'gap': '20px',
        'marginBottom': '40px'
    }),
])

# Event-Dropdown aktualisieren
@app.callback(
    Output('event-dropdown', 'options'),
    Output('event-dropdown', 'value'),
    Input('sportart-fakten-dropdown', 'value')
)
def update_event_dropdown(sport):
    if not sport:
        return [], None
    options = get_event_options(sport)
    return options, options[0]['value'] if options else None

# Fakten zur Sportart immer anzeigen
@app.callback(
    Output('sportart-fakten-output', 'children'),
    Input('sportart-fakten-dropdown', 'value')
)
def sportart_fakten(sportart):
    if not sportart:
        return html.Div("Bitte wählen Sie eine Sportart aus.", 
                       style={'textAlign': 'center', 'color': '#7f8c8d', 'fontStyle': 'italic'})
    
    df = athlete_events[athlete_events['sport'] == sportart]
    if df.empty:
        return html.Div("Keine Daten für diese Sportart verfügbar.", 
                       style={'textAlign': 'center', 'color': '#e74c3c'})
    
    # Berechnungen
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
        html.H4(f"📊 {sportart}", 
               style={'color': '#2c3e50', 'marginBottom': '20px', 'fontSize': '1.4em'}),
        html.Div([
            html.Div([
                html.Span("🗓️ ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Olympische Spiele: {austragungen} ({first_year}–{last_year})")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(102, 126, 234, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #667eea'}),
            
            html.Div([
                html.Span("🏃‍♂️ ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Top-Athlet: {top_athlet} ({top_athlet_count} Teilnahmen)")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(102, 126, 234, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #667eea'}),
            
            html.Div([
                html.Span("🌍 ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Top-Land: {top_land} ({top_land_count} Teilnahmen)")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(102, 126, 234, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #667eea'}),
            
            html.Div([
                html.Span("👥 ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Verschiedene Athleten: {unique_athletes:,}")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(102, 126, 234, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #667eea'}),
            
            html.Div([
                html.Span("🏁 ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Teilnehmende Länder: {unique_countries}")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(102, 126, 234, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #667eea'}),
            
            html.Div([
                html.Span("🎯 ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Häufigste Disziplin: {top_event} ({top_event_count} Teilnahmen)")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(102, 126, 234, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #667eea'}),
        ])
    ])

# Fakten zum Event (Games + City) immer anzeigen
@app.callback(
    Output('event-fakten-output', 'children'),
    Input('event-dropdown', 'value'),
    Input('sportart-fakten-dropdown', 'value')
)
def event_fakten(event_value, sportart):
    if not event_value or not sportart:
        return html.Div("Bitte wählen Sie eine Sportart und ein Event aus.", 
                       style={'textAlign': 'center', 'color': '#7f8c8d', 'fontStyle': 'italic'})
    
    games, city = event_value.split("||")
    df = athlete_events[(athlete_events['sport'] == sportart) & 
                       (athlete_events['Games'] == games) & 
                       (athlete_events['City'] == city)]
    
    if df.empty:
        return html.Div("Keine Daten für dieses Event verfügbar.", 
                       style={'textAlign': 'center', 'color': '#e74c3c'})
    
    # Berechnungen
    teilnehmer = df['name'].nunique()
    
    medals = df[df['medal'].notna()].groupby('name').size()
    if not medals.empty:
        top_medalist = medals.idxmax()
        top_medalist_count = medals.max()
    else:
        top_medalist = "Keine Daten"
        top_medalist_count = 0
    
    # Größe
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
    
    # Alter
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
        html.H4(f"🏅 {games} ({city})", 
               style={'color': '#2c3e50', 'marginBottom': '20px', 'fontSize': '1.4em'}),
        html.Div([
            html.Div([
                html.Span("👥 ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Teilnehmer: {teilnehmer:,} Athleten")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(118, 75, 162, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #764ba2'}),
            
            html.Div([
                html.Span("🏆 ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Meiste Medaillen: {top_medalist} ({top_medalist_count})")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(118, 75, 162, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #764ba2'}),
            
            html.Div([
                html.Span("📏 ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Größter: {groesster_name} ({groesster_value} cm)")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(118, 75, 162, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #764ba2'}),
            
            html.Div([
                html.Span("📐 ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Kleinster: {kleinster_name} ({kleinster_value} cm)")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(118, 75, 162, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #764ba2'}),
            
            html.Div([
                html.Span("👴 ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Ältester: {aeltester_name} ({aeltester_value} Jahre)")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(118, 75, 162, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #764ba2'}),
            
            html.Div([
                html.Span("👶 ", style={'fontSize': '1.2em', 'marginRight': '8px'}),
                html.Span(f"Jüngster: {juengster_name} ({juengster_value} Jahre)")
            ], style={'marginBottom': '12px', 'padding': '10px', 'background': 'rgba(118, 75, 162, 0.1)', 'borderRadius': '8px', 'borderLeft': '4px solid #764ba2'}),
        ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
