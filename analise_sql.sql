# Quantos chamados foram abertos no dia 01/04/2023?
# R: 73

SELECT 
  COUNT(*) as total
FROM  
  datario.administracao_servicos_publicos.chamado_1746
WHERE
  data_inicio >= '2023-04-01' 
  AND data_inicio < '2023-04-02';

# Qual o tipo de chamado que teve mais reclamações no dia 01/04/2023?
# R: 24

SELECT 
  tipo,
  COUNT(*) AS total_reclamacoes
FROM  
  datario.administracao_servicos_publicos.chamado_1746
WHERE
  data_inicio >= '2023-04-01' 
  AND data_inicio < '2023-04-02'
  AND tipo IS NOT NULL
GROUP BY 
  tipo
ORDER BY 
  total_reclamacoes DESC
LIMIT 1;

# Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?
# R: 1 - Engenho de Dentro - 8, 2 - Leblon - 6, 3 - Campo Grande - 6

SELECT 
  bairro.nome AS nome_bairro,
  COUNT(*) AS total_chamados
FROM  
  datario.administracao_servicos_publicos.chamado_1746 chamado
JOIN 
  datario.dados_mestres.bairro bairro ON chamado.id_bairro = bairro.id_bairro
WHERE
  chamado.data_inicio >= '2023-04-01' 
  AND chamado.data_inicio < '2023-04-02'
GROUP BY 
  nome_bairro
ORDER BY 
  total_chamados DESC
LIMIT 3;


# Qual o nome da subprefeitura com mais chamados abertos nesse dia?
# R: Zona Norte - 25

SELECT 
  bairro.subprefeitura AS subprefeitura,
  COUNT(*) AS total_chamados
FROM  
  datario.administracao_servicos_publicos.chamado_1746 chamado
JOIN 
  datario.dados_mestres.bairro bairro ON chamado.id_bairro = bairro.id_bairro
WHERE
  chamado.data_inicio >= '2023-04-01' 
  AND chamado.data_inicio < '2023-04-02'
GROUP BY 
  subprefeitura
ORDER BY 
  total_chamados DESC
LIMIT 1;

# Existe algum chamado aberto nesse dia que não foi associado a um bairro ou   subprefeitura na tabela de bairros? Se sim, por que isso acontece?
# R: Acontece por motivos de dados ausentes (null)

SELECT 
  chamado.id_chamado,
  chamado.data_inicio
FROM  
  datario.administracao_servicos_publicos.chamado_1746 chamado
LEFT JOIN 
  datario.dados_mestres.bairro bairro ON chamado.id_bairro = bairro.id_bairro
WHERE
  chamado.data_inicio >= '2023-04-01' 
  AND chamado.data_inicio < '2023-04-02'
  AND bairro.id_bairro IS NULL;

# Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?
# R: 42408

SELECT 
  COUNT(*) AS total_chamados
FROM  
  datario.administracao_servicos_publicos.chamado_1746 chamado
WHERE
  chamado.subtipo = 'Perturbação do sossego'
  AND chamado.data_inicio >= '2022-01-01' 
  AND chamado.data_inicio <= '2023-12-31';

# Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).

SELECT 
  chamado.*
FROM  
  datario.administracao_servicos_publicos.chamado_1746 chamado
JOIN
  datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos evento
ON
  chamado.data_inicio >= evento.data_inicial
  AND chamado.data_inicio <= evento.data_final
WHERE
  chamado.subtipo = 'Perturbação do sossego'
  AND evento.evento IN ('Reveillon', 'Carnaval', 'Rock in Rio');

# Quantos chamados desse subtipo foram abertos em cada evento?
# R: Rock in Rio - 518, Reveillon - 79, Carnaval - 197

SELECT 
  eventos.evento,
  COUNT(chamado.id_chamado) AS total_chamados
FROM  
  datario.administracao_servicos_publicos.chamado_1746 chamado
JOIN
  datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos eventos
ON
  chamado.data_inicio >= eventos.data_inicial
  AND chamado.data_inicio <= eventos.data_final
WHERE
  chamado.subtipo = 'Perturbação do sossego'
  AND eventos.evento IN ('Reveillon', 'Carnaval', 'Rock in Rio')
GROUP BY
eventos.evento;

# Qual evento teve a maior média diária de chamados abertos desse subtipo?
# R: Rock in Rio - 73.58

WITH EventosChamados AS (
  SELECT 
    eventos.evento,
    DATE_DIFF(eventos.data_final, eventos.data_inicial, DAY) + 1 AS duracao_evento,
    COUNT(chamado.id_chamado) AS total_chamados
  FROM  
    datario.administracao_servicos_publicos.chamado_1746 chamado
  JOIN
    datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos eventos
  ON
    chamado.data_inicio >= eventos.data_inicial
    AND chamado.data_inicio <= eventos.data_final
  WHERE
    chamado.subtipo = 'Perturbação do sossego'
    AND eventos.evento IN ('Reveillon', 'Carnaval', 'Rock in Rio')
  GROUP BY
    eventos.evento, eventos.data_inicial, eventos.data_final
)

SELECT 
  evento,
  AVG(total_chamados / duracao_evento) AS media_diaria_chamados
FROM
  EventosChamados
GROUP BY
  evento
ORDER BY
  media_diaria_chamados DESC
LIMIT 1;

# Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.
# R: Período Geral - ~58, Reveillon - ~26, Rock in Rio - ~74, Carnaval - ~49

WITH MediasDiarias AS (
  SELECT 
    eventos.evento,
    DATE_DIFF(eventos.data_final, eventos.data_inicial, DAY) + 1 AS duracao_evento,
    COUNT(chamado.id_chamado) AS total_chamados
  FROM  
    datario.administracao_servicos_publicos.chamado_1746 chamado
  JOIN
    datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos eventos
  ON
    chamado.data_inicio >= eventos.data_inicial
    AND chamado.data_inicio <= eventos.data_final
  WHERE
    chamado.subtipo = 'Perturbação do sossego'
    AND eventos.evento IN ('Reveillon', 'Carnaval', 'Rock in Rio')
  GROUP BY
    eventos.evento, eventos.data_inicial, eventos.data_final
),

MediaDiariaGeral AS (
  SELECT 
    DATE_DIFF('2023-12-31', '2022-01-01', DAY) + 1 AS duracao_periodo,
    COUNT(chamado.id_chamado) AS total_chamados
  FROM  
    datario.administracao_servicos_publicos.chamado_1746 chamado
  WHERE
    chamado.subtipo = 'Perturbação do sossego'
    AND chamado.data_inicio >= '2022-01-01' 
    AND chamado.data_inicio <= '2023-12-31'
)

SELECT 
  'Evento Específico' AS tipo,
  evento AS nome_evento,
  AVG(total_chamados / duracao_evento) AS media_diaria_chamados
FROM
  MediasDiarias
GROUP BY
  evento

UNION ALL

SELECT 
  'Período Geral' AS tipo,
  'Todo o Período' AS nome_evento,
  AVG(total_chamados / duracao_periodo) AS media_diaria_chamados
FROM
  MediaDiariaGeral;
