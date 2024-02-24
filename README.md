# Desafio Técnico - Cientista de Dados Júnior

## Descrição

Bem-vindo! Este é um fork do repositório original do desafio e aqui estão as minhas respostas para o desafio técnico para a vaga de Cientista de Dados Júnior no Escritório Municipal de Dados do Rio de Janeiro. Este desafio tem o objetivo de avaliar habilidades técnicas em manipulação de dados, consulta SQL, análise de dados e visualização de dados utilizando ferramentas como BigQuery e Python. 

### Objetivo

O objetivo deste desafio é realizar análises exploratórias em conjuntos de dados públicos disponíveis no BigQuery, responder a perguntas específicas sobre esses dados utilizando SQL e Python, e criar visualizações informativas e visualmente atraentes.

### Conjunto de Dados

Os conjuntos de dados utilizados neste desafio são:

- **Chamados do 1746:** Dados relacionados a chamados de serviços públicos na cidade do Rio de Janeiro. O caminho da tabela é : `datario.administracao_servicos_publicos.chamado_1746`
- **Bairros do Rio de Janeiro:** Dados sobre os bairros da cidade do Rio de Janeiro - RJ. O caminho da tabela é: `datario.dados_mestres.bairro`
- **Ocupação Hoteleira em Grandes Eventos no Rio**: Dados contendo o período de duração de alguns grandes eventos que ocorreram no Rio de Janeiro em 2022 e 2023 e a taxa de ocupação hoteleira da cidade nesses períodos. O caminho da tabela é: `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos`

### Ferramentas e Recursos

Você precisará de acesso ao Google Cloud Platform (GCP) para utilizar o BigQuery e consultar os dados públicos disponíveis no projeto `datario`. Além disso, vamos utilizar a biblioteca `basedosdados` em Python para acessar os dados do BigQuery.

- Tutorial para acessar dados no BigQuery, desde a criação da conta no GCP até consultar os dados utilizando SQL e Python: [Como acessar dados no BigQuery](https://docs.dados.rio/tutoriais/como-acessar-dados/)

### Perguntas do Desafio

As perguntas do desafio estão detalhadas no arquivo `perguntas_desafio.md`.

## Etapas

1. Siga o tutorial acima para criar sua conta no GCP e aprender como utilizar o BigQuery para consultar os dados.
2. Com o Google Cloud Studio e BigQuery já configurados, é possível fazer as consultas disponíveis nos arquivos de resolução de questões (`analise_python.py`, alterando somente o id do projeto no início dos arquivos). A consulta só funcionará mediante a prévia configuração nas plataformas mencionadas e autenticação de conta.