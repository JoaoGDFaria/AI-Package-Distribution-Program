import info
import random
from itertools import permutations


class Entrega:
    def __init__(self, lencomendas, estafeta, graph):
        self.lencomendas = lencomendas
        self.estafeta = estafeta
        self.graph = graph

    def melhorCaminho(self, locaisentrega, velocidadeMedia, encomendas):
        localinicial = self.estafeta.localizacao
        caminho = []
        penalizacao = -1
        ordementrega = []

        all_permutations = list(permutations(locaisentrega))
        for i in all_permutations:
            temp = self.tempoCaminho(localinicial, i, velocidadeMedia, encomendas)

            if penalizacao == -1:
                penalizacao = temp[1]
                caminho = temp[0]
                ordementrega = i

            if temp[1] < penalizacao:
                penalizacao = temp[1]
                caminho = temp[0]
                ordementrega = i

        return penalizacao, caminho, ordementrega

    def tempoCaminho(self, localinicial, locaisentrega, velocidadeMedia, encomendas):
        t = ([], 0)
        tp = 0
        pen = 0
        caminho = []
        for i in locaisentrega:
            t = self.graph.procura_BFS(self.estafeta.localizacao, i)
            for j in encomendas:
                if j.localizacao == i:
                    tp = j.tempoPedido
            pen = t[1] / velocidadeMedia
            if tp < pen:
                pen = pen - tp
            caminho.append(t[0])
            self.estafeta.localizacao = i
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

    def calculaVelocidadeMedia(self, metereologia):
        if metereologia == False and (
                self.estafeta.veiculo == "bicicleta" or self.estafeta.veiculo == "mota"):  # False = chuva, veiculos que sofrem penalizacao
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

    # Fazer uma determianda entrega com base nas encomendas a entregar
    def fazerEntrega(self, encomendas, locaisEntrega, metereologia, timeatual, estafeta, grafo):
        self.estafeta = estafeta
        self.graph = grafo
        tinicio = timeatual
        self.estafeta.disponivel = False
        inicio = self.estafeta.localizacao
        distanciatotal = 0

        pesoTotalEncomendas = sum(encomendas.peso)
        self.estafeta.velocidadeMedia -= self.estafeta.perdaPorKg * pesoTotalEncomendas

        vm = self.calculaVelocidadeMedia(metereologia)

        da = self.graph.procura_BFS(self.estafeta.localizacao, "Calendário")
        db = self.graph.procura_BFS(self.estafeta.localizacao, "Castelões")

        if (da[1] < db[1]):
            for passo in da[0]:
                timeatual += self.graph.get_arc_cost(self.estafeta.localizacao, passo) / self.estafeta.velocidadeMedia
                self.estafeta.localizacao = passo

        else:
            for passo in db[0]:
                timeatual += self.graph.get_arc_cost(self.estafeta.localizacao, passo) / self.estafeta.velocidadeMedia
                self.estafeta.localizacao = passo

        tempolevantamento = encomendas.length * 60
        timeatual += tempolevantamento

        distancia = self.melhorCaminho(locaisEntrega, vm, encomendas)  # distancia[0] -> tempo geral penalização, distancia[1] -> caminho, distancia[2] -> ordem de entrega
        tempototalpenalizacao = distancia[0]
        caminho = distancia[1]
        ordem = distancia[2]

        iterar = 0
        numparagens = encomendas.length
        cont = 0
        for i in caminho:
            while cont < numparagens:
                distanciatotal += self.graph.get_arc_cost(self.estafeta.localizacao, i)
                self.estafeta.localizacao = i

                if (i == ordem[iterar]):
                    tempogastoporencomenda = distanciatotal / self.estafeta.velocidadeMedia
                    pen = self.estafeta.calculaPenalizacao(self.estafeta.veiculo, tempogastoporencomenda, encomendas[iterar].tempoEntrega)
                    timeatual += tempogastoporencomenda

                    tempogastonestaencomenda = timeatual - tinicio
                    tempogastonestaencomenda -= encomendas[iterar].tempoEntrega
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
        self.estafeta.localizacao = locaisEntrega[-1]
        self.estafeta.disponivel = True

