# Green-Software-Developer

## Alteração do ficheiro `measure.sh`
Esta alteração para permitiu a compilação automática de vários inputs (inseridos manualmente num array), com flags de otimização (no caso, apenas utilizei a linguagem C) e são feitas as avaliações com a biblioteca RAPL fornecida pela equipa docente.


## Criação de ficheiro Python
Decidi simplificar a impressão de inúmeros gráficos utilizando o matplotlib através do ficheiro measurements.csv. O ficheiro separa linguagens diferentes, de programas diferentes, de inputs diferentes e agrega a informação de forma a um ser humano poder intrepertar um gráfico que compara os valores obtidos dos vários programas, acerca da mesma variável de avaliação (energia, memória, tempo, etc).

## Como utilizar?
Dentro da diretoria RAPL_Measurements, executar:
```sudo bash measure.sh```
Irá gerar os vários executáveis e os resultados serão escritos num ficheiro measurements.csv, nesta mesma diretoria. O programa adormece sempre que a temperatura média dos processadores for acima de 36ª Celsius. De seguida, posso executar, na mesma diretoria:
```python3 plots.py ```
E serão gerados todos os gráficos utilizados nos slides dentro de uma pasta chamada **Plots**.