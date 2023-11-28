from time import perf_counter

import info
import random
from itertools import permutations
from datetime import datetime, timedelta


class Entrega:
    def __init__(self, listaEncomendas, graph, metereologia, tempoInicio, tempoFim, pontosRecolha, gl):
        self.listaEncomendas = listaEncomendas
        self.graph = graph
        self.metereologia = metereologia
        self.tempoInicio = tempoInicio
        self.tempoFim = tempoFim
        self.locaisEntrega = [encomenda.localEntrega for encomenda in self.listaEncomendas]
        self.pesoTotalEncomendas = sum(encomenda.peso for encomenda in self.listaEncomendas)
        self.pontosRecolha = pontosRecolha
        self.gl = gl

        (a, b, c) = self.melhorCaminho()
        print((a, b, c))

        # self.calculaVelocidadeMedia(self.metereologia, self.pesoTotalEncomendas)
        # self.localizacaoInicio = self.estafeta.localizacao


    def melhorCaminho(self):
        all_permutations_path = list(permutations(self.locaisEntrega))
        path_ideal = []
        custo_ideal = float("inf")

        start_time = perf_counter()
        for posicaoInicial in self.gl.get_estafetas_available(self.pesoTotalEncomendas):
            for pontoRecolha in self.pontosRecolha:
                for path in all_permutations_path:
                    all_paths = [pontoRecolha] + list(path)

                    (path, custo) = self.calculaMelhorCaminho(posicaoInicial, all_paths)

                    if custo < custo_ideal:
                        custo_ideal = custo
                        path_ideal = path
                        print(all_paths)
        print(f"Time taken: {(perf_counter() - start_time) * 1000 :.2f} ms")
        print(path_ideal)
        print(custo_ideal)

        velocidade_media = self.calculaVelocidadeDeEntrega(custo_ideal)
        print(f"Velocidade média: {velocidade_media} km/h")
        print(f"Peso: {self.pesoTotalEncomendas} kg")

                    #temp = self.tempoCaminho(posicaoInicial, all_paths, self.listaEncomendas)

                    # if penalizacao == -1:
                    #     penalizacao = temp[1]
                    #     caminho = temp[0]
                    #     ordementrega = all_paths
                    #
                    # if temp[1] < penalizacao:
                    #     penalizacao = temp[1]
                    #     caminho = temp[0]
                    #     ordementrega = all_paths

        #return penalizacao, caminho, ordementrega

    def tempoCaminho(self, localinicial, locaisentrega, listaEncomendas):
        penalizacao = 0
        caminho_ideal = []

        for local in locaisentrega:
            (path,custo) = self.graph.procura_BFS(self.estafeta.localizacao, local)

            for encomenda in listaEncomendas:
                if encomenda.localizacao == local:
                    tempoFim = encomenda.tempoFim

            tempoEntrega = (path / velocidadeMedia)*3600
            finalizacaoRealDaEncomenda = encomenda.tempoInicio+timedelta(seconds=tempoEntrega)

            if tempoFim < finalizacaoRealDaEncomenda:
                penalizacao = finalizacaoRealDaEncomenda - tempoFim
            caminho_ideal.append(custo)
            self.estafeta.localizacao = local

        self.estafeta.localizacao = localinicial
        return caminho_ideal, penalizacao

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


    def calculaVelocidadeDeEntrega(self, distancia):
        intervaloDeTempo = self.get_tempo_encomenda() -self.tempoInicio
        intervaloDeTempoEmHoras = intervaloDeTempo.total_seconds() / 3600

        velocidadeMedia = distancia/intervaloDeTempoEmHoras
        return velocidadeMedia


    def calculaMelhorCaminho(self, localinicial, locaisentrega):
        custo_final = 0
        caminho_final = []

        for local in locaisentrega:
            (path, custo) = self.graph.procura_BFS(localinicial, local)
            localinicial = local

            if caminho_final != [] and caminho_final[-1] == path[0]:
                caminho_final.extend(path[1:])
            else:
                caminho_final.extend(path)
            custo_final += custo

        return caminho_final, custo_final


    def get_tempo_encomenda(self):
        tempoMinimo = datetime.max
        for encomenda in self.listaEncomendas:
            if encomenda.tempoFim < tempoMinimo:
                tempoMinimo = encomenda.tempoFim
        return tempoMinimo




