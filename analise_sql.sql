#Pergunta 01
SELECT 
  COUNT(id_chamado) AS qtd_chamados #Fazendo contagem das chamadas pelo id e renomeando
FROM datario.adm_central_atendimento_1746.chamado #Descrevendo a tabela na qual farei a busca
WHERE DATE(data_inicio) = '2023-04-01'; #Filtrando a data pela coluna data_inicio. Como a data possui horas, optei pelo comando DATE() para considerar apenas a data.

#Pergunta 02
SELECT 
  tipo, #Adicionando a coluna 'tipo' a consulta
  COUNT(id_chamado) AS qtd_chamados
FROM datario.adm_central_atendimento_1746.chamado
WHERE DATE(data_inicio) = '2023-04-01'
GROUP BY tipo #Agrupando a qtd_chamados pelo 'tipo'
ORDER BY qtd_chamados DESC #Ordenando de maneira decrescente
LIMIT 1; #Limitando a primeira linha (linha com maior qtd de observações)

#Pergunta 03
SELECT 
  tb_bairro.nome, #Descrevendo as colunas a serem exibidas
  COUNT(tb_chamado.id_chamado) AS qtd_chamados
FROM datario.adm_central_atendimento_1746.chamado tb_chamado #Chamando a tabela na qual a busca deve ser feita por outro nome para facilitar
JOIN datario.dados_mestres.bairro tb_bairro #Mesclando a tabela com o nome dos bairros à tabela principal
  ON tb_chamado.id_bairro = tb_bairro.id_bairro #Descrevendo qual coluna será utilizada para fazer a ligação
WHERE DATE(tb_chamado.data_inicio) = '2023-04-01' #Filtrando a data
GROUP BY tb_bairro.nome #Agrupando os resultados por bairro
ORDER BY qtd_chamados DESC #Ordenando os bairros por qtd de chamado
LIMIT 3; #Exibindo apenas o top 3

#Pergunta 04
SELECT #Análogo ao problema anterior 
  tb_bairro.subprefeitura,
  COUNT(tb_chamado.id_chamado) AS qtd_chamados
FROM datario.adm_central_atendimento_1746.chamado tb_chamado
JOIN datario.dados_mestres.bairro tb_bairro
  ON tb_chamado.id_bairro = tb_bairro.id_bairro
WHERE DATE(tb_chamado.data_inicio) = '2023-04-01'
GROUP BY tb_bairro.subprefeitura
ORDER BY qtd_chamados DESC
LIMIT 1;

#Pergunta 05
SELECT 
  tb_chamado #COUNT(tb_chamado.id_chamado) AS qtd_chamados_sem_associacao
FROM datario.adm_central_atendimento_1746.chamado tb_chamado
LEFT JOIN datario.dados_mestres.bairro tb_bairro
  ON tb_chamado.id_bairro = tb_bairro.id_bairro #Utilizei o LEFT JOIN porque os dados de 'subprefeitura' estavam em uma tabela distinta (bairro) e utilizando o JOIN eu teria a correspondência apenas para as linhas com bairro preenchido
WHERE DATE(tb_chamado.data_inicio) = '2023-04-01'
  AND (tb_bairro.id_bairro IS NULL OR tb_bairro.subprefeitura IS NULL); #Selecionando linhas em branco para bairro ou subprefeitura

#Aparentemente, essas linhas não possuem bairro por serem chamados ligados a transportes ou problemas online, não possuindo logradouro.

#Pergunta 06
SELECT 
  COUNT(id_chamado) AS qtd_chamados_perturbacao_sossego
FROM datario.adm_central_atendimento_1746.chamado
WHERE DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31' #Comando BETWEEN para incluir as extremidades do intervalo de datas
  AND subtipo = 'Perturbação do sossego'; #Filtrando o subtipo também para incluir apenas Perturbação do Sossego

#Pergunta 07
SELECT 
  DISTINCT tb_chamado.id_chamado, #Apenas id's distintos
  tb_eventos.evento,
  tb_chamado.* #Selecionando todas as colunas da tabela de chamados e o nome do evento
FROM datario.adm_central_atendimento_1746.chamado tb_chamado
JOIN datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos tb_eventos #que nome de tabela grande viu
  ON DATE(data_inicio) BETWEEN tb_eventos.data_inicial AND tb_eventos.data_final #Realizando o JOIN pelas datas dos eventos listados na questão
WHERE DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31' #Análogo ao problema anterior 
  AND subtipo = 'Perturbação do sossego';

#Pergunta 08
SELECT 
  tb_eventos.evento,
  COUNT(DISTINCT id_chamado) AS qtd_chamados_perturbacao_sossego #Contando os ids distintos
FROM datario.adm_central_atendimento_1746.chamado tb_chamado
JOIN datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos tb_eventos 
  ON DATE(data_inicio) BETWEEN tb_eventos.data_inicial AND tb_eventos.data_final
