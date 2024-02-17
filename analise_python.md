# Análise de chamados ao 1746

Scripts em python usando pandas para responder as perguntas a seguir.


```python
import pandas as pd
import basedosdados as bd
from datetime import date

calls = bd.read_sql(
    """
    SELECT
        *
    FROM
        `datario.administracao_servicos_publicos.chamado_1746`
    WHERE
        data_particao BETWEEN "2022-01-01" AND "2023-12-31";
    """,
    billing_project_id="avian-light-413816",
)

neighborhoods = bd.read_sql(
    """
    SELECT
        *
    FROM
        `datario.dados_mestres.bairro`;
    """,
    billing_project_id="avian-light-413816",
)

events = bd.read_sql(
    """
    SELECT
        *
    FROM
        `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos`;
    """,
    billing_project_id="avian-light-413816",
)
```

    Downloading: 100%|[32m██████████[0m|
    Downloading: 100%|[32m██████████[0m|
    Downloading: 100%|[32m██████████[0m|


## Localização de chamados do 1746

1. Quantos chamados foram abertos no dia 01/04/2023?


```python
# 1. Quantos chamados foram abertos no dia 01/04/2023?
calls_01042023 = calls[calls["data_inicio"].dt.date == date(2023, 4, 1)]
print(f"Foram abertos {calls_01042023.shape[0]} chamados no dia 01/04/2023")
```

    Foram abertos 73 chamados no dia 01/04/2023


2. Qual o tipo de chamado que teve mais reclamações no dia 01/04/2023?


```python
# 2. Qual o tipo de chamado que teve mais reclamações no dia 01/04/2023?
most_complained_type = calls_01042023["tipo"].value_counts().idxmax()
print(
    f'O tipo de chamado que teve mais reclamações no dia 01/04/2023 foi "{most_complained_type}"'
)
```

    O tipo de chamado que teve mais reclamações no dia 01/04/2023 foi "Poluição sonora"


3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?


```python
# 3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?
calls_with_neighborhoods = calls_01042023.merge(
    neighborhoods, left_on="id_bairro", right_on="id_bairro"
)

top_3_neighborhoods = calls_with_neighborhoods["nome"].value_counts().head(3)
print(f"Os 3 bairros que mais tiveram chamados abertos no dia 01/04/2023 foram:")
display(top_3_neighborhoods)
```

    Os 3 bairros que mais tiveram chamados abertos no dia 01/04/2023 foram:



    nome
    Engenho de Dentro    8
    Leblon               6
    Campo Grande         6
    Name: count, dtype: int64


4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?


```python
# 4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?
most_called_subprefecture = (
    calls_with_neighborhoods["subprefeitura"].value_counts().idxmax()
)
print(
    f'A subprefeitura com mais chamados abertos no dia 01/04/2023 foi "{most_called_subprefecture}"'
)
```

    A subprefeitura com mais chamados abertos no dia 01/04/2023 foi "Zona Norte"


5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?


```python
# 5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?
calls_without_neighborhood = calls_01042023.loc[
    ~calls_01042023["id_bairro"].isin(neighborhoods["id_bairro"])
]
if calls_without_neighborhood.shape[0] > 0:
    print("Sim, há chamados que não foram associados a um bairro ou subprefeitura.")
    with pd.option_context("display.max_colwidth", 0):
        display(
            calls_without_neighborhood.loc[
                :, ["id_bairro", "tipo", "subtipo"]
            ].reset_index(drop=True)
        )
```

    Sim, há chamados que não foram associados a um bairro ou subprefeitura.



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_bairro</th>
      <th>tipo</th>
      <th>subtipo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>None</td>
      <td>Ônibus</td>
      <td>Verificação de ar condicionado inoperante no ônibus</td>
    </tr>
  </tbody>
</table>
</div>


## Chamados do 1746 em grandes eventos

6. Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?


```python
# 6. Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?

calls_perturbacao_sossego = calls.loc[
    (calls["subtipo"] == "Perturbação do sossego")
    & (calls["data_inicio"].dt.year.between(2022, 2023))
]

print(
    f'Foram abertos {calls_perturbacao_sossego.shape[0]:,} chamados com o subtipo "Perturbação do sossego" desde 01/01/2022 até 31/12/2023'
)
```

    Foram abertos 42,408 chamados com o subtipo "Perturbação do sossego" desde 01/01/2022 até 31/12/2023


7. Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).


```python
# 7. Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).
def get_event(date):
    event = events.loc[
        (date >= events["data_inicial"]) & (date <= events["data_final"]), "evento"
    ]
    return event.item() if event.shape[0] > 0 else None


calls_during_events = (
    calls_perturbacao_sossego.loc[
        calls_perturbacao_sossego["data_inicio"].dt.date.between(
            events["data_inicial"].min(), events["data_final"].max()
        ),
        ["id_chamado", "tipo", "subtipo", "data_inicio", "subtipo"],
    ]
    .assign(durante_evento=lambda d: d["data_inicio"].dt.date.apply(get_event))
    .dropna(subset=["durante_evento"])
)


print(calls_during_events.info())
display(calls_during_events.head())
display(calls_during_events.tail())
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 1212 entries, 104220 to 1610754
    Data columns (total 6 columns):
     #   Column          Non-Null Count  Dtype
    ---  ------          --------------  -----
     0   id_chamado      1212 non-null   object
     1   tipo            1212 non-null   object
     2   subtipo         1212 non-null   object
     3   data_inicio     1212 non-null   datetime64[ns]
     4   subtipo         1212 non-null   object
     5   durante_evento  1212 non-null   object
    dtypes: datetime64[ns](1), object(5)
    memory usage: 66.3+ KB
    None



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_chamado</th>
      <th>tipo</th>
      <th>subtipo</th>
      <th>data_inicio</th>
      <th>subtipo</th>
      <th>durante_evento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>104220</th>
      <td>18078399</td>
      <td>Poluição sonora</td>
      <td>Perturbação do sossego</td>
      <td>2022-12-30 23:55:13</td>
      <td>Perturbação do sossego</td>
      <td>Reveillon</td>
    </tr>
    <tr>
      <th>104221</th>
      <td>18078416</td>
      <td>Poluição sonora</td>
      <td>Perturbação do sossego</td>
      <td>2022-12-31 00:38:53</td>
      <td>Perturbação do sossego</td>
      <td>Reveillon</td>
    </tr>
    <tr>
      <th>104222</th>
      <td>18079138</td>
      <td>Poluição sonora</td>
      <td>Perturbação do sossego</td>
      <td>2022-12-31 13:55:41</td>
      <td>Perturbação do sossego</td>
      <td>Reveillon</td>
    </tr>
    <tr>
      <th>104224</th>
      <td>18078209</td>
      <td>Poluição sonora</td>
      <td>Perturbação do sossego</td>
      <td>2022-12-30 21:05:12</td>
      <td>Perturbação do sossego</td>
      <td>Reveillon</td>
    </tr>
    <tr>
      <th>105544</th>
      <td>18079523</td>
      <td>Poluição sonora</td>
      <td>Perturbação do sossego</td>
      <td>2022-12-31 20:52:48</td>
      <td>Perturbação do sossego</td>
      <td>Reveillon</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_chamado</th>
      <th>tipo</th>
      <th>subtipo</th>
      <th>data_inicio</th>
      <th>subtipo</th>
      <th>durante_evento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1610104</th>
      <td>18080295</td>
      <td>Poluição sonora</td>
      <td>Perturbação do sossego</td>
      <td>2023-01-01 21:02:32</td>
      <td>Perturbação do sossego</td>
      <td>Reveillon</td>
    </tr>
    <tr>
      <th>1610113</th>
      <td>18079629</td>
      <td>Poluição sonora</td>
      <td>Perturbação do sossego</td>
      <td>2023-01-01 03:56:34</td>
      <td>Perturbação do sossego</td>
      <td>Reveillon</td>
    </tr>
    <tr>
      <th>1610118</th>
      <td>18080124</td>
      <td>Poluição sonora</td>
      <td>Perturbação do sossego</td>
      <td>2023-01-01 17:39:28</td>
      <td>Perturbação do sossego</td>
      <td>Reveillon</td>
    </tr>
    <tr>
      <th>1610746</th>
      <td>18079614</td>
      <td>Poluição sonora</td>
      <td>Perturbação do sossego</td>
      <td>2023-01-01 02:11:44</td>
      <td>Perturbação do sossego</td>
      <td>Reveillon</td>
    </tr>
    <tr>
      <th>1610754</th>
      <td>18080382</td>
      <td>Poluição sonora</td>
      <td>Perturbação do sossego</td>
      <td>2023-01-01 23:05:50</td>
      <td>Perturbação do sossego</td>
      <td>Reveillon</td>
    </tr>
  </tbody>
</table>
</div>


8. Quantos chamados desse subtipo foram abertos em cada evento?


```python
# 8. Quantos chamados desse subtipo foram abertos em cada evento?
calls_during_events_by_event = calls_during_events["durante_evento"].value_counts()
print(
    'Quantidade de chamados com o subtipo "Perturbação do sossego" abertos em cada evento:'
)
display(calls_during_events_by_event)
```

    Quantidade de chamados com o subtipo "Perturbação do sossego" abertos em cada evento:



    Rock in Rio    834
    Carnaval       241
    Reveillon      137
    Name: durante_evento, dtype: int64


9. Qual evento teve a maior média diária de chamados abertos desse subtipo?


```python
# 9. Qual evento teve a maior média diária de chamados abertos desse subtipo?
calls_during_events["data"] = calls_during_events["data_inicio"].dt.date
calls_during_events_by_event_and_day = (
    calls_during_events.groupby(["durante_evento", "data"])
    .size()
    .reset_index(name="count")
    .groupby("durante_evento")["count"]
    .mean()
)

print(
    f"O evento com maior média diária de chamados desse subtipo foi o {calls_during_events_by_event_and_day.idxmax()} com {calls_during_events_by_event_and_day.max():.2f} chamados por dia"
)
```

    O evento com maior média diária de chamados desse subtipo foi o Rock in Rio com 119.14 chamados por dia


10. Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.



```python
# 10. Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.

calls_perturbacao_sossego_by_day = (
    calls_perturbacao_sossego.groupby(calls_perturbacao_sossego["data_inicio"].dt.date)
    .size()
    .mean()
)

calls_during_events_by_event_and_day = pd.concat(
    [
        calls_during_events_by_event_and_day,
        pd.Series(
            calls_perturbacao_sossego_by_day,
            index=["Período de 01/01/2022 até 31/12/2023"],
        ),
    ]
)
print(calls_during_events_by_event_and_day)
```

    Carnaval                                 60.250000
    Reveillon                                45.666667
    Rock in Rio                             119.142857
    Período de 01/01/2022 até 31/12/2023     63.201192
    dtype: float64
