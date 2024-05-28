from dash import Dash, html, dcc, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv("rodion.csv")
all_cont = df['Country'].unique()

external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([
    html.Div([
        html.H1("Дашборд"),
        html.P(
            "Статистика показателей по странам мира."
        )
    ], style={
        'backgroundColor': 'rgb(100, 100, 158)',
        'padding': '10px 10px'
    }),

    html.Div([
        html.Div([
            html.Label('Выпадающий список показателей'),
            dcc.Dropdown(
                id='crossfilter-ind',
                options=[{'label': i, 'value': i} for i in df.columns[2:]],
                value='Population'
            )
        ]),
        dcc.Graph(id='bar-chart',
                  style={'width': '100%', 'display': 'inline-block'}),
        dcc.Graph(id='map', style={'width': '100%',
                  'display': 'inline-block'}),
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    })])


@app.callback(
    Output('bar-chart', 'figure'),
    [Input('crossfilter-ind', 'value')]
)
def update_bar_chart(indicator):
    fig = px.bar(
        df.sort_values(indicator, ascending=False).head(20),
        x='Country',
        y=indicator,
        title="Топ-20 стран по выбранному показателю",
        color='Country'
    )
    return fig


@app.callback(
    Output('map', 'figure'),
    [Input('crossfilter-ind', 'value')]
)
def update_map(indicator):
    fig = px.choropleth(
        df,
        locations='Country',
        locationmode='country names',
        color=indicator,
        title="Распределение выбранного показателя по миру",
        hover_name='Country',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)