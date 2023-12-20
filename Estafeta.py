import info
import random

class Estafeta:

    def __init__(self, veiculo, localizacao, nome, rating, num, gl):
        self.veiculo = veiculo
        self.id = id
        self.rating = rating
        self.atraso = 0
        self.nome = nome
        self.numentregas = num
        self.localizacao = localizacao
        self.pesoMaximo = info.infoPesoMaximo[veiculo]
        self.velocidadeMedia = info.infoVelocidadeMedia[veiculo]
        self.perdaPorKg = info.infoPerdaPorKg[veiculo]
        self.disponivel = True
        self.gl = gl
        self.gl.add_estafeta(self)


    def setDisponivel (self, disponivel):
        self.disponivel = disponivel



    def calculaVelocidadeMedia(self, metereologia, pesoTotalEncomendas):
        velocidadeInicial = self.velocidadeMedia
        self.velocidadeMedia -= self.perdaPorKg * pesoTotalEncomendas

        if not metereologia and (not self.estafeta.veiculo == "carro"):  # False = chuva, veiculos que sofrem penalizacao
            self.estafeta.velocidadeMedia *= 0.8

        num = random.randint(1, 100)
        rand = random.randint(60, 100)
        rand /= 100
        if self.estafeta.veiculo == "carro" and num < 10:
            self.estafeta.velocidadeMedia *= rand
        elif self.estafeta.veiculo == "mota" and num < 20:
            self.estafeta.velocidadeMedia *= rand
        elif self.estafeta.veiculo == "bicicleta" and num < 30:
            self.estafeta.velocidadeMedia *= rand

        # fator de multiplicacao
        return self.estafeta.velocidadeMedia / velocidadeInicial

        # Fazer uma determianda entrega com base nas listaEncomendas a entregar



