import math
from datetime import timedelta

import info
import random

class Estafeta:

    def __init__(self, veiculo, localizacao, nome, rating, num, gl):
        self.veiculo = veiculo
        self.id = id
        self.rating = rating
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



    def calculaVelocidadeMedia(self, pesoTotalEncomendas):
        self.velocidadeMedia = round(info.infoVelocidadeMedia[self.veiculo] - (info.infoPerdaPorKg[self.veiculo] * pesoTotalEncomendas), 2)
        num = random.randint(1, 100)
        rand = random.randint(60, 100)
        rand /= 100

        if self.veiculo == "carro" and num < 10:
            self.velocidadeMedia = round(self.velocidadeMedia * rand, 2)

        elif self.veiculo == "mota" and num < 7:
            self.velocidadeMedia = round(self.velocidadeMedia * rand, 2)

        elif self.veiculo == "bicicleta" and num < 5:
            self.velocidadeMedia = round(self.velocidadeMedia * rand, 2)

        print(f"\nVelocidade média do estafeta final: {self.velocidadeMedia} km/h")


    def efetuarEncomenda(self, path, tempoInicio, locaisEntrega, graph, listaEncomendas, pesoTotalEncomendas):

        self.setDisponivel(False)
        tempoFinal = tempoInicio + timedelta(minutes=len(locaisEntrega))
        distancia_percorrida = 0
        caminho_anterior = path[0]
        encomenda = None

        for caminho in path:
            while caminho in locaisEntrega:  # Entrega

                for encomenda in listaEncomendas:
                    if encomenda.localEntrega == caminho:
                        listaEncomendas.remove(encomenda)
                        break

                locaisEntrega.remove(caminho)
                arc_cost = graph.get_arc_cost(caminho_anterior, caminho)
                if arc_cost == math.inf: arc_cost = 0
                distancia_percorrida+=arc_cost

                self.localizacao = caminho
                caminho_anterior = caminho

                print(f"distancia_percorrida: {distancia_percorrida}")
                print(f"self.velocidadeMedia: {self.velocidadeMedia}")
                tempoGastoPorEncomenda = tempoFinal + timedelta(hours=(distancia_percorrida / self.velocidadeMedia)) + timedelta(minutes=1)
                tempoFinal = tempoGastoPorEncomenda

                pesoTotalEncomendas -= encomenda.peso
                self.velocidadeMedia = self.calculaVelocidadeMedia(pesoTotalEncomendas)

                rating = encomenda.penalizacaoEncomenda
                ratingCliente = float(input("Que rating pretende dar ao estafeta? "))
                if ratingCliente < 0: ratingCliente = 0
                elif ratingCliente > 5: ratingCliente = 5

                ratingEntrega = (rating + ratingCliente)/2

                self.rating = ((self.rating * self.numentregas) + ratingEntrega) / (self.numentregas + 1)
                self.numentregas += 1


        # Redifine tudo para o estado inicial
        self.velocidadeMedia = info.infoVelocidadeMedia[self.veiculo]
        self.setDisponivel(True)


    def mudaRating(self, rate):
        total = self.rating * self.entregas
        total += rate
        self.rating = total / (self.entregas + 1)


    def calculaPenalizacao(self, veiculo, entrega, suposto, ratingdadocliente):
        multiplicador = 1
        pen = 0

        if veiculo == "carro":
            multiplicador = 1

        elif veiculo == "mota":
            multiplicador = 1.5

        elif veiculo == "bicicleta":
            multiplicador = 2

        pen = (entrega / suposto) * multiplicador

        if pen > 4:
            pen = 4
        pen += 1

        return pen
