from shiny import App, render, ui
import pandas as pd
import geopandas as gpd
import zipfile
import os
import altair as alt

# load data
base_path = "/Users/charismalambert/Documents/GitHub/problem-set-6-solo/top_alerts_map"
file_path = os.path.join(base_path, "top_alerts_aggregated.csv")
top_alerts = pd.read_csv(file_path)

top_alerts["type_subtype"] = top_alerts["type"] + " - " + top_alerts["subtype"]
type_subtype = sorted(top_alerts["type_subtype"].unique())

min_lat, max_lat = 41.86, 41.98
min_long, max_long = -87.78, -87.64

app_ui = ui.page_fluid(
    ui.panel_title("type_subtype",  "Select Type and Subtype", type_subtype),
    ui.output_table("top_locations")
)

def server(input, output, session):
    @render.text
    def top_locations():
        filtered_df = top_alerts[top_alerts["type_subtype"] == input.type_subtype()]
        
        top_10 = filtered_df.nlargest(10, "count")
        
        return top_10[["binned_lat", "binned_long", "count"]]
    
app = App(app_ui, server)
