import geopandas as gpd
import plotly.express as px


def make_choropleth(calls, neighborhoods):
    neighboards_calls = (
        calls.merge(neighborhoods, how="right", on="id_bairro")
        .groupby("id_bairro")
        .agg(
            {
                "id_bairro": "count",
                "nome": "first",
                "subprefeitura": "first",
                "geometry": "first",
            }
        )
        .rename(columns={"id_bairro": "chamados"})
        .sort_values("chamados", ascending=False)
    )

    neighboards_calls = gpd.GeoDataFrame(
        neighboards_calls,
        geometry=gpd.GeoSeries.from_wkt(neighboards_calls["geometry"]),
        crs="EPSG:4326",
    )
    fig = px.choropleth_mapbox(
        neighboards_calls,
        geojson=neighboards_calls["geometry"],
        locations=neighboards_calls.index,
        color="chamados",
        color_continuous_scale="Blues",
        range_color=(0, neighboards_calls["chamados"].max()),
        mapbox_style="carto-positron",
        zoom=8.5,
        center={"lat": -22.914469232838503, "lon": -43.4461895474592},
        opacity=0.6,
        hover_data={"nome": True, "subprefeitura": True, "chamados": True},
        width=400,
        height=350,
    )

    fig.update_layout(
        coloraxis_showscale=False,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    return fig
