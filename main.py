from Cliente import Cliente
from Estafeta import Estafeta
from Global import Global


gl = Global()

cliente1 = Cliente("João", "Nine", gl)
cliente2 = Cliente("Ana", "Fradelos", gl)
cliente3 = Cliente("António", "Bairro", gl)


estafeta1 = Estafeta("bicicleta", "Nine", "Anacleto", gl)
estafeta2 = Estafeta("mota", "Joane", "Mandela", gl)
estafeta3 = Estafeta("carro", "Louro", "Júlio", gl)


cliente1.printAll()





