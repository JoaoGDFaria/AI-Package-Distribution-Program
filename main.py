import os
from pathlib import Path
import shutil
from datetime import datetime
from Cliente import Cliente
from Estafeta import Estafeta
from Global import Global
from AgruparEncomenda import AgruparEncomenda
import Graph as gr
import pandas as pd
import funcoes_auxiliares as fa
import menu


def main():
    gl = Global()

    # Read all .csv Utilizadores
    df_estafetas = pd.read_csv("Files/Utilizadores/estafetas.csv", encoding='utf-8')
    for linha in df_estafetas.itertuples(index=False):
        Estafeta(linha.veiculo, linha.freguesia, linha.nome, linha.rating, linha.numEntregas, gl)

    df_clientes = pd.read_csv("Files/Utilizadores/clientes.csv", encoding='utf-8')
    for linha in df_clientes.itertuples(index=False):
        Cliente(linha.nome, linha.localização, gl)

    # Read all .csv Grafo
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

    ag = AgruparEncomenda(pontoslevantamento, gl, g)

    directory_path = f"./Outputs/"
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)


    lista_encomenda = []
    datetimeStart = datetime(year=2023, month=12, day=20, hour=18, minute=30)

    while True:
        print("1-Consultar clientes")
        print("2-Consultar estafetas")
        print("3-Inserir encomendas .csv com todos os algoritmos")
        print("4-Inserir encomendas .csv com algoritmo específico")
        print("5-Remover ligação entre freguesias")
        print("6-Atualizar data inicial")
        print("0-Sair")


        try:

            saida = int(input("Introduza a sua opção-> "))

            if saida == 0:
                print("Saindo .......")
                break

            elif saida == 1:
                gl.printAllUtilizadores()

            elif saida == 2:
                gl.printAllEstafetas()

            elif saida == 3:
                print("A ler ficheiro .csv .......")
                df_encomendas = pd.read_csv("Files/Encomendas/encomendas.csv", encoding='utf-8')
                for linha in df_encomendas.itertuples(index=False):
                    lista_encomenda.append((linha.idcliente, linha.peso, linha.preco, linha.volume, linha.tempoFim))
                fa.estudoDeUmaEntrega(pontoslevantamento, lista_encomenda, datetimeStart, gl, g, ag)
                lista_encomenda.clear()
                print("-----------------------------")

            elif saida == 4:
                while True:
                    print("1-Usar o algoritmo DFS")
                    print("2-Usar o algoritmo BFS")
                    print("3-Usar o algoritmo Procura Custo Uniforme")
                    print("4-Usar o algoritmo Greedy")
                    print("5-Usar o algoritmo A*")
                    
                    try:
                        saida = int(input("Introduza a sua opção-> "))
                        
                        if saida == 0:
                            print("Saindo .......")
                            break
                    
                        elif saida>= 1 and saida<=5:
                            print("A ler ficheiro .csv .......")
                            df_encomendas = pd.read_csv("Files/Encomendas/encomendas.csv", encoding='utf-8')
                            for linha in df_encomendas.itertuples(index=False):
                                lista_encomenda.append((linha.idcliente, linha.peso, linha.preco, linha.volume, linha.tempoFim))
                            print("-----------------------------")
                            fa.estudoDeUmaEntrega2(pontoslevantamento,lista_encomenda, datetimeStart, gl, g, ag, saida-1)
                            lista_encomenda.clear()

                        else:
                            print("Please insert a valid number")
                            input("Prima Enter para continuar")
                         
                    except ValueError:
                        print("Please insert a valid input")
                        input("Prima Enter para continuar")


            elif saida == 5:
                inicio = menu.checkIfExists("Nodo inicial", g)
                fim = menu.checkIfExists("Nodo final", g)

                g.del_route(inicio, fim)
                input("Prima Enter para continuar")

            elif saida == 6:
                data = input("Introduza data-> ")
                datetimeStart = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
                gl.atualizarEstafetas(datetimeStart)

            else:
                print("Please insert a valid number")
                input("Prima Enter para continuar")

        except ValueError:
            print("Please insert a valid input")
            input("Prima Enter para continuar")


if __name__ == "__main__":
    main()

# print(len(gl.get_encomendas_sem_entregador()))