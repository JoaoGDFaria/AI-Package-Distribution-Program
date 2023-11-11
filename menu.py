import networkx as nx
import matplotlib.pyplot as plt


def main():
    g = nx.Graph()

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
            pos = nx.spring_layout(g)
            nx.draw_networkx(g, pos, with_labels=True, font_weight="bold")
            labels = nx.get_edge_attributes(g, "weight")
            nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
            plt.title("Freguesias de Famalicão")
            plt.show()
            l = input("prima enter para continuar")
        elif saida == 2:
            inicio = input("Nodo inicial->")
            fim = input("Nodo final->")
            #print(g.procura_DFS(inicio, fim, path=[], visited=set()))
            l = input("prima enter para continuar")
        elif saida == 3:
            inicio = input("Nodo inicial->")
            fim = input("Nodo final->")
            #print(g.procura_BFS(inicio, fim))
            l = input("prima enter para continuar")
        else:
            print("you didn't add anything")
            l = input("prima enter para continuar")




if __name__ == "__main__":
    main()
