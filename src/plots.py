from typing import Any
from typing import Dict
from typing import Optional

import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    x_label: str = "",
    y_label: str = "",
    title: str = "",
    title_font_size: Optional[int] = None,
    margin: Optional[Dict[str, Any]] = None,
    height: Optional[int] = None,
) -> go.Figure:
    """
    Plota um gráfico de barras horizontal.

    Args:
        data (pd.DataFrame): O dataframe contendo os dados a serem plotados.
        x (str): A coluna do dataframe a ser usada no eixo x.
        y (str): A coluna do dataframe a ser usada no eixo y.
        x_label (str, optional): O rótulo do eixo x. Defaults to "".
        y_label (str, optional): O rótulo do eixo y. Defaults to "".
        title (str, optional): O título do gráfico. Defaults to "".
        title_font_size (int, optional): O tamanho da fonte do título. Defaults to None.
        margin (dict, optional): Configuração das margens do gráfico. Defaults to None.
        height (int, optional): A altura do gráfico. Defaults to None.

    Returns:
        go.Figure: O objeto figura do Plotly contendo o gráfico de barras.
    """
    # Cria um gráfico de barras horizontal
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        orientation="h",
        labels={"x": x_label, "y": y_label},
        height=height,
    )

    # Configurações para a aparência das barras
    fig.update_traces(
        marker_color="#004A80",
        texttemplate="<b>%{x}</b>",
        textposition=[
            "inside" if i == data.shape[0] - 1 else "outside"
            for i in range(data.shape[0])
        ],
        textfont=dict(size=16),
    )

    # Configurações adicionais para o layout do gráfico
    fig.update_layout(
        xaxis_visible=False,
        xaxis_showticklabels=False,
        margin=margin,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        yaxis=dict(
            showline=True,
            linewidth=2,
            linecolor="black",
            tickfont=dict(size=16),
        ),
        title_font_size=title_font_size,
    )
    fig.update_yaxes(title_text="", ticksuffix="   ")

    return fig


def make_choropleth(
    calls: pd.DataFrame, neighborhoods: pd.DataFrame
) -> go.Figure:
    """
    Cria um mapa de coroplético com base nos chamados por bairro.

    Args:
        calls (pd.DataFrame): O dataframe contendo os chamados.
        neighborhoods (pd.DataFrame): O dataframe contendo os bairros.

    Returns:
        go.Figure: O objeto figura do Plotly contendo o mapa de coroplético.
    """
    # Agrupa os chamados por bairro
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

    # Cria um GeoDataFrame a partir do resultado
    neighboards_calls = gpd.GeoDataFrame(
        neighboards_calls,
        geometry=gpd.GeoSeries.from_wkt(neighboards_calls["geometry"]),
        crs="EPSG:4326",
    )

    # Cria o mapa de coroplético
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

    # Configurações adicionais para o layout do gráfico
    fig.update_layout(
        coloraxis_showscale=False,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    return fig


def plot_calls_ts(calls: pd.DataFrame) -> go.Figure:
    """
    Plota um gráfico de séries temporais para os chamados.

    Args:
        calls (pd.DataFrame): O dataframe contendo os chamados.

    Returns:
        go.Figure: O objeto figura do Plotly contendo o gráfico de séries temporais.
    """
    # Cria um gráfico de linha com a contagem de chamados por data
    fig = px.line(
        calls["data_inicio"].dt.date.value_counts().sort_index(),
        template="plotly_white",
    )

    # Configurações visuais para as linhas do gráfico
    fig.update_traces(line=dict(color="#004A80", width=2))

    # Configurações adicionais para o layout do gráfico
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    fig.update_layout(
        xaxis=dict(tickfont=dict(size=14)), yaxis=dict(tickfont=dict(size=14))
    )

    # Configurações para o seletor de intervalo de datas
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

    # Altera o tamanho do gráfico
    fig.update_layout(
        autosize=True,
        width=800,
        height=350,
    )

    return fig
