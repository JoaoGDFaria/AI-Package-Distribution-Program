from Cliente import Cliente
from Estafeta import Estafeta
from Global import Global
from Entrega import Entrega
from datetime import datetime
import pandas as pd
import Graph as gr


gl = Global()


df_estafetas = pd.read_csv("Files/Utilizadores/estafetas.csv", encoding='utf-8')
for linha in df_estafetas.itertuples(index=False):
    Estafeta(linha.veiculo, linha.freguesia, linha.nome, linha.rating, linha.numEntregas, gl)


df_clientes = pd.read_csv("Files/Utilizadores/clientes.csv", encoding='utf-8')
for linha in df_clientes.itertuples(index=False):
    Cliente(linha.nome, linha.localização, gl)















######TESTES


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





estafeta1 = Estafeta("bicicleta", "Bairro", "Anacleto",4.5,10, gl)
datetimeStart = datetime(year=2023, month=11, day=22, hour=18, minute=30)
cliente1 = Cliente("João", "Nine", gl)
cliente2 = Cliente("Ana", "Fradelos", gl)
cliente3 = Cliente("António", "Bairro", gl)
enc1 = cliente2.criarEncomenda(peso=2, precoBase=54.23, tempoInicio=datetimeStart, tempoFim=datetime(year=2023, month=11, day=22, hour=22, minute=30))
enc2 = cliente1.criarEncomenda(peso=3, precoBase=543, tempoInicio=datetimeStart, tempoFim=datetime(year=2023, month=11, day=22, hour=22, minute=30))


list = []
list.append(enc1)
list.append(enc2)
ent = Entrega(list, estafeta1, g, False, datetimeStart, pontoslevantamento)

