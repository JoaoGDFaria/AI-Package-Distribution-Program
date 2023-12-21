import tkinter as tk
from time import perf_counter
import Graph as gr
import pandas as pd
from functools import partial
from tkinter import simpledialog

def opcao1(g, pos):
    return lambda: g.desenha(pos)

def opcao2(g, pontoslevantamento):
    return lambda: mostrar_menu("Opção 2 - Percorrer DFS", partial(auxFunction, g.procura_DFS, pontoslevantamento, g))

def opcao3(g, pontoslevantamento):
    return lambda: mostrar_menu("Opção 3 - Percorrer BFS", partial(auxFunction, g.procura_BFS, pontoslevantamento, g))

def opcao4(g, pontoslevantamento):
    return lambda: mostrar_menu("Opção 4 - Percorrer A*", partial(auxFunction, g.procura_aStar, pontoslevantamento, g))

def opcao5(g, pontoslevantamento):
    return lambda: mostrar_menu("Opção 5 - Percorrer Greedy", partial(auxFunction, g.greedy, pontoslevantamento, g))

def mostrar_menu(titulo, proxima_opcao):
    # Limpar a tela
    for widget in root.winfo_children():
        widget.destroy()

    # Criar rótulo de título
    label_titulo = tk.Label(root, text=titulo, font=("Helvetica", 16))
    label_titulo.pack(pady=10)

    # Criar botão para avançar para a próxima opção
    button_proxima_opcao = tk.Button(root, text="Próxima Opção", command=proxima_opcao)
    button_proxima_opcao.pack(pady=20)

def sair(root):
    root.destroy()

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

    # Criar a janela principal
    global root
    root = tk.Tk()
    root.title("Menu")

    # Criar um menu
    menu = tk.Menu(root)
    root.config(menu=menu)

    # Criar um submenu
    submenu = tk.Menu(menu)
    menu.add_cascade(label="Opções", menu=submenu)

    submenu.add_command(label="Opção 1 - Mostrar Grafo", command=opcao1(g, pos))
    submenu.add_command(label="Opção 2 - Percorrer DFS", command=opcao2(g, pontoslevantamento))
    submenu.add_command(label="Opção 3 - Percorrer BFS", command=opcao3(g, pontoslevantamento))
    submenu.add_command(label="Opção 4 - Percorrer A*", command=opcao4(g, pontoslevantamento))
    submenu.add_command(label="Opção 5 - Percorrer Greedy", command=opcao5(g, pontoslevantamento))
    submenu.add_separator()
    submenu.add_command(label="Sair", command=lambda: sair(root))
    # Iniciar o loop de eventos
    root.mainloop()


def auxFunction(algorithmFunction, nodeStops, nodes, root):
    inicio = simpledialog.askstring("Nodo inicial", "Nodo inicial:")
    if not nodes.node_exists(inicio):
        return

    fim = simpledialog.askstring("Nodo final", "Nodo final:")
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

    # Remova a linha abaixo se não quiser pausar a execução
    simpledialog.askstring("Prima Enter para continuar", "Prima Enter para continuar")

# Modifique a chamada para incluir a janela principal 'root'
if __name__ == "__main__":
    main()
