from time import perf_counter
import Graph as gr
import pandas as pd


#TODO Reutilizar código das pesquisas do menu
#TODO Gerar a encomenda e tratar da sua entrega

def main():

    g = gr.Graph()

    df_grafo = pd.read_csv("files/Grafo/grafo.csv", encoding='utf-8')
    for linha in df_grafo.itertuples(index=False):
        g.add_edge(linha.origem, linha.destino, float(linha.distancia))


    pos = {}
    df_posicoes = pd.read_csv("files/Grafo/posGrafo.csv", encoding='utf-8')
    for linha in df_posicoes.itertuples(index=False):
        pos[linha.nodo] = (int(linha.x), int(linha.y))


    df_h_grafo = pd.read_csv("files/Grafo/heristicasGrafo.csv", encoding='utf-8')
    for linha in df_h_grafo.itertuples(index=False):
        g.add_heuristica(linha.nodo, int(linha.heuristica))


    pontoslevantamento = []
    df_postosLevantamento = pd.read_csv("files/Grafo/postosLevantamento.csv", encoding='utf-8')
    for linha in df_postosLevantamento.itertuples(index=False):
        pontoslevantamento.append(linha.nodo)



    saida = -1
    while saida != 0:
        print("1-Desenhar Grafo")
        print("2-DFS")
        print("3-BFS")
        print("4-A*")
        print("5-Gulosa")
        print("0-Sair")

        saida = int(input("Introduza a sua opção-> "))

        if saida == 0:
            print("Saindo .......")


        elif saida == 1:
            g.desenha(pos)


        elif saida == 2:

            inicio = input("Nodo inicial-> ")
            if not g.node_exists(inicio): continue
            fim = input("Nodo final-> ")
            if not g.node_exists(fim): continue

            start_time = perf_counter()

            path_inicio_calendario = g.procura_DFS(inicio, "Calendário", path=[], visited=set())
            path_calendario_fim = g.procura_DFS("Calendário", fim, path=[], visited=set())

            path_inicio_casteloes = g.procura_DFS(inicio, "Castelões", path=[], visited=set())
            path_casteloes_fim = g.procura_DFS("Castelões", fim, path=[], visited=set())

            path_inicio_maximinos = g.procura_DFS(inicio, "Maximinos", path=[], visited=set())
            path_maximinos_fim = g.procura_DFS("Maximinos", fim, path=[], visited=set())

            calendario = path_inicio_calendario[1] + path_calendario_fim[1]
            casteloes = path_inicio_casteloes[1] + path_casteloes_fim[1]
            maximinos = path_inicio_maximinos[1] + path_maximinos_fim[1]

            value = min(calendario, casteloes, maximinos)

            if value == calendario:
                solucao = (path_inicio_calendario[0] + path_calendario_fim[0][1:], "{:.1f}".format(path_inicio_calendario[1] + path_calendario_fim[1]))
            elif value == maximinos:
                solucao = (path_inicio_maximinos[0] + path_maximinos_fim[0][1:], "{:.1f}".format(path_inicio_maximinos[1] + path_maximinos_fim[1]))
            else:
                solucao = (path_inicio_casteloes[0] + path_casteloes_fim[0][1:], "{:.1f}".format(path_inicio_casteloes[1] + path_casteloes_fim[1]))

            print(f"Ideal Path: {solucao} | Time taken: {(perf_counter()-start_time)*1000} ms")

            l = input("Prima Enter para continuar")


        elif saida == 3:

            inicio = input("Nodo inicial-> ")
            if not g.node_exists(inicio): continue
            fim = input("Nodo final-> ")
            if not g.node_exists(fim): continue

            start_time = perf_counter()

            path_inicio_calendario = g.procura_BFS(inicio, "Calendário")
            path_calendario_fim = g.procura_BFS("Calendário", fim)

            path_inicio_casteloes = g.procura_BFS(inicio, "Castelões")
            path_casteloes_fim = g.procura_BFS("Castelões", fim)

            path_inicio_maximinos = g.procura_BFS(inicio, "Maximinos")
            path_maximinos_fim = g.procura_BFS("Maximinos", fim)

            calendario = path_inicio_calendario[1] + path_calendario_fim[1]
            casteloes = path_inicio_casteloes[1] + path_casteloes_fim[1]
            maximinos = path_inicio_maximinos[1] + path_maximinos_fim[1]

            value = min(calendario, casteloes, maximinos)

            if value == calendario:
                solucao = (path_inicio_calendario[0] + path_calendario_fim[0][1:], "{:.1f}".format(path_inicio_calendario[1] + path_calendario_fim[1]))
            elif value == maximinos:
                solucao = (path_inicio_maximinos[0] + path_maximinos_fim[0][1:], "{:.1f}".format(path_inicio_maximinos[1] + path_maximinos_fim[1]))
            else:
                solucao = (path_inicio_casteloes[0] + path_casteloes_fim[0][1:], "{:.1f}".format(path_inicio_casteloes[1] + path_casteloes_fim[1]))


            print(f"Ideal Path: {solucao} | Time taken: {(perf_counter()-start_time)*1000} ms")

            l = input("Prima Enter para continuar")


        elif saida == 4:

            inicio = input("Nodo inicial-> ")
            if not g.node_exists(inicio): continue
            fim = input("Nodo final-> ")
            if not g.node_exists(fim): continue

            start_time = perf_counter()

            path_inicio_calendario = g.procura_aStar(inicio, "Calendário")
            path_calendario_fim = g.procura_aStar("Calendário", fim)

            path_inicio_casteloes = g.procura_aStar(inicio, "Castelões")
            path_casteloes_fim = g.procura_aStar("Castelões", fim)

            path_inicio_maximinos = g.procura_aStar(inicio, "Maximinos")
            path_maximinos_fim = g.procura_aStar("Maximinos", fim)

            calendario = path_inicio_calendario[1] + path_calendario_fim[1]
            casteloes = path_inicio_casteloes[1] + path_casteloes_fim[1]
            maximinos = path_inicio_maximinos[1] + path_maximinos_fim[1]

            value = min(calendario, casteloes, maximinos)

            if value == calendario:
                solucao = (path_inicio_calendario[0] + path_calendario_fim[0][1:],
                           "{:.1f}".format(path_inicio_calendario[1] + path_calendario_fim[1]))
            elif value == maximinos:
                solucao = (path_inicio_maximinos[0] + path_maximinos_fim[0][1:],
                           "{:.1f}".format(path_inicio_maximinos[1] + path_maximinos_fim[1]))
            else:
                solucao = (path_inicio_casteloes[0] + path_casteloes_fim[0][1:],
                           "{:.1f}".format(path_inicio_casteloes[1] + path_casteloes_fim[1]))

            print(f"Ideal Path: {solucao} | Time taken: {(perf_counter()-start_time)*1000} ms")

            l = input("Prima Enter para continuar")

        elif saida == 5:

            inicio = input("Nodo inicial-> ")
            if not g.node_exists(inicio): continue
            fim = input("Nodo final-> ")
            if not g.node_exists(fim): continue

            start_time = perf_counter()

            path_inicio_calendario = g.greedy(inicio, "Calendário")
            path_calendario_fim = g.greedy("Calendário", fim)

            path_inicio_casteloes = g.greedy(inicio, "Castelões")
            path_casteloes_fim = g.greedy("Castelões", fim)

            path_inicio_maximinos = g.greedy(inicio, "Maximinos")
            path_maximinos_fim = g.greedy("Maximinos", fim)

            calendario = path_inicio_calendario[1] + path_calendario_fim[1]
            casteloes = path_inicio_casteloes[1] + path_casteloes_fim[1]
            maximinos = path_inicio_maximinos[1] + path_maximinos_fim[1]

            value = min(calendario, casteloes, maximinos)

            if value == calendario:
                solucao = (path_inicio_calendario[0] + path_calendario_fim[0][1:], "{:.1f}".format(path_inicio_calendario[1] + path_calendario_fim[1]))
            elif value == maximinos:
                solucao = (path_inicio_maximinos[0] + path_maximinos_fim[0][1:], "{:.1f}".format(path_inicio_maximinos[1] + path_maximinos_fim[1]))
            else:
                solucao = (path_inicio_casteloes[0] + path_casteloes_fim[0][1:], "{:.1f}".format(path_inicio_casteloes[1] + path_casteloes_fim[1]))


            print(f"Ideal Path: {solucao} | Time taken: {(perf_counter()-start_time)*1000} ms")

            l = input("Prima Enter para continuar")


        else:
            print("You didn't add anything")
            l = input("Prima Enter para continuar")


if __name__ == "__main__":
    main()
