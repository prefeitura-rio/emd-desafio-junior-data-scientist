import basedosdados as bd

main_path = "datario.administracao_servicos_publicos.chamado_1746"
neighborhood_path = "datario.dados_mestres.bairro"
events_path = "datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos"

quantidade_bairros = f"SELECT COUNT(*) as quantidade FROM {neighborhood_path};"
maiores_bairros = f"SELECT nome, area FROM {neighborhood_path} ORDER BY area DESC LIMIT 5;"
subprefeituras_mais_repetem = f"SELECT subprefeitura, COUNT(*) AS Recorrencia FROM {neighborhood_path} GROUP BY subprefeitura ORDER BY Recorrencia DESC LIMIT 5;"
tipo_chamado_mais_recorrente = f"SELECT tipo, COUNT(*) AS total_ocorrencias FROM {main_path} GROUP BY tipo ORDER BY total_ocorrencias DESC LIMIT 1;"
local_1000_chamados = f"SELECT latitude, longitude FROM {main_path} WHERE latitude IS NOT NULL AND longitude IS NOT NULL LIMIT 1000;"
dia_mais_chamados = f"SELECT COUNT(*) AS total_chamados FROM {main_path} WHERE DATE(data_inicio) = (SELECT DATE(data_inicio) FROM {main_path} GROUP BY DATE(data_inicio) ORDER BY COUNT(*) DESC LIMIT 1);"
quantidade_total_chamados = f"SELECT COUNT(*) AS total_chamados FROM {main_path} ;"

status_desejados = ['Fechado com solução', 'Em andamento', 'Fechado com providências', 'Sem possibilidade de atendimento']
consulta_chamados_por_status = f"SELECT status, COUNT(*) AS total_chamados FROM {main_path} WHERE status IN {tuple(status_desejados)} GROUP BY status"
consulta_tempo_medio_resolucao = f"SELECT AVG(tempo_prazo) AS tempo_medio_resolucao FROM {main_path} WHERE tempo_prazo IS NOT NULL"
trimestres_query = f"""SELECT EXTRACT(YEAR FROM data_inicio) AS ano, CASE
    WHEN EXTRACT(MONTH FROM data_inicio) BETWEEN 1 AND 3 THEN '1º trimestre'
    WHEN EXTRACT(MONTH FROM data_inicio) BETWEEN 4 AND 6 THEN '2º trimestre'
    WHEN EXTRACT(MONTH FROM data_inicio) BETWEEN 7 AND 9 THEN '3º trimestre'
    WHEN EXTRACT(MONTH FROM data_inicio) BETWEEN 10 AND 12 THEN '4º trimestre'
  END AS trimestre,
  COUNT(*) AS total_chamados
FROM
  {main_path}
GROUP BY
  ano,
  trimestre
ORDER BY
  ano,
  trimestre;
"""

eventos_query = f"SELECT DISTINCT evento FROM {events_path};"
media_taxa = f"SELECT evento, AVG(taxa_ocupacao) AS media_taxa_ocupacao FROM {events_path} GROUP BY evento;"
consulta_chamado_por_evento = f"SELECT eventos.evento, COUNT(chamados.id_chamado) AS num_chamados FROM {main_path} AS chamados JOIN {events_path} AS eventos ON chamados.data_inicio >= eventos.data_inicial AND chamados.data_inicio <= eventos.data_final GROUP BY eventos.evento;"
chamados_mais_recorrentes = f"SELECT tipo, COUNT(*) AS total_ocorrencias FROM {main_path} WHERE DATE(data_inicio) = '2023-04-01' GROUP BY tipo ORDER BY total_ocorrencias DESC LIMIT 1;"
total_chamados_na_data = f"SELECT COUNT(*) AS total_chamados_abertos FROM {main_path} WHERE DATE(data_inicio) = '2023-04-01';"
localizacao_3_ocorrencia_chamado = f"""
SELECT nome 
FROM {neighborhood_path} 
WHERE id_bairro IN (
    SELECT id_bairro
    FROM (
        SELECT id_bairro, COUNT(*) AS recorrencia_bairro 
        FROM {main_path} 
        WHERE DATE(data_inicio) = '2023-04-01'
        GROUP BY id_bairro 
        ORDER BY recorrencia_bairro DESC 
        LIMIT 3
    )
);
"""