from datetime import datetime
from time import perf_counter
import pandas as pd
from tabulate import tabulate
from Cliente import Cliente


def estudoDeUmaEntrega(pontoslevantamento, gl, g, ag):

    d = {'Algoritmo': [], 'Tempo execução': []}
    df = pd.DataFrame(data=d)

    df.at[0, 'Algoritmo'] = "DFS"
    df.at[1, 'Algoritmo'] = "BFS"
    df.at[2, 'Algoritmo'] = "Uniforme"
    df.at[3, 'Algoritmo'] = "Greedy"
    df.at[4, 'Algoritmo'] = "A*"


    cliente1 = Cliente("João", "Nine", gl)
    cliente2 = Cliente("Ana", "Fradelos", gl)
    cliente3 = Cliente("António", "Bairro", gl)
    cliente4 = Cliente("AA", "Famalicão", gl)


    datetimeStart = datetime(year=2023, month=11, day=22, hour=18, minute=30)
    datetimeFinish1 = datetime(year=2023, month=11, day=22, hour=18, minute=31)
    datetimeFinish2 = datetime(year=2023, month=11, day=22, hour=22, minute=30)
    datetimeFinish3 = datetime(year=2023, month=11, day=22, hour=23, minute=30)
    datetimeFinish4 = datetime(year=2023, month=12, day=22, hour=22, minute=30)


    all_algorithms = [g.procura_DFS, g.procura_BFS, g.procura_UCS, g.greedy, g.procura_aStar]
    fileNames = ["1.DFS","2.BFS","3.Uniforme","4.Greedy","5.aStar"]
    for i in range(5):
        start_time = perf_counter()


        cliente1.criarEncomenda(peso=99, preco=54.23, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish1, pontosRecolha=pontoslevantamento, g=g, ag=ag, algoritmo=all_algorithms[i], fileName=fileNames[i])
        cliente2.criarEncomenda(peso=1, preco=10, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish2, pontosRecolha=pontoslevantamento, g=g, ag=ag, algoritmo=all_algorithms[i], fileName=fileNames[i])
        cliente3.criarEncomenda(peso=1, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish3, pontosRecolha=pontoslevantamento, g=g, ag=ag, algoritmo=all_algorithms[i], fileName=fileNames[i])
        cliente4.criarEncomenda(peso=10, preco=5.23, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish1, pontosRecolha=pontoslevantamento, g=g, ag=ag, algoritmo=all_algorithms[i], fileName=fileNames[i])
        cliente1.criarEncomenda(peso=1, preco=55, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish4, pontosRecolha=pontoslevantamento, g=g, ag=ag, algoritmo=all_algorithms[i], fileName=fileNames[i])

        #ag.imprimirEncomendas()

        ag.agruparPorEstafeta(all_algorithms[i])
        #gl.printAllGlobal()

        #print("ENTREIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n\n\n")


        timeTaken = f"{(perf_counter() - start_time) * 1000 :.2f}"
        df.at[i, 'Tempo execução'] = f"{timeTaken} ms"


    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    df_sorted = df.sort_values(by='Tempo execução')
    table_str = tabulate(df_sorted, headers='keys', tablefmt='pretty', showindex=False)
    print(table_str)
