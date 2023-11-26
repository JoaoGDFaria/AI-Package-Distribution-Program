from time import perf_counter
import Graph as gr
import pandas as pd


# TODO Reutilizar código das pesquisas do menu
# TODO Gerar a encomenda e tratar da sua entrega

def main():
    g = gr.Graph()

    df_grafo = pd.read_csv("Files/Grafo/grafo.csv", encoding='utf-8')
    for linha in df_grafo.itertuples(index=False):
        g.add_edge(linha.origem, linha.destino, float(linha.distancia))

    pos = {}
    df_posicoes = pd.read_csv("Files/Grafo/posGrafo.csv", encoding='utf-8')
    for linha in df_posicoes.itertuples(index=False):
        pos[linha.nodo] = (int(linha.x), int(linha.y))

    df_h_grafo = pd.read_csv("Files/Grafo/heristicasGrafo.csv", encoding='utf-8')
    for linha in df_h_grafo.itertuples(index=False):
        g.add_heuristica(linha.nodo, int(linha.heuristica))

    pontoslevantamento = []
    df_postosLevantamento = pd.read_csv("Files/Grafo/postosLevantamento.csv", encoding='utf-8')
    for linha in df_postosLevantamento.itertuples(index=False):
        pontoslevantamento.append(linha.nodo)



    while True:
        print("1-Desenhar Grafo")
        print("2-DFS")
        print("3-BFS")
        print("4-A*")
        print("5-Gulosa")
        print("0-Sair")


        try:

            saida = int(input("Introduza a sua opção-> "))

            if saida == 0:
                print("Saindo .......")
                break

            elif saida == 1:
                g.desenha(pos)

            elif saida == 2:
                auxFunction(g.procura_DFS, pontoslevantamento, g)

            elif saida == 3:
                auxFunction(g.procura_BFS, pontoslevantamento, g)

            elif saida == 4:
                auxFunction(g.procura_aStar, pontoslevantamento, g)

            elif saida == 5:
                auxFunction(g.greedy, pontoslevantamento, g)

            else:
                print("Please insert a valid number")
                input("Prima Enter para continuar")

        except ValueError:
            print("Please insert a valid input")
            input("Prima Enter para continuar")



def auxFunction(algorithmFunction, nodeStops, nodes):

    inicio = input("Nodo inicial-> ")
    if not nodes.node_exists(inicio):
        return

    fim = input("Nodo final-> ")
    if not nodes.node_exists(fim):
        return


    start_time = perf_counter()


    minimumCost = float('inf')
    solucao = None

    for stop in nodeStops:
        path_inicio_stop = algorithmFunction(inicio, stop)
        path_stop_fim = algorithmFunction(stop, fim)

        routeCost = path_inicio_stop[1] + path_stop_fim[1]

        if routeCost < minimumCost:
            solucao = (path_inicio_stop[0] + path_stop_fim[0][1:], "{:.1f}".format(routeCost))
            minimumCost = routeCost


    print(f"Ideal Path: {solucao} | Time taken: {(perf_counter() - start_time) * 1000 :.2f} ms")

    input("Prima Enter para continuar")


if __name__ == "__main__":
    main()

