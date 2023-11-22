from time import perf_counter
import Graph as gr


def main():

    g = gr.Graph()


    # Definir nodos e arestas - Distância em km entre freguesias
    g.add_edge("Lousado", "Fradelos", weight=9.2)
    g.add_edge("Lousado", "Calendário", weight=5.7)
    g.add_edge("Fradelos", "Gondifelos", weight=10.2)
    g.add_edge("Gondifelos", "Outiz", weight=5.1)
    g.add_edge("Outiz", "Calendário", weight=4.2)
    g.add_edge("Calendário", "Abade de Vermoim", weight=6.0)
    g.add_edge("Abade de Vermoim", "Cabeçudos", weight=5.2)
    g.add_edge("Calendário", "Famalicão", weight=4.0)
    g.add_edge("Famalicão", "Louro", weight=5.1)
    g.add_edge("Louro", "Nine", weight=4.2)
    g.add_edge("Famalicão", "Requião", weight=5.2)
    g.add_edge("Requião", "Castelões", weight=8.0)
    g.add_edge("Mogege", "Castelões", weight=3.1)
    g.add_edge("Novais", "Castelões", weight=3.9)
    g.add_edge("Novais", "Riba de Ave", weight=4.9)
    g.add_edge("Novais", "Bairro", weight=3.0)
    g.add_edge("Famalicão", "Cruz", weight=11.4)
    g.add_edge("Arnoso (S.ta Maria)", "Cruz", weight=3.9)
    g.add_edge("Telhado", "Cruz", weight=6.2)
    g.add_edge("Telhado", "Joane", weight=9.0)


    # Definir eurísticas - Qualidade das estradas
        # 1-> Estrada em muito boas condições
        # 5-> Estrada em muito más condições
    g.add_heuristica("Lousado", 5)
    g.add_heuristica("Fradelos", 2)
    g.add_heuristica("Cabeçudos", 4)
    g.add_heuristica("Abade de Vermoim", 3)
    g.add_heuristica("Calendário", 3)
    g.add_heuristica("Outiz", 1)
    g.add_heuristica("Gondifelos", 1)
    g.add_heuristica("Bairro", 5)
    g.add_heuristica("Riba de Ave", 1)
    g.add_heuristica("Novais", 5)
    g.add_heuristica("Castelões", 2)
    g.add_heuristica("Mogege", 2)
    g.add_heuristica("Requião", 3)
    g.add_heuristica("Famalicão", 1)
    g.add_heuristica("Louro", 5)
    g.add_heuristica("Nine", 4)
    g.add_heuristica("Cruz", 2)
    g.add_heuristica("Arnoso (S.ta Maria)", 1)
    g.add_heuristica("Telhado", 2)
    g.add_heuristica("Joane", 3)


    # Coordenadas fixas para cada nó no gráfico
    pos = {
        "Lousado": (486, 960 - 857),
        "Fradelos": (172, 960 - 744),
        "Calendário": (486, 960 - 531),
        "Gondifelos": (172, 960 - 432),
        "Outiz": (349, 960 - 456),
        "Abade de Vermoim": (639, 960 - 572),
        "Famalicão": (527, 960 - 416),
        "Louro": (428, 960 - 311),
        "Nine": (428, 960 - 137),
        "Requião": (705, 960 - 432),
        "Castelões": (937, 960 - 448),
        "Mogege": (1021, 960 - 371),
        "Novais": (904, 960 - 572),
        "Riba de Ave": (1125, 960 - 604),
        "Bairro": (953, 960 - 712),
        "Cruz": (648, 960 - 255),
        "Arnoso (S.ta Maria)": (623, 960 - 96),
        "Telhado": (836, 960 - 199),
        "Joane": (970, 960 - 255),
        "Cabeçudos": (615, 960 - 736),
    }

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

            if path_inicio_casteloes[1] + path_casteloes_fim[1] >= path_inicio_calendario[1] + path_calendario_fim[1]:
                solucao = (path_inicio_calendario[0] + path_calendario_fim[0][1:], "{:.1f}".format(path_inicio_calendario[1] + path_calendario_fim[1]))
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

            if path_inicio_casteloes[1] + path_casteloes_fim[1] >= path_inicio_calendario[1] + path_calendario_fim[1]:
                solucao = (path_inicio_calendario[0] + path_calendario_fim[0][1:], "{:.1f}".format(path_inicio_calendario[1] + path_calendario_fim[1]))
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

            if path_inicio_casteloes[1] + path_casteloes_fim[1] >= path_inicio_calendario[1] + path_calendario_fim[1]:
                solucao = (path_inicio_calendario[0] + path_calendario_fim[0][1:], "{:.1f}".format(path_inicio_calendario[1] + path_calendario_fim[1]))
            else:
                solucao = (path_inicio_casteloes[0] + path_casteloes_fim[0][1:], "{:.1f}".format(path_inicio_casteloes[1] + path_casteloes_fim[1]))

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

            if path_inicio_casteloes[1] + path_casteloes_fim[1] >= path_inicio_calendario[1] + path_calendario_fim[1]:
                solucao = (path_inicio_calendario[0] + path_calendario_fim[0][1:], "{:.1f}".format(path_inicio_calendario[1] + path_calendario_fim[1]))
            else:
                solucao = (path_inicio_casteloes[0] + path_casteloes_fim[0][1:], "{:.1f}".format(path_inicio_casteloes[1] + path_casteloes_fim[1]))

            print(f"Ideal Path: {solucao} | Time taken: {(perf_counter()-start_time)*1000} ms")

            l = input("Prima Enter para continuar")


        else:
            print("You didn't add anything")
            l = input("Prima Enter para continuar")


if __name__ == "__main__":
    main()
