import geopandas as gpd
import plotly.express as px


def plot_calls_by_neighborhood(calls_by_neighborhood, top_n=10, height=350):
    top_10 = (
        calls_by_neighborhood["nome"].value_counts().head(top_n).sort_values()
    )
    fig = px.bar(
        top_10,
        x=top_10.values,
        y=top_10.index,
        orientation="h",
        labels={"x": "Chamados", "y": "Bairro"},
        height=height,
    )

    fig.update_yaxes(title_text="")
    fig.update_layout(
        xaxis_visible=False,
        xaxis_showticklabels=False,
        margin=dict(l=0, r=0, b=0, t=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    fig.update_traces(
        marker_color="#004A80",
        texttemplate="<b>%{x}</b>",
        textposition=[
            "inside" if i == top_10.shape[0] - 1 else "outside"
            for i in range(top_10.shape[0])
        ],
        textfont=dict(size=16),
    )

    fig.update_layout(
        yaxis=dict(
            showline=True,
            linewidth=2,
            linecolor="black",
            tickfont=dict(size=16),
        ),
    )
    fig.update_yaxes(ticksuffix="   ")
    return fig


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


def plot_calls_ts(calls):
    fig = px.line(
        calls["data_inicio"].dt.date.value_counts().sort_index(),
        template="plotly_white",
    )

    fig.update_traces(line=dict(color="#004A80", width=2))

    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)

    fig.update_layout(
        xaxis=dict(tickfont=dict(size=14)), yaxis=dict(tickfont=dict(size=14))
    )

    fig.update_layout(
        showlegend=False,
        margin=dict(r=0, b=0),
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(
                            count=1,
                            label="1 mês",
                            step="month",
                            stepmode="backward",
                        ),
                        dict(
                            count=3,
                            label="3 meses",
                            step="month",
                            stepmode="backward",
                        ),
                        dict(
                            count=6,
                            label="6 meses",
                            step="month",
                            stepmode="backward",
                        ),
                        dict(
                            count=1,
                            label="1 ano",
                            step="year",
                            stepmode="backward",
                        ),
                        dict(label="tudo", step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        ),
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
    )

    # alterar tamanho do gráfico
    fig.update_layout(
        autosize=True,
        width=800,
        height=350,
    )

    return fig


def plot_calls_during_events(calls_during_events):
    fig = px.bar(
        calls_during_events,
        x="chamados",
        y="evento",
        template="plotly_white",
    )

    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)

    fig.update_layout(
        xaxis=dict(tickfont=dict(size=14)), yaxis=dict(tickfont=dict(size=14))
    )

    fig.update_layout(
        showlegend=False,
        margin=dict(r=0, b=0),
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        autosize=True,
        height=380,
        title=dict(
            text="Quantidade de chamados por evento",
            font=dict(size=20, color="#004A80"),
        ),
    )

    fig.update_traces(
        marker_color="#004A80",
        texttemplate="<b>%{x}</b>",
        textposition=[
            "inside" if i == calls_during_events.shape[0] - 1 else "outside"
            for i in range(calls_during_events.shape[0])
        ],
        textfont=dict(size=16),
    )
    fig.update_xaxes(showticklabels=False)
    return fig
