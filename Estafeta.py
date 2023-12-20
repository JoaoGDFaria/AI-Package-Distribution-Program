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


    def efetuarEncomenda(self, path, tempoInicio, locaisEntrega, graph, listaEncomendas, pesoTotalEncomendas, pontosRecolha):
        self.setDisponivel(False)
        tempoFinal = tempoInicio + timedelta(minutes=len(locaisEntrega))
        distancia_percorrida = 0
        caminho_anterior = path[0]
        encomenda = None
        flag = False

        for caminho in path:
            distancia_percorrida += graph.get_arc_cost(caminho_anterior, caminho)

            if caminho in pontosRecolha: flag = True

            if flag:
                while caminho in locaisEntrega:  # Entrega

                    for encomenda in listaEncomendas:
                        if encomenda.localEntrega == caminho:
                            listaEncomendas.remove(encomenda)
                            break

                    locaisEntrega.remove(caminho)

                    self.localizacao = caminho

                    tempoGastoPorEncomenda = tempoFinal + timedelta(hours=(distancia_percorrida / self.velocidadeMedia)) + timedelta(minutes=1)
                    tempoFinal = tempoGastoPorEncomenda
                    distancia_percorrida = 0

                    (rating, atraso) = encomenda.penalizacaoEncomenda(tempoGastoPorEncomenda)

                    hours1, remainder1 = divmod((tempoFinal-tempoInicio).seconds, 3600)
                    minutes1 = remainder1 // 60

                    hours2, remainder2 = divmod(atraso.seconds, 3600)
                    minutes2 = remainder2 // 60

                    ratingCliente = float(input(f"Encomenda chegou {hours1} horas e {minutes1} minutos depois a {self.localizacao} com {hours2} horas e {minutes2} minutos de atraso!\nQue rating pretende dar à/ao estafeta {self.nome}? "))

                    if ratingCliente < 0: ratingCliente = 0
                    elif ratingCliente > 5: ratingCliente = 5
                    ratingEntrega = (rating + ratingCliente)/2
                    print(f"Rating global: {ratingEntrega}\n")

                    self.rating = ((self.rating * self.numentregas) + ratingEntrega) / (self.numentregas + 1)
                    self.numentregas += 1

                    pesoTotalEncomendas -= encomenda.peso
                    self.calculaVelocidadeMedia(pesoTotalEncomendas)

            caminho_anterior = caminho

        # Redefine tudo para o estado inicial
        self.velocidadeMedia = info.infoVelocidadeMedia[self.veiculo]
        self.setDisponivel(True)
