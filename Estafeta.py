import math
from datetime import timedelta

import info
import random

class Estafeta:

    def __init__(self, veiculo, localizacao, nome, rating, num, gl):
        self.veiculo = veiculo
        self.rating = rating
        self.nome = nome
        self.numentregas = num
        self.localizacao = localizacao
        self.pesoMaximo = info.infoPesoMaximo[veiculo]
        self.velocidadeMedia = info.infoVelocidadeMedia[veiculo]
        self.perdaPorKg = info.infoPerdaPorKg[veiculo]
        self.disponivel = True
        self.gl = gl
        self.id = self.gl.add_estafeta(self)


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


    def efetuarEncomenda(self, path, tempoInicio, locaisEntrega, graph, listaEncomendas, pesoTotalEncomendas, pontosRecolha, df, row):
        self.setDisponivel(False)

        for encomenda in listaEncomendas:
            encomenda.idEstafeta = self.id

        tempoFinal = tempoInicio + timedelta(minutes=len(locaisEntrega))
        distancia_percorrida = 0
        distancia_acumulativa = 0
        caminho_anterior = path[0]
        encomenda = None
        flag = False

        for caminho in path:
            distancia_percorrida += graph.get_arc_cost(caminho_anterior, caminho)
            distancia_acumulativa += distancia_percorrida

            if caminho in pontosRecolha: flag = True

            if flag:
                while caminho in locaisEntrega:  # Entrega

                    for encomenda in listaEncomendas:
                        if encomenda.localEntrega == caminho:
                            listaEncomendas.remove(encomenda)
                            break

                    locaisEntrega.remove(caminho)

                    self.localizacao = caminho

                    tempoGastoPorEncomenda = (tempoFinal + timedelta(hours=(distancia_percorrida / self.velocidadeMedia)) + timedelta(minutes=1)).replace(second=0, microsecond=0)
                    tempoFinal = tempoGastoPorEncomenda
                    distancia_percorrida = 0

                    (rating, atraso) = encomenda.penalizacaoEncomenda(tempoGastoPorEncomenda)

                    hours1, remainder1 = divmod((tempoFinal-tempoInicio).seconds, 3600)
                    minutes1 = remainder1 // 60

                    hours2, remainder2 = divmod(atraso.seconds, 3600)
                    minutes2 = remainder2 // 60

                    encomenda.preco = round(encomenda.preco+(distancia_acumulativa//10), 2)


                    cliente = self.gl.get_cliente(encomenda.idCliente)
                    ratingCliente = cliente.avaliarEstafeta(hours1, minutes1, hours2, minutes2, self.nome, encomenda.preco)
                    #df.at[row, 'Distância percorrida'] = f"{round(distancia_acumulativa, 2)} km"
                    if ratingCliente < 0: ratingCliente = 0
                    elif ratingCliente > 5: ratingCliente = 5
                    ratingEntrega = round((rating + ratingCliente)/2, 1)
                    print(f"Rating global: {ratingEntrega}\n")

                    self.rating = round(((self.rating * self.numentregas) + ratingEntrega) / (self.numentregas + 1), 1)
                    self.numentregas += 1
                    encomenda.tempoEntrega = tempoFinal
                    encomenda.rating = ratingEntrega

                    pesoTotalEncomendas -= encomenda.peso
                    self.calculaVelocidadeMedia(pesoTotalEncomendas)

            caminho_anterior = caminho
        # Redefine tudo para o estado inicial
        self.velocidadeMedia = info.infoVelocidadeMedia[self.veiculo]
        self.setDisponivel(True)
        #df.at[row, 'Tempo de entrega'] = tempoFinal - tempoInicio

        #self.gl.printAllGlobal()