WHERE DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31' 
  AND subtipo = 'Perturbação do sossego' #Até aqui tudo similar ao problema anterior
GROUP BY evento #Adicionar o GROUP BY na consulta anterior já resolve o nosso problema
ORDER BY qtd_chamados_perturbacao_sossego DESC
LIMIT 1; #Rock in Rio o inimigo da paz (?)

#Pergunta 09
WITH EventosContados AS ( #Realizei duas subconsultas para facilitar
  SELECT #A primeira retorna os chamados e dias de evento ocorrido para cada evento em cada intervalo de datas
    evento,
    data_final,
    data_inicial,
    COUNT(DISTINCT tb_chamado.id_chamado) AS total_chamados,
    DATE_DIFF(data_final, data_inicial, DAY) + 1 AS dias_evento #somano 1 para indluir o dia
  FROM datario.adm_central_atendimento_1746.chamado tb_chamado
    JOIN datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos tb_eventos 
        ON DATE(tb_chamado.data_inicio) BETWEEN tb_eventos.data_inicial AND tb_eventos.data_final #Mesclando pela data dos eventos
    WHERE DATE(tb_chamado.data_inicio) BETWEEN '2022-01-01' AND '2023-12-31' #Apenas esse intervalo de data
      AND tb_chamado.subtipo = 'Perturbação do sossego' #Filtrando o chamado
  GROUP BY evento, data_final, data_inicial #Agrupando
),
DiasEvento AS (
  SELECT #A segunda consulta foi para calcular o total de dias corridos e chamados em cada evento
    ec.evento,
    SUM(ec.dias_evento) AS tot_dias_evento,
    SUM(ec.total_chamados) AS tot_chamados_evento
  FROM EventosContados ec
  GROUP BY ec.evento
)
SELECT 
    DISTINCT de.evento, #Selecionando colunas únicas, pois eventos com mais de uma data aparecerão repetidos (Rock in Rio)
    de.tot_chamados_evento/de.tot_dias_evento AS chamados_perturbacao_diarios, #Calculando a média por evento
FROM DiasEvento de
ORDER BY chamados_perturbacao_diarios DESC
LIMIT 1; #Ordenando para ver o com maior número de chamados
#Rock in Rio campeão

#Pergunta 10
WITH EventosContados AS ( #Realizando uma subconsulta para calcular os chamados por evento
  SELECT #Basicamente a consulta anterior
    evento,
    data_final,
    data_inicial,
    COUNT(DISTINCT tb_chamado.id_chamado) AS total_chamados,
    DATE_DIFF(data_final, data_inicial, DAY) + 1 AS dias_evento
  FROM datario.adm_central_atendimento_1746.chamado tb_chamado
    JOIN datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos tb_eventos 
        ON DATE(tb_chamado.data_inicio) BETWEEN tb_eventos.data_inicial AND tb_eventos.data_final
    WHERE DATE(tb_chamado.data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
      AND tb_chamado.subtipo = 'Perturbação do sossego'
  GROUP BY evento, data_final, data_inicial
),
DiasEvento AS (
  SELECT #A segunda consulta foi para calcular o total de dias corridos em cada evento
    ec.evento,
    SUM(ec.dias_evento) AS tot_dias_evento,
    SUM(ec.total_chamados) AS tot_chamados_evento
  FROM EventosContados ec
  GROUP BY ec.evento
),
TotalChamados AS ( #Subconsulta para contabilizar o total de chamados no intervalo de datas
    SELECT 
        COUNT(tb_chamado.id_chamado) AS total_chamados_geral,
        DATE_DIFF(MAX(tb_chamado.data_inicio),MIN(tb_chamado.data_inicio), DAY) + 1 AS total_dias_geral #Somando 1 pra incruir extremidades
    FROM datario.adm_central_atendimento_1746.chamado tb_chamado
    WHERE DATE(tb_chamado.data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
      AND tb_chamado.subtipo = 'Perturbação do sossego'
)
SELECT 
    DISTINCT de.evento, #Selecionando colunas únicas, pois eventos com mais de uma data aparecerão repetidos
    de.tot_chamados_evento/de.tot_dias_evento AS chamados_perturbacao_diarios, #Calculando a média por evento
    tc.total_chamados_geral/tc.total_dias_geral AS media_total_chamados_por_dia #Calculando a média por dia geral
FROM EventosContados ec
CROSS JOIN TotalChamados tc #Mesclando as duas tabelas sem relação alguma para ver o resultado em uma única consulta
JOIN DiasEvento de
  ON ec.evento = de.evento
ORDER BY chamados_perturbacao_diarios DESC; #Ordenando pra ficar bonitinho e mais visual o top eventos com mais reclamações