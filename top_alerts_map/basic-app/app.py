from shiny import App, render, ui
import pandas as pd
import geopandas as gpd
import zipfile
import os
import altair as alt
import json

# load data
base_path = "/Users/charismalambert/Documents/GitHub/problem-set-6-solo/top_alerts_map"
file_path = os.path.join(base_path, "top_alerts_map.csv")
top_alerts = pd.read_csv(file_path)

top_alerts["type_subtype"] = top_alerts["type"] + " - " + top_alerts["subtype"]

file_path = "/Users/charismalambert/Downloads/Boundaries - Neighborhoods.geojson"

with open(file_path) as f:
    chicago_geojson = json.load(f)

geo_data = alt.Data(values=chicago_geojson["features"])



app_ui = ui.page_fluid(
    ui.panel_title( "Select Type and Subtype"),
    ui.input_select("type_subtype", 
                    "Type and Subtype Pairs",
                    choices = list(top_alerts["type_subtype"].unique())
    ),
    ui.output_text_verbatim("txt"),
    ui.output_plot("chart")
)

def server(input, output, session):
    map = alt.Chart(geo_data).mark_geoshape(
        fill = "lightgray",
        stroke = "white"
    ).project("equirectangular")

    @render.text
    def txt():
        return f"You selected: {input.type_subtype()}"
    
    def chart():
        #filter for type and subtype
        filter_for_type = top_alerts[top_alerts["type_subtype"] == input.type_subtype()]

        top_10 = filter_for_type.groupby(["binned_lat", "binned_long"]).size().reset_index(name="count").head(10)

        min_lat, max_lat = 41.86, 41.98
        min_long, max_long = -87.78, -87.64

        # altair scatter plot of top 10 type - subtype
        chart = alt.Chart(top_10).mark_circle().encode(
            x = alt.X("binned_long:Q", scale = alt.Scale(domain = [min_long, max_long]), title = "Longitude"),
            y = alt.Y("binned_lat:Q", scale = alt.Scale(domain = [min_lat, max_lat]), title = "Latitude"),
            size = alt.Size("count:Q", title = "Alert_Count"),
        ).properties(
            title = f"Top 10 Alerts for {input.type_subtype()}"
        ) 
        
        chicago_map = map + chart
        
        return chicago_map
    
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
