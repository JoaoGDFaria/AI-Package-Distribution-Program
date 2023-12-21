import pandas as pd
from tabulate import tabulate

from Entrega import Entrega


def estudoDeUmaEntrega(lEntr, gr, dtimeStart, pLevantamento, gl, g):

    d = {'Algoritmo': [], 'Tempo execução': [], 'Custo': [], 'Distância percorrida':[], 'Tempo de entrega': [], 'Velocidade mínima': [],
         'Veículo': [], 'Velocidade média': []}
    df = pd.DataFrame(data=d)
    df.at[0, 'Algoritmo'] = "DFS"
    df.at[1, 'Algoritmo'] = "BFS"
    df.at[2, 'Algoritmo'] = "A*"
    df.at[3, 'Algoritmo'] = "Greedy"
    df.at[4, 'Algoritmo'] = "Uniforme"

    Entrega(lEntr.copy(), gr, dtimeStart, pLevantamento, gl, g.procura_DFS, "Algoritmo DFS", df, 0)
    Entrega(lEntr.copy(), gr, dtimeStart, pLevantamento, gl, g.procura_BFS, "Algoritmo BFS", df, 1)
    Entrega(lEntr.copy(), gr, dtimeStart, pLevantamento, gl, g.procura_aStar, "Algoritmo A Estrela", df, 2)
    Entrega(lEntr.copy(), gr, dtimeStart, pLevantamento, gl, g.greedy, "Algoritmo Greedy", df, 3)
    Entrega(lEntr.copy(), gr, dtimeStart, pLevantamento, gl, g.procura_UCS, "Algoritmo Uniforme", df, 4)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    df_sorted = df.sort_values(by='Tempo execução')
    table_str = tabulate(df_sorted, headers='keys', tablefmt='pretty', showindex=False)
    print(table_str)
