from Cliente import Cliente
from Estafeta import Estafeta
from Global import Global
from datetime import datetime
import pandas as pd


gl = Global()


df_estafetas = pd.read_csv("files/Utilizadores/estafetas.csv", encoding='utf-8')
for linha in df_estafetas.itertuples(index=False):
    Estafeta(linha.veiculo, linha.freguesia, linha.nome, linha.rating, linha.numEntregas, gl)


df_clientes = pd.read_csv("files/Utilizadores/clientes.csv", encoding='utf-8')
for linha in df_clientes.itertuples(index=False):
    Cliente(linha.nome, linha.localização, gl)



datetimeStart = datetime(year=2023, month=11, day=22, hour=18, minute=30)

gl.printAllGlobal()
