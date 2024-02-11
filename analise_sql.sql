## Localização de chamados do 1746
#### Utilize a tabela de Chamados do 1746 e a tabela de Bairros do Rio de Janeiro para as perguntas de 1-5.

#1. Quantos chamados foram abertos no dia 01/04/2023?
SELECT COUNT (*) AS total_chamados
FROM `datario.administracao_servicos_publicos.chamado_1746` 
WHERE data_particao = '2023-04-01' 
#No dia 01/04/2023 foram abertos 65.938

#2. Qual o tipo de chamado que teve mais reclamações no dia 01/04/2023?
#3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?
#4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?
#5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?