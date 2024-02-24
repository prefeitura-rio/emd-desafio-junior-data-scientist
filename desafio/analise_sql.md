## Localização de chamados do 1746

1. Quantos chamados foram abertos no dia 01/04/2023?
    ```sql
    SELECT COUNT(*) AS total_chamados
    FROM `datario.administracao_servicos_publicos.chamado_1746`
    WHERE DATE(data_inicio) = "2023-04-01"
    AND data_particao = "2023-04-01"
    ```
    | total_chamados |
    | -------------- |
    | 73            |
2. Qual o tipo de chamado que teve mais reclamações no dia 01/04/2023?
    ```sql
    SELECT tipo,
        COUNT(*) AS total_chamados
    FROM `datario.administracao_servicos_publicos.chamado_1746`
    WHERE DATE(data_inicio) = "2023-04-01"
    AND data_particao = "2023-04-01"
    GROUP BY tipo
    ORDER BY total_chamados DESC
    LIMIT 1
    ```
    | tipo | total_chamados |
    | ---- | -------------- |
    | Poluição sonora | 24 |
3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?
    ```sql
    WITH chamados_bairros AS (
        SELECT id_bairro,
            COUNT(*) AS total_chamados
        FROM `datario.administracao_servicos_publicos.chamado_1746`
        WHERE DATE(data_inicio) = "2023-04-01"
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
    | nome |
    | ---- |
    | Engenho de Dentro |
    | Leblon |
    | Campo Grande |
4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?
    ```sql
    SELECT bairro.subprefeitura,
           COUNT(*) AS total_chamados
    FROM `datario.administracao_servicos_publicos.chamado_1746` AS chamado_1746
    JOIN `datario.dados_mestres.bairro` AS bairro ON chamado_1746.id_bairro = bairro.id_bairro
    WHERE DATE(data_inicio) = "2023-04-01"
    AND data_particao = "2023-04-01"
    GROUP BY bairro.subprefeitura
    ORDER BY total_chamados DESC
    LIMIT 1
    ```
    | subprefeitura | total_chamados |
    | ------------- | -------------- |
    | Zona Norte | 25 |
5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?
    ```sql
    SELECT subtipo
    FROM `datario.administracao_servicos_publicos.chamado_1746`
    WHERE DATE(data_inicio) = "2023-04-01"
        AND data_particao = "2023-04-01"
        AND id_bairro IS NULL
    ```
    | subtipo |
    | ------- |
    | Verificação de ar condicionado inoperante no ônibus|

## Chamados do 1746 em grandes eventos

6. Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?
    ```sql
    SELECT
        COUNT(*) AS total_chamados
    FROM
        `datario.administracao_servicos_publicos.chamado_1746`
    WHERE
        subtipo = "Perturbação do sossego"
        AND data_inicio >= "2022-01-01"
        AND data_inicio < "2024-01-01"
        AND data_particao BETWEEN "2022-01-01" AND "2023-12-31"
    ```
    | total_chamados |
    | -------------- |
    | 42.408         |
7. Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).
    ```sql
    SELECT chamados.id_chamado, evento.evento
    FROM `datario.administracao_servicos_publicos.chamado_1746` chamados
    JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` evento
        ON DATE(chamados.data_inicio) BETWEEN evento.data_inicial AND evento.data_final
    WHERE
        chamados.subtipo = "Perturbação do sossego"
        AND chamados.data_particao BETWEEN "2022-01-01" AND "2023-12-31"
        AND evento.evento IN ("Reveillon", "Carnaval", "Rock in Rio")
    ```
    | id_chamado | evento      |
    | ---------- | ----------- |
    | 18078336   | Reveillon   |
    | 17661848   | Rock in Rio |
    | 17682634   | Rock in Rio |
    | ...   | ... |
8. Quantos chamados desse subtipo foram abertos em cada evento?
    ```sql
    SELECT eventos.evento,
        COUNT(*) AS total_chamados
    FROM `datario.administracao_servicos_publicos.chamado_1746` chamados
    JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` eventos ON DATE(chamados.data_inicio) BETWEEN eventos.data_inicial AND eventos.data_final
    WHERE chamados.subtipo = "Perturbação do sossego"
    AND chamados.data_particao BETWEEN "2022-01-01" AND "2023-12-31"
    GROUP BY eventos.evento
    ```
    | evento      | total_chamados |
    | ----------- | -------------- |
    | Rock in Rio | 834            |
    | Carnaval    | 241            |
    | Reveillon   | 137            |

9. Qual evento teve a maior média diária de chamados abertos desse subtipo?
    ```sql
    WITH chamados_data AS(
        SELECT eventos.evento,
            DATE(chamados.data_inicio) AS data_chamado,
            COUNT(*) AS total_chamados
        FROM
            `datario.administracao_servicos_publicos.chamado_1746` chamados
        JOIN
            `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` eventos
        ON
            DATE(chamados.data_inicio) BETWEEN eventos.data_inicial AND eventos.data_final
        WHERE
            chamados.subtipo = "Perturbação do sossego"
            AND chamados.data_particao BETWEEN "2022-01-01" AND "2023-12-31"
        GROUP BY
            eventos.evento,
            data_chamado
    )
    SELECT evento,
        AVG(total_chamados) AS media_diaria
    FROM
        chamados_data
    GROUP BY
        evento
    ORDER BY
        media_diaria DESC
    LIMIT 1
    ```
    | evento      | media_diaria |
    | ----------- | ------------ |
    | Rock in Rio | 119.142857...|

10. Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.
    ```sql
    -- Primeira parte: Calculando a média diária de chamados por evento usando a tabela temporária criada na pergunta 9
    SELECT
        evento,
        AVG(total_chamados) AS media_diaria
    FROM
        chamados_data
    GROUP BY
        evento

    -- Segunda parte: Calculando a média diária total de chamados para perturbação do sossego
    UNION ALL

    SELECT
        "Chamados totais" AS evento,
        AVG(total_chamados) AS media_diaria
    FROM
        (
        -- Subconsulta para calcular o número total de chamados por dia para perturbação do sossego
        SELECT
            DATE(data_inicio) AS data_chamado,
            COUNT(*) AS total_chamados
        FROM
            `datario.administracao_servicos_publicos.chamado_1746`
        WHERE
            subtipo = "Perturbação do sossego"
            AND data_inicio >= "2022-01-01"
            AND data_inicio < "2024-01-01"
            AND data_particao BETWEEN "2022-01-01" AND "2023-12-31"
        GROUP BY
            data_chamado
        ) AS total_chamados_perturbacao

    ```
    | evento      | media_diaria |
    | ----------- | ------------ |
    | Chamados totais | 63.2011922...|
    | Rock in Rio | 119.142857...|
    | Reveillon   | 45.6666666... |
    | Carnaval    | 60.25 |
