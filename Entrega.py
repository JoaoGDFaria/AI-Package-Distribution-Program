import info
import random
from itertools import permutations
from datetime import datetime, timedelta


class Entrega:
    def __init__(self, listaEncomendas, estafeta, graph, metereologia, tempoInicio, pontosRecolha):
        self.listaEncomendas = listaEncomendas
        self.estafeta = estafeta
        self.graph = graph
        self.metereologia = metereologia
        self.tempoInicio = tempoInicio
        self.estafeta.disponivel = False
        self.localizacaoInicio = self.estafeta.localizacao
        self.distanciatotal = 0
        self.locaisEntrega = [encomenda.localEntrega for encomenda in self.listaEncomendas]
        self.pesoTotalEncomendas = sum(encomenda.peso for encomenda in self.listaEncomendas)
        self.calculaVelocidadeMedia(self.metereologia, self.pesoTotalEncomendas)
        self.velocidadeMedia = self.estafeta.velocidadeMedia
        self.pontosRecolha = pontosRecolha
        (a, b, c) = self.melhorCaminho()
        print((a, b, c))


    def melhorCaminho(self):
        all_permutations_path = list(permutations(self.locaisEntrega))
        penalizacao = -1

        for pRecolha in self.pontosRecolha:
            for path in all_permutations_path:
                all_paths = [pRecolha] + list(path)
                print(self.localizacaoInicio, all_paths, self.velocidadeMedia, self.listaEncomendas)
                temp = self.tempoCaminho(self.localizacaoInicio, all_paths, self.velocidadeMedia, self.listaEncomendas)

                if penalizacao == -1:
                    penalizacao = temp[1]
                    caminho = temp[0]
                    ordementrega = all_paths

                if temp[1] < penalizacao:
                    penalizacao = temp[1]
                    caminho = temp[0]
                    ordementrega = all_paths

        return penalizacao, caminho, ordementrega

    def tempoCaminho(self, localinicial, locaisentrega, velocidadeMedia, listaEncomendas):
        pen = 0
        caminho = []

        for local in locaisentrega:
            t = self.graph.procura_BFS(self.estafeta.localizacao, local)
            tempoFim = datetime(year=2023, month=11, day=22, hour=22, minute=30)

            for encomenda in listaEncomendas:
                if encomenda.localizacao == local:
                    tempoFim = encomenda.tempoFim

            tempoEntrega = (t[1] / velocidadeMedia)*3600
            finalizacaoRealDaEncomenda = encomenda.tempoInicio+timedelta(seconds=tempoEntrega)

            if tempoFim < finalizacaoRealDaEncomenda:
                tempoPenalizacao = finalizacaoRealDaEncomenda - tempoFim
            caminho.append(t[0])
            self.estafeta.localizacao = local

        self.estafeta.localizacao = localinicial
        return caminho, pen

    def mudaRating(self, rate):
        total = self.estafeta.rating * self.estafeta.numentregas
        total += rate
        self.estafeta.rating = total / (self.estafeta.numentregas + 1)

    def calculaPenalizacao(self, entrega, suposto):
        veiculo = self.estafeta.veiculo
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


    def calculaVelocidadeMedia(self, metereologia, pesoTotalEncomendas):
        self.estafeta.velocidadeMedia -= self.estafeta.perdaPorKg * pesoTotalEncomendas

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



    # Fazer uma determianda entrega com base nas listaEncomendas a entregar
    def fazerEntrega(self):

        tempoFinal = self.tempoInicio + timedelta(minutes=self.listaEncomendas.length)

        distancia = self.melhorCaminho()  # distancia[0] -> tempo geral penalização, distancia[1] -> caminho, distancia[2] -> ordem de entrega
        tempototalpenalizacao = distancia[0]
        caminho = distancia[1]
        ordem = distancia[2]
        timeatual=0
        iterar = 0
        numparagens = self.listaEncomendas.length
        cont = 0

        for i in caminho:
            while cont < numparagens:
                self.distanciatotal += self.graph.get_arc_cost(self.estafeta.localizacao, i)
                self.estafeta.localizacao = i

                if i == ordem[iterar]:
                    tempogastoporencomenda = self.distanciatotal / self.estafeta.velocidadeMedia
                    pen = self.estafeta.calculaPenalizacao(self.estafeta.veiculo, tempogastoporencomenda, self.listaEncomendas[iterar].tempoEntrega)
                    timeatual += tempogastoporencomenda

                    tempogastonestaencomenda = timeatual - self.tempoInicio
                    tempogastonestaencomenda -= self.listaEncomendas[iterar].tempoEntrega
                    if tempogastonestaencomenda <= 0:
                        tempogastonestaencomenda = 0

                    ratingdadocliente = int(input(
                        f"A encomenda chegou com {tempogastonestaencomenda} segundos de atraso \n Qual a avaliação que faz da entrega? -> "))
                    rate = 5 - (pen + (5 - ratingdadocliente)) / 2
                    self.estafeta.mudaRating(rate)

                    cont += 1
                    iterar += 1

        # Redifine tudo para o estado inicial
        self.estafeta.velocidadeMaxima = info.infoVelocidadeMedia[self.estafeta.veiculo]
        self.estafeta.localizacao = self.locaisEntrega[-1]
        self.estafeta.disponivel = True

