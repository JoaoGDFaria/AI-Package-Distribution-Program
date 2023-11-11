import time
import Graph as gr


def main():
    g = gr.Graph()

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

    # Coordenadas fixas para cada nó
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
        print("0-Saír")

        saida = int(input("introduza a sua opcao-> "))
        if saida == 0:
            print("saindo.......")
        elif saida == 1:
            g.desenha(pos)
        elif saida == 2:

            inicio = input("Nodo inicial->")
            if not g.node_exists(inicio): continue
            fim = input("Nodo final->")
            if not g.node_exists(fim): continue

            start_time = time.time()
            print(f"Ideal Path: {g.procura_DFS(inicio, fim, path=[], visited=set())}"
                  f" | Time taken: {(time.time()-start_time)*1000} ms")

            l = input("prima enter para continuar")

        elif saida == 3:

            inicio = input("Nodo inicial->")
            if not g.node_exists(inicio): continue
            fim = input("Nodo final->")
            if not g.node_exists(fim): continue
            start_time = time.time()
            print(f"Ideal Path: {g.procura_BFS(inicio, fim)} |"
                  f" Time taken: {(time.time()-start_time)*1000} ms")

            l = input("prima enter para continuar")
        else:
            print("you didn't add anything")
            l = input("prima enter para continuar")




if __name__ == "__main__":
    main()
