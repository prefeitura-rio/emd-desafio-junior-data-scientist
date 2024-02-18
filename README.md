
<div align="center">
    <a href="https://www.1746.rio/hc/pt-br" target="_blank"><img src="static/logo-1746.png" align="right" alt="Central 1746" width="150"></a>
    <h1>Análise de chamados da Central 1746</h1>
    <a href="#tada-funcionalidades">Funcionalidades</a> •
    <a href="#computer-tecnologias-utilizadas">Tecnologias Utilizadas</a> •
    <a href="#wrench-como-rodar-o-projeto">Como Rodar o Projeto</a> •
    <a href="#floppy_disk-dados">Dados</a>
    <p>Dashboard interativo para visualização e análise dos dados da Central 1746 do Rio de Janeiro.</p>
</div>

![DVC](https://img.shields.io/badge/-DVC-blue?style=flat-square&logo=dvc&logoColor=white&color=%239463CF)
![Python 3.10](https://img.shields.io/badge/3.10-%233776AB?style=flat-square&logo=python&logoColor=white&label=Python)
![Code Style Black](https://img.shields.io/badge/black-%23000000?style=flat-square&label=code%20style&link=https%3A%2F%2Fgithub.com%2Fpsf%2Fblack)

Este projeto consiste em um dashboard interativo para visualização e análise dos dados da Central 1746 do Rio de Janeiro durante o período de 2022 a 2023. A Central 1746 é responsável por receber e registrar solicitações, reclamações e denúncias dos cidadãos relacionadas a serviços públicos municipais.


## :tada: Funcionalidades

- Visualização de estatísticas gerais sobre os atendimentos realizados.
- Análise de tendências ao longo do tempo.
- Geolocalização das ocorrências em um mapa interativo.

## :computer: Tecnologias Utilizadas

- **Streamlit**: Framework Python para criação de aplicativos web interativos.
- **Plotly**: Biblioteca para criação de gráficos e visualizações.
- **Pandas**: Manipulação e análise de dados.
- **Docker**: Para empacotar o aplicativo em um contêiner isolado.

## :wrench: Como Rodar o Projeto

1. Clone o repositório.
```bash
git clone https://github.com/jessicacardoso/emd-analise-central-1746.git
```

2. Faça o download dos dados e coloque-os na pasta `data/`.
```bash
pip install dvc[gdrive]
dvc pull
```

3. Instale as dependências.
```bash
pip install -r requirements.txt
```

4. Execute o aplicativo.
```bash
streamlit run streamlit_app.py
```

5. Ou execute o aplicativo em um contêiner Docker:
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
