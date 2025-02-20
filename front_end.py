import dash
from dash import dcc, html
import plotly.express as px
import sqlite3
import pandas as pd

conn = sqlite3.connect("elf_sections.db")
df = pd.read_sql_query('SELECT timestamp, size, section_name FROM elf_sections ORDER BY timestamp', conn)
conn.close()

app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        dcc.Graph(
            figure=px.area(df, x='timestamp', y='size', title="ELF File Size over Time", text="section_name", color="section_name"),
            style={"height": "100vh", "width": "100vw"}
        )
    ],
    style={"height": "100vh", "width": "100vw", "margin": 0, "padding": 0, "overflow": "hidden"}
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050)
