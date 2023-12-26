from Cliente import Cliente
from Estafeta import Estafeta
from Global import Global
from AgruparEncomenda import AgruparEncomenda
from datetime import datetime
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

    ag = AgruparEncomenda(pontoslevantamento, gl, g)



    #enc1 = cliente1.criarEncomenda(peso=99, preco=54.23, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish1, pontosRecolha=pontoslevantamento, g=g, ag=ag, algoritmo=g.procura_BFS)
    #enc2 = cliente2.criarEncomenda(peso=1, preco=10, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish2, pontosRecolha=pontoslevantamento, g=g, ag=ag)
    #enc3 = cliente3.criarEncomenda(peso=1, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish3, pontosRecolha=pontoslevantamento, g=g, ag=ag)
    #enc4 = cliente4.criarEncomenda(peso=10, preco=5.23, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish1, pontosRecolha=pontoslevantamento, g=g, ag=ag)
    #enc5 = cliente1.criarEncomenda(peso=1, preco=55, volume=123, tempoInicio=datetimeStart, tempoFim=datetimeFinish4, pontosRecolha=pontoslevantamento, g=g, ag=ag)
    #enc6 = cliente3.criarEncomenda(peso=1, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2024, month=11, day=22, hour=23, minute=0))
    #enc7 = cliente2.criarEncomenda(peso=2, preco=54.23, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2024, month=11, day=23, hour=18, minute=30))
    #enc8 = cliente1.criarEncomenda(peso=3, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2024, month=11, day=26, hour=22, minute=15))



    #ag.imprimirEncomendas()
    #ag.imprimirEncomendas()

    fa.estudoDeUmaEntrega(pontoslevantamento, gl, g, ag)
    #fa.escolherEncomendas(gl, g, pontoslevantamento)

if __name__ == "__main__":
    main()



#print(len(gl.get_encomendas_sem_entregador()))
