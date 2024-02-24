
<h1 align="center">
    <a href="https://www.1746.rio/hc/pt-br" target="_blank"><img src="static/logo-1746.png" alt="Central 1746" width="150"></a>
    </br>Análise de chamados da Central 1746
</br>
<img src="https://img.shields.io/badge/3.10-%233776AB?style=flat-square&logo=python&logoColor=white&label=Python" alt="Python 3.10">
<img src="https://img.shields.io/badge/black-%23000000?style=flat-square&label=code%20style&link=https%3A%2F%2Fgithub.com%2Fpsf%2Fblack" alt="Code Style Black">
</h1>

<div align="center">

<img src="https://img.shields.io/badge/-DVC-blue?style=flat-square&logo=dvc&logoColor=white&color=%239463CF" alt="DVC">
<img src="https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
<img src="https://img.shields.io/badge/-Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white" alt="Plotly">
<img src="https://img.shields.io/badge/-Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas">
<img src="https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">

<p>Dashboard interativo para visualização e análise dos dados da Central 1746 do Rio de Janeiro.</p>
<img src="https://i.imgur.com/UJlInkz.gif"/>
<hr/>
<table border=0 cellspacing=0 celspadding=0>
  <tr>
    <td><img src="https://imgur.com/iqO8VhW.jpg" width="240px"/></td>
    <td><img src="https://imgur.com/3vHlKLr.jpg" width="240px"/></td>
    <td><img src="https://imgur.com/k3DQQQg.jpg" width="240px"/></td>

  </tr>
</table>
</div>

## :page_with_curl: Sobre o Projeto

Este projeto consiste em um dashboard interativo para visualização e análise dos dados da Central 1746 do Rio de Janeiro durante o período de 2022 a 2023. A Central 1746 é responsável por receber e registrar solicitações, reclamações e denúncias dos cidadãos relacionadas a serviços públicos municipais.


## :tada: Funcionalidades

- Visualização de informações gerais sobre os atendimentos realizados.
- Análise ao longo do tempo.
- Geolocalização com destaque para os bairros com maior número de ocorrências.

## :wrench: Como Rodar o Projeto

1. Clone o repositório.
```bash
git clone https://github.com/jessicacardoso/emd-analise-central-1746.git
```

2. Faça o download dos dados e coloque-os na pasta `data/`.
```bash
pip install "dvc[gdrive]"
```

3. Faça download dos dados do Google Drive. Para isso, é necessário autenticar o DVC com a sua conta do Google Drive. Execute o comando abaixo e siga as instruções exibidas no terminal.
```bash
dvc get https://github.com/jessicacardoso/emd-analise-central-1746/ \
    data/rede_hoteleira_ocupacao_eventos.parquet -o data/rede_hoteleira_ocupacao_eventos.parquet

dvc get https://github.com/jessicacardoso/emd-analise-central-1746/ \
    data/bairro.parquet -o data/bairro.parquet

dvc get https://github.com/jessicacardoso/emd-analise-central-1746/ \
    data/chamado_1746.parquet -o data/chamado_1746.parquet
```

4. Instale as dependências necessárias para executar o dashboard.
```bash
pip install -r requirements.txt
```

5. Execute o dashboard com o comando:
```bash
streamlit run streamlit_app.py
```

6. Ou execute o aplicativo em um contêiner Docker:
```bash
docker build -t dashboard-1746 .
docker run -p 8501:8501 dashboard-1746
```
6. Acesse o endereço exibido no terminal (normalmente http://localhost:8501).

## :floppy_disk: Dados

Os dados utilizados neste projeto foram obtidos do projeto `datario`, disponível no Google Cloud Platform. Eles contêm informações sobre as ocorrências registradas na Central 1746, incluindo detalhes como tipo de serviço, localização, data e hora. As instruções para obter os dados estão disponíveis no [tutorial do Escritório de Dados](https://docs.dados.rio/tutoriais/como-acessar-dados/).

Abaixo, temos um diagrama das tabelas utilizadas no projeto:

<div align="center">
    <img src="dicionario-dados/tabelas-desafio.svg" height="600" alt="Tabelas do Desafio">
</div>
