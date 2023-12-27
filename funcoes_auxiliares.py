from time import perf_counter
import pandas as pd
from tabulate import tabulate
from Estafeta import Estafeta


def estudoDeUmaEntrega(pontoslevantamento, lista_encomenda, datetimeStart, gl, g, ag):
     d = {'Algoritmo': [], 'Tempo execução': []}
     df = pd.DataFrame(data=d)

     df.at[0, 'Algoritmo'] = "DFS"
     df.at[1, 'Algoritmo'] = "BFS"
     df.at[2, 'Algoritmo'] = "Uniforme"
     df.at[3, 'Algoritmo'] = "Greedy"
     df.at[4, 'Algoritmo'] = "A*"

     all_algorithms = [g.procura_DFS, g.procura_BFS, g.procura_UCS, g.greedy, g.procura_aStar]
     fileNames = ["1.DFS", "2.BFS", "3.Uniforme", "4.Greedy", "5.aStar"]


     for i in range(5):
         start_time = perf_counter()

         for enc in lista_encomenda:
             cliente = gl.get_cliente(enc[0])
             cliente.criarEncomenda(peso=enc[1], preco=enc[2], volume=enc[3], tempoInicio=datetimeStart, tempoFim=enc[4],
                                   pontosRecolha=pontoslevantamento, g=g, ag=ag, algoritmo=all_algorithms[i],
                                   fileName=fileNames[i])

         ag.agruparPorEstafeta(all_algorithms[i], fileNames[i])

         gl.deleteAllEncomendas()
         gl.deleteAllEstafetas()

         df_estafetas = pd.read_csv("Files/Utilizadores/estafetas.csv", encoding='utf-8')
         for linha in df_estafetas.itertuples(index=False):
             Estafeta(linha.veiculo, linha.freguesia, linha.nome, linha.rating, linha.numEntregas, gl)


         timeTaken = f"{(perf_counter() - start_time) * 1000 :.2f}"
         df.at[i, 'Tempo execução'] = f"{timeTaken} ms"

     pd.set_option('display.max_rows', None)
     pd.set_option('display.max_columns', None)
     df_sorted = df.sort_values(by='Tempo execução')
     table_str = tabulate(df_sorted, headers='keys', tablefmt='pretty', showindex=False)
     print(table_str)


def estudoDeUmaEntrega2(pontoslevantamento, lista_encomenda, datetimeStart, gl, g, ag, algoritmo, filename, row):
    d = {'Algoritmo': [], 'Tempo execução': []}
    df = pd.DataFrame(data=d)

    df.at[0, 'Algoritmo'] = "DFS"
    df.at[1, 'Algoritmo'] = "BFS"
    df.at[2, 'Algoritmo'] = "Uniforme"
    df.at[3, 'Algoritmo'] = "Greedy"
    df.at[4, 'Algoritmo'] = "A*"

    start_time = perf_counter()

    for enc in lista_encomenda:
        cliente = gl.get_cliente(enc[0])
        cliente.criarEncomenda(peso=enc[1], preco=enc[2], volume=enc[3], tempoInicio=datetimeStart, tempoFim=enc[4],
                                pontosRecolha=pontoslevantamento, g=g, ag=ag, algoritmo=algoritmo,
                                fileName=filename)

        ag.agruparPorEstafeta(algoritmo, filename)


        timeTaken = f"{(perf_counter() - start_time) * 1000 :.2f}"
        df.at[row, 'Tempo execução'] = f"{timeTaken} ms"

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    df_sorted = df.sort_values(by='Tempo execução')
    table_str = tabulate(df_sorted, headers='keys', tablefmt='pretty', showindex=False)
    print(table_str)
