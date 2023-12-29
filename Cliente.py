from Encomenda import Encomenda
import info

class Cliente:

    def __init__(self, nome, localizacao, gl):
        self.encomendas = []
        self.localizacao = localizacao
        self.nome = nome
        self.gl = gl
        self.id = self.gl.add_cliente(self)

    def criarEncomenda(self, peso, preco, volume, tempoInicio, tempoFim, pontosRecolha, g, ag, algoritmo, fileName):
        pesoMax = info.infoPesoMaximo["carro"]
        volumeMax = info.infoVolumeMaximo["carro"]

        if peso > pesoMax:
            print(f"Não é possível transportar encomendas com mais de {pesoMax} kg!")
            return
        if volume > volumeMax:
            print(f"Não é possível transportar encomendas com mais de {volumeMax} L!")
            return

        enc = Encomenda(peso, preco, volume, self.localizacao, self.id, tempoInicio, tempoFim, pontosRecolha, self.gl, g, ag, algoritmo, fileName)
        self.addEncomenda(enc)

        return enc

    def printAll(self):
        self.gl.printAllGlobal()

    def addEncomenda(self, enc):
        self.encomendas.append(enc)

    # def avaliarEstafeta(self, hours1, minutes1, hours2, minutes2, nomeEstafeta, preco, id):
    #     print(
    #         f"A encomenda {id} chegou {hours1} horas e {minutes1} minutos depois a {self.localizacao} com {hours2} horas e {minutes2} minutos de atraso!"
    #         f"\nPreço final: {preco} €"
    #         f"\nQue rating pretende dar à/ao estafeta {nomeEstafeta}? ")
    #     return 0