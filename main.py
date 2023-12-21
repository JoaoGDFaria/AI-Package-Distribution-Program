from Cliente import Cliente
from Estafeta import Estafeta
from Global import Global
import funcoes_auxiliares as fa
from datetime import datetime
import Graph as gr
import pandas as pd

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





    cliente1 = Cliente("João", "Nine", gl)
    cliente2 = Cliente("Ana", "Fradelos", gl)
    cliente3 = Cliente("António", "Bairro", gl)

    datetimeStart = datetime(year=2023, month=11, day=22, hour=18, minute=30)
    datetimeFinish = datetime(year=2023, month=11, day=22, hour=22, minute=30)


    enc1 = cliente2.criarEncomenda(peso=2, preco=54.23, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2023, month=11, day=22, hour=23, minute=30))
    enc2 = cliente1.criarEncomenda(peso=2, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2023, month=11, day=22, hour=23, minute=30))
    enc3 = cliente3.criarEncomenda(peso=1, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2023, month=11, day=22, hour=22, minute=35))
    enc4 = cliente2.criarEncomenda(peso=2, preco=54.23, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2023, month=11, day=22, hour=21, minute=15))
    enc5 = cliente1.criarEncomenda(peso=2, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2023, month=11, day=28, hour=20, minute=45))
    enc6 = cliente3.criarEncomenda(peso=1, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2023, month=11, day=22, hour=23, minute=0))
    enc7 = cliente2.criarEncomenda(peso=2, preco=54.23, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2023, month=11, day=23, hour=18, minute=30))
    enc8 = cliente1.criarEncomenda(peso=2, preco=543, volume=123, tempoInicio=datetimeStart, tempoFim=datetime(year=2023, month=11, day=26, hour=22, minute=15))


    fa.estudoDeUmaEntrega([enc1, enc2], g, datetimeStart, pontoslevantamento, gl, g)


if __name__ == "__main__":
    main()



#print(len(gl.get_encomendas_sem_entregador()))
