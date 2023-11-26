import info
from Global import Global
import random
import Graph as g
from itertools import permutations

#TODO - O calculo do melhor caminho so usa um algoritmo
#TODO - Verificar antes de encomenda qual o veiculo mais proveitoso para a entrega
#TODO - Verificar se é suposto escolher o veiculo aquando do pedido

class Estafeta:

    def __init__(self, veiculo, localizacao, nome, rating, num, gl):
        self.veiculo = veiculo
        self.id = id
        self.rating = rating
        self.atraso = 0
        self.nome = nome
        self.entregas = num
        self.localizacao = localizacao
        self.pesoMaximo = info.infoPesoMaximo[veiculo]
        self.velocidadeMedia = info.infoVelocidadeMedia[veiculo]
        self.perdaPorKg = info.infoPerdaPorKg[veiculo]
        self.disponivel = True
        self.gl = gl
        self.gl.add_estafeta(self)


    def mudarLocalizacao(self, localizacao):
        self.localizacao = localizacao

    def melhorCaminho(self, locaisentrega, velocidadeMedia, encomendas):
        localinicial = self.localizacao
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
        t = ([],0)
        tp = 0
        pen = 0
        caminho = []
        for i in locaisentrega:
            t = g.procura_BFS(self.localizacao, i)
            for j in encomendas:
                if j.localizacao == i:
                    tp = j.tempoPedido
            pen = t[1] / velocidadeMedia
            if tp < pen:
                pen = pen - tp
            caminho.append(t[0])
            self.localizacao = i
        self.localizacao = localinicial
        return caminho,pen

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

    def calculaVelocidadeMedia(self, metereologia):
        if metereologia == False and (self.veiculo == "bicicleta" or self.veiculo == "mota"): # False = chuva, veiculos que sofrem penalizacao
            self.velocidadeMedia*=0.8

        num = random.randint(1,100)
        rand = random.randint(60,100)
        rand /= 100
        if self.veiculo == "carro" and num < 10:
            self.velocidadeMedia *= rand
        elif self.veiculo == "mota" and num < 20:
            self.velocidadeMedia *= rand
        elif self.veiculo == "bicicleta" and num < 30:
            self.velocidadeMedia *= rand


    # Fazer uma determianda entrega com base nas encomendas a entregar
    def fazerEntrega(self, encomendas, locaisEntrega, metereologia, ratingdadocliente, timeatual):
        tinicio = timeatual
        self.disponivel = False
        inicio = self.localizacao
        distanciapornodo = 0

        pesoTotalEncomendas = sum(encomendas.peso)
        self.velocidadeMedia -= self.perdaPorKg * pesoTotalEncomendas

        vm = self.calculaVelocidadeMedia(metereologia)

        da = g.procura_BFS(self.localizacao, "Calendário")
        db = g.procura_BFS(self.localizacao, "Castelões")

        if (da[1] < db[1]):
            for passo in da[0]:
                timeatual += g.get_arc_cost(self.localizacao, passo) / self.velocidadeMedia
                self.localizacao = passo

        else:
            for passo in db[0]:
                timeatual += g.get_arc_cost(self.localizacao, passo) / self.velocidadeMedia
                self.localizacao = passo

        tempolevantamento = encomendas.length * 60
        timeatual += tempolevantamento

        distancia = self.melhorCaminho(locaisEntrega, vm, encomendas)  # distancia[0] -> tempo geral penalização, distancia[1] -> caminho, distancia[2] -> ordem de entrega
        tempototalpenalizacao = distancia[0]
        caminho = distancia[1]
        ordem = distancia[2]

        iterar = 0
        for i in caminho:
            while(i!=ordem[iterar]):
                distanciapornodo += g.procura_BFS(self.localizacao, i)[1]

            if(i==ordem[iterar]):
                tempogastoporencomenda = distanciapornodo/self.velocidadeMedia
                pen = self.calculaPenalizacao(self.veiculo, tempogastoporencomenda, encomendas[iterar].tempoEntrega, ratingdadocliente, timeatual)
                timeatual += tempogastoporencomenda

                tempogastonestaencomenda = timeatual - tinicio
                tempogastonestaencomenda -= encomendas[iterar].tempoEntrega
                if tempogastonestaencomenda <= 0:
                    tempogastonestaencomenda = 0

                ratingdadocliente = int(input(f"A encomenda chegou com {tempogastonestaencomenda} segundos de atraso \n Qual a avaliação que faz da entrega? -> "))
                rate = 5 - (pen + ratingdadocliente) / 2
                self.mudaRating(rate)

                iterar+=1

        # Redifine tudo para o estado inicial
        self.velocidadeMaxima = info.infoVelocidadeMedia[self.veiculo]
        self.localizacao = locaisEntrega[-1]
        self.disponivel = True

