import pandas as pd
from tabulate import tabulate
import info
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



def escolherEncomendas(gl, g, pontosRecolha):
    (l_bicicleta, l_mota, l_carro) = gl.get_encomendas_sem_entregador()

    calcularVeiculo("bicicleta", gl, g, l_bicicleta, pontosRecolha)
    #calcularVeiculo("mota", gl, g, l_mota, pontosRecolha)
    #calcularVeiculo("carro", gl, g, l_carro, pontosRecolha)


def calcularVeiculo(veiculo, gl, g, lista, pontosRecolha):

    all_subconjuntos = gl.get_all_subsets(lista)

    for conjunto in all_subconjuntos:
        peso_total = 0

        for enc in conjunto:
            peso_total += enc.peso
            if peso_total > info.infoPesoMaximo[veiculo]:
                all_subconjuntos.remove(conjunto)
                break

    for a in all_subconjuntos:
        print("-------------------------")
        for aa in a:
            print(aa.idCliente)

    for listaEncomendas in all_subconjuntos[::-1]:
        print(type(all_subconjuntos))
        entrega = Entrega(listaEncomendas, g, listaEncomendas[0].tempoInicio, pontosRecolha, gl, None, None, None, None)
        flag = entrega.melhorCaminho2(g.procura_BFS, veiculo)
        print("AAAAAAAAAAAAAAAAAAAAAAAAA")
        if flag is True:
            escolherEncomendas(gl, g, pontosRecolha)

