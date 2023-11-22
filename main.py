from Cliente import Cliente
from Estafeta import Estafeta
from Global import Global
from datetime import datetime


datetimeStart = datetime(year=2023, month=11, day=22, hour=18, minute=30)

gl = Global()

cliente1 = Cliente("João", "Nine", gl)
cliente2 = Cliente("Ana", "Fradelos", gl)
cliente3 = Cliente("António", "Bairro", gl)


estafeta1 = Estafeta("bicicleta", "Nine", "Anacleto", gl)
estafeta2 = Estafeta("mota", "Joane", "Mandela", gl)
estafeta3 = Estafeta("carro", "Louro", "Júlio", gl)



cliente2.criarEncomenda(peso=24.23, precoBase=54.23, tempoInicio=datetimeStart, tempoFim=datetime(year=2023, month=11, day=22, hour=22, minute=30))
cliente1.printAll()
