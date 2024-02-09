# Desafio Técnico - Cientista de Dados Júnior

## Descrição

Bem-vindo ao desafio técnico para a vaga de Cientista de Dados Júnior no Escritório Municipal de Dados do Rio de Janeiro! Este desafio tem o objetivo de avaliar suas habilidades técnicas em manipulação de dados, consulta SQL, análise de dados e visualização de dados utilizando ferramentas como BigQuery e Python. A **data limite** do seu último commit no repositório é de **25/02/2024 às 23:59 UTC-3**.

### Objetivo

O objetivo deste desafio é realizar análises exploratórias em conjuntos de dados públicos disponíveis no BigQuery, responder a perguntas específicas sobre esses dados utilizando SQL e Python, e criar visualizações informativas e visualmente atraentes.

#### Observação

É esperado que você possa não ter tido contato prévio com algumas das tecnologias solicitadas no desafio, e isso é intencional. Parte da avaliação consiste em verificar se você é capaz de aprender rapidamente e produzir resultados após estudar as tecnologias por algum tempo. Por essa razão, o desafio tem uma duração de 15 dias, permitindo que você tenha tempo para estudar e aprender antes de enviar suas respostas.

### Conjunto de Dados

Os conjuntos de dados que serão utilizados neste desafio são:

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
2. Faça um fork desse repositório.
3. Utilize SQL para resolver todas as questões contidas no arquivo `perguntas_desafio.md` no BigQuery. Salve suas respostas em um arquivo `analise_sql.sql`.
4. Utilize Python e pandas para resolver todas as questões contidas no arquivo `perguntas_desafio.md`. Salve suas respostas em um arquivo `analise_python.sql`. Para acessar os dados do BigQuery no python, siga o tutorial acima e utilize a biblioteca `basedosdados`.
6. Utilize o LookerStudio, Power BI, StreamLit, Tableau ou qualquer outra ferramenta de visualização de sua preferência para criar visualizações informativas dos dados das 3 tabelas. Suas visualizações não precisam se limitar apenas aos resultados das análises; é encorajado que você explore os dados e crie visualizações interessantes sobre eles.
7. Faça commits incrementais à medida que trabalha no desafio e, finalmente, faça push do seu código para o seu repositório no GitHub. Seu repositório deve conter um README com todos os passos necessários para rodar seu código e ver a visualização de dados que você criou.

### Dúvidas

Se tiver alguma dúvida ou precisar de esclarecimentos adicionais sobre o desafio, entre em contato pelo email escritoriodedados@gmail.com.

Boa sorte e estamos ansiosos para ver suas soluções! 

---

**Escritório de Dados**  
**Prefeitura da Cidade do Rio de Janeiro**

