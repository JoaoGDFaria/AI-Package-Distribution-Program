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

    #df_encomendas = pd.read_csv("Files/Encomendas/encomendas.csv", encoding='utf-8')

    # enc1 = cliente1.criarEncomenda(peso=99, preco=54.23, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish1, pontosRecolha=pontoslevantamento, g=g, ag=ag, algoritmo=g.procura_BFS)
    # enc2 = cliente2.criarEncomenda(peso=1, preco=10, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish2, pontosRecolha=pontoslevantamento, g=g, ag=ag)
    # enc3 = cliente3.criarEncomenda(peso=1, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish3, pontosRecolha=pontoslevantamento, g=g, ag=ag)
    # enc4 = cliente4.criarEncomenda(peso=10, preco=5.23, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish1, pontosRecolha=pontoslevantamento, g=g, ag=ag)
    # enc5 = cliente1.criarEncomenda(peso=1, preco=55, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish4, pontosRecolha=pontoslevantamento, g=g, ag=ag)
    # enc6 = cliente3.criarEncomenda(peso=1, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2024, month=11, day=22, hour=23, minute=0))
    # enc7 = cliente2.criarEncomenda(peso=2, preco=54.23, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2024, month=11, day=23, hour=18, minute=30))
    # enc8 = cliente1.criarEncomenda(peso=3, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2024, month=11, day=26, hour=22, minute=15))

    # lista_encomenda = []
    #
    # while True:
    #     print("1-Consultar clientes")
    #     print("2-Consultar estafetas")
    #     print("3-Inserir encomenda manualmente")
    #     print("4-Inserir encomenda")
    #     print("5-Consultar lista encomendas")
    #     print("6-Consultar postos de levantamento")
    #     print("7-Carregar encomendas")
    #     print("8-Remover ligação entre freguesias")
    #     print("0-Sair")
    #
    #     datetimeStart = datetime(year=2023, month=11, day=22, hour=18, minute=30)
    #
    #     try:
    #
    #         saida = int(input("Introduza a sua opção-> "))
    #
    #         if saida == 0:
    #             print("Saindo .......")
    #             break
    #
    #         elif saida == 1:
    #             print(gl.printAllUtilizadores())
    #
    #         elif saida == 2:
    #             print(gl.printAllEstafetas())
    #
    #         elif saida == 3:
    #             print("Inserir a encomenda no ficheiro 'encomendas.csv'")
    #             print("-----------------------------")
    #
    #         elif saida == 4:
    #             localizacao = (input("Indique a localização do cliente-> "))
    #             cliente = gl.get_cliente_by_localizacao(localizacao)
    #             peso = int(input("Indique o peso-> "))
    #             preco = float(input("Indique o preco-> "))
    #             volume = int(input("Indique o volume-> "))
    #             limite = (input("Indique o prazo limite entrega-> "))
    #             encomendas_cliente = (cliente, peso, preco, volume, limite, datetimeStart)
    #             lista_encomenda.append(encomendas_cliente)
    #
    #         elif saida == 5:
    #             print(gl.printAllEncomendas())
    #
    #         elif saida == 6:
    #             print(df_postosLevantamento)
    #             print("-----------------------------")
    #
    #         elif saida == 7:
    #             fa.estudoDeUmaEntrega(pontoslevantamento, lista_encomenda, gl, g, ag)
    #             print("As encomendas foram carregadas")
    #             print("-----------------------------")
    #
    #         elif saida == 8:
    #             g.del_route("Nine", "Louro")
    #
    #
    #         else:
    #             print("Please insert a valid number")
    #             input("Prima Enter para continuar")
    #
    #     except ValueError:
    #         print("Please insert a valid input")
    #         input("Prima Enter para continuar")

    # ag.imprimirEncomendas()
    # ag.imprimirEncomendas()

    fa.estudoDeUmaEntrega(pontoslevantamento, gl, g, ag)

    # fa.escolherEncomendas(gl, g, pontoslevantamento)


if __name__ == "__main__":
    main()

# print(len(gl.get_encomendas_sem_entregador()))