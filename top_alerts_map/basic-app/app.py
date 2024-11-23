from shiny import App, render, ui
import pandas as pd
import geopandas as gpd
import zipfile
import os
import altair as alt

# load data
base_path = "/Users/charismalambert/Documents/GitHub/problem-set-6-solo/top_alerts_map"
file_path = os.path.join(base_path, "top_alerts_map.csv")
top_alerts = pd.read_csv(file_path)

top_alerts["type_subtype"] = top_alerts["type"] + " - " + top_alerts["subtype"]

#min_lat, max_lat = 41.86, 41.98
#min_long, max_long = -87.78, -87.64

app_ui = ui.page_fluid(
    ui.panel_title( "Select Type and Subtype"),
    ui.input_select("type_subtype", "Select Type and Subtype", choices = top_alerts[type_subtype].unique()),
    ui.output_text_verbatim("txt")
)

def server(input, output, session):
    @render.text
    def txt():
        return f"You selected: {input.type_subtype()}"
    
app = App(app_ui, server)
