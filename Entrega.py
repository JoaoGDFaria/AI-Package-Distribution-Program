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
        #self.pesoTotalEncomendas = sum(self.listaEncomendas.peso)
        #self.calculaVelocidadeMedia(self.metereologia, self.pesoTotalEncomendas)
        self.velocidadeMedia = self.estafeta.velocidadeMedia
        self.pontosRecolha = pontosRecolha





        all_permutations_path = list(permutations(self.locaisEntrega))
        all_paths = []

        for pRecolha in self.pontosRecolha:
            for path in all_permutations_path:
                all_paths.append([self.localizacaoInicio, pRecolha] + list(path))


        for p in all_paths:
            print(f"{p}\n")

    def melhorCaminho(self):
        caminho = []
        penalizacao = -1
        ordementrega = []

        all_permutations_path = list(permutations(self.locaisEntrega))
        all_paths = [[]]

        for pRecolha in self.pontosRecolha:
            for path in all_permutations_path:
                all_paths.append([self.localizacaoInicio, pRecolha] + path)


        for i in all_permutations:
            temp = self.tempoCaminho(self.estafeta.localizacao, i, velocidadeMedia, listaEncomendas)

            if penalizacao == -1:
                penalizacao = temp[1]
                caminho = temp[0]
                ordementrega = i

            if temp[1] < penalizacao:
                penalizacao = temp[1]
                caminho = temp[0]
                ordementrega = i

        return penalizacao, caminho, ordementrega

    def tempoCaminho(self, localinicial, locaisentrega, velocidadeMedia, listaEncomendas):
        t = ([], 0)
        tp = 0
        pen = 0
        caminho = []
        for i in locaisentrega:
            t = self.graph.procura_BFS(self.estafeta.localizacao, i)
            for j in listaEncomendas:
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

        distancia = self.melhorCaminho(self.locaisEntrega, self.velocidadeMedia, self.listaEncomendas)  # distancia[0] -> tempo geral penalização, distancia[1] -> caminho, distancia[2] -> ordem de entrega
        tempototalpenalizacao = distancia[0]
        caminho = distancia[1]
        ordem = distancia[2]

        iterar = 0
        numparagens = self.listaEncomendas.length
        cont = 0
        for i in caminho:
            while cont < numparagens:
                self.distanciatotal += self.graph.get_arc_cost(self.estafeta.localizacao, i)
                self.estafeta.localizacao = i

                if (i == ordem[iterar]):
                    tempogastoporencomenda = distanciatotal / self.estafeta.velocidadeMedia
                    pen = self.estafeta.calculaPenalizacao(self.estafeta.veiculo, tempogastoporencomenda, listaEncomendas[iterar].tempoEntrega)
                    timeatual += tempogastoporencomenda

                    tempogastonestaencomenda = timeatual - tempoInicio
                    tempogastonestaencomenda -= listaEncomendas[iterar].tempoEntrega
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

