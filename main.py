import csv
from datetime import datetime
from Cliente import Cliente
from Estafeta import Estafeta
from Global import Global
from AgruparEncomenda import AgruparEncomenda
import Graph as gr
import pandas as pd
import funcoes_auxiliares as fa



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

    artigos = []
    df_artigos = pd.read_csv("Files/Artigos/artigos.csv", encoding='utf-8')
    for linha in df_artigos.itertuples(index=False):
        artigos.append(linha.nome)

    ag = AgruparEncomenda(pontoslevantamento, gl, g)

    lista_encomenda = []

    while True:
        print("1-Consultar clientes")
        print("2-Consultar estafetas")
        print("3-Inserir encomenda")
        print("4-Consultar lista encomendas")
        print("5-Consultar postos de levantamento")
        print("6-Remover ligação entre freguesias")
        print("0-Sair")

        datetimeStart = datetime(year=2023, month=11, day=22, hour=18, minute=30)

        try:

            saida = int(input("Introduza a sua opção-> "))

            if saida == 0:
                print("Saindo .......")
                break

            elif saida == 1:
                print(gl.printAllUtilizadores())

            elif saida == 2:
                print(gl.printAllEstafetas())

            elif saida == 3:
                print("A ler ficheiro .csv .......")
                df_encomendas = pd.read_csv("Files/Encomendas/encomendas.csv", encoding='utf-8')
                for linha in df_encomendas.itertuples(index=False):
                    lista_encomenda.append((linha.idcliente, linha.peso, linha.preco, linha.volume, linha.tempoFim))
                fa.estudoDeUmaEntrega(pontoslevantamento, lista_encomenda, datetimeStart, gl, g, ag)
                
                print("-----------------------------")

            elif saida == 4:
                print(gl.printAllEncomendas())

            elif saida == 5:
                print(df_postosLevantamento)
                print("-----------------------------")

            else:
                print("Please insert a valid number")
                input("Prima Enter para continuar")

        except ValueError:
            print("Please insert a valid input")
            input("Prima Enter para continuar")

    ag.imprimirEncomendas()
    ag.imprimirEncomendas()

    fa.estudoDeUmaEntrega(pontoslevantamento, gl, g, ag)

    # fa.escolherEncomendas(gl, g, pontoslevantamento)


if __name__ == "__main__":
    main()

# print(len(gl.get_encomendas_sem_entregador()))