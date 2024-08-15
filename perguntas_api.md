## Integração com APIs: Feriados e Tempo

### Utilize as APIs públicas abaixo para responder às questões 1-8:
- [Public Holiday API](https://date.nager.at/Api)
- [Open-Meteo Historical Weather API](https://open-meteo.com/)

1. **Quantos feriados há no Brasil em todo o ano de 2024?**

2. **Qual mês de 2024 tem o maior número de feriados?**

3. **Quantos feriados em 2024 caem em dias de semana (segunda a sexta-feira)?**

4. **Qual foi a temperatura média em cada mês?**  
   Utilize a Open-Meteo Historical Weather API para obter as temperaturas médias diárias no Rio de Janeiro de 01/01/2024 a 01/08/2024.  
   
5. **Qual foi o tempo predominante em cada mês nesse período?**  
   Utilize como referência para o código de tempo (_weather_code_) o seguinte link: [WMO Code](https://gist.github.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c).

6. **Qual foi o tempo e a temperatura média em cada feriado de 01/01/2024 a 01/08/2024?**

7. **Considere as seguintes suposições:**
   - O cidadão carioca considera "frio" um dia cuja temperatura média é menor que 20ºC;
   - Um feriado bem aproveitado no Rio de Janeiro é aquele em que se pode ir à praia;
   - O cidadão carioca só vai à praia quando não está com frio;
   - O cidadão carioca também só vai à praia em dias com sol, evitando dias **totalmente** nublados ou chuvosos (considere _weather_code_ para determinar as condições climáticas).

   Houve algum feriado "não aproveitável" em 2024? Se sim, qual(is)?

8. **Qual foi o feriado "mais aproveitável" de 2024?**  
   Considere o melhor par tempo e temperatura.
