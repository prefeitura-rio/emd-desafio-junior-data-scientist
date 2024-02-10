## Localização de chamados do 1746
#### Utilize a tabela de Chamados do 1746 e a tabela de Bairros do Rio de Janeiro para as perguntas de 1-5.

1. Quantos chamados foram abertos no dia 01/04/2023?
    ```sql
    SELECT COUNT(*) AS total_chamados
    FROM `datario.administracao_servicos_publicos.chamado_1746`
    WHERE data_inicio >= "2023-04-01"
    AND data_inicio < "2023-04-02"
    AND data_particao = "2023-04-01"
    ```
2. Qual o tipo de chamado que teve mais reclamações no dia 01/04/2023?
    ```sql
    SELECT tipo,
        COUNT(*) AS total_chamados
    FROM `datario.administracao_servicos_publicos.chamado_1746`
    WHERE data_inicio >= "2023-04-01"
    AND data_inicio < "2023-04-02"
    AND data_particao = "2023-04-01"
    GROUP BY tipo
    ORDER BY total_chamados DESC
    LIMIT 1
    ```
3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?
    ```sql
    WITH chamados_bairros AS (
        SELECT id_bairro,
            COUNT(*) AS total_chamados
        FROM `datario.administracao_servicos_publicos.chamado_1746`
        WHERE data_inicio >= "2023-04-01"
        AND data_inicio < "2023-04-02"
        AND data_particao = "2023-04-01"
        GROUP BY id_bairro
        ORDER BY total_chamados DESC
        LIMIT 3
    )
    SELECT bairro.nome
    FROM chamados_bairros, `datario.dados_mestres.bairro` AS bairro
    WHERE bairro.id_bairro = chamados_bairros.id_bairro
    ORDER BY total_chamados DESC
    ```
4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?
    ```sql
    SELECT bairro.subprefeitura,
           COUNT(*) AS total_chamados
    FROM `datario.administracao_servicos_publicos.chamado_1746` AS chamado_1746
    JOIN `datario.dados_mestres.bairro` AS bairro ON chamado_1746.id_bairro = bairro.id_bairro
    WHERE data_inicio >= "2023-04-01"
    AND data_inicio < "2023-04-02"
    AND data_particao = "2023-04-01"
    GROUP BY bairro.subprefeitura
    ORDER BY total_chamados DESC
    LIMIT 1
    ```
5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?
    ```sql
    SELECT categoria,
        tipo,
        subtipo
    FROM `datario.administracao_servicos_publicos.chamado_1746`
    WHERE data_inicio >= "2023-04-01"
    AND data_inicio < "2023-04-02"
    AND data_particao = "2023-04-01"
    AND id_bairro IS NULL
    ```

## Chamados do 1746 em grandes eventos
#### Utilize a tabela de Chamados do 1746 e a tabela de Ocupação Hoteleira em Grandes Eventos no Rio para as perguntas de 6-10. Para todas as perguntas considere o subtipo de chamado "Perturbação do sossego".

6. Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?
7. Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).
8. Quantos chamados desse subtipo foram abertos em cada evento?
9. Qual evento teve a maior média diária de chamados abertos desse subtipo?
10. Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.

##### Importante: a tabela de Chamados do 1746 possui mais de 10M de linhas. Evite fazer consultas exploratórias na tabela sem um filtro ou limite de linhas para economizar sua cota no BigQuery!
