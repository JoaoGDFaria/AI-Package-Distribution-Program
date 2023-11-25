import info
from Global import Global
import random
import Graph as g
from itertools import permutations

class Estafeta:

    def __init__(self, veiculo, localizacao, nome, gl):
        self.veiculo = veiculo
        self.id = id
        self.rating = 0
        self.atraso = 0
        self.nome = nome
        self.entregas = 0
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
        i = []
        valor=0
        temp=0
        mp=[]
        pentempo = 0
        perm = []
        all_permutations = list(permutations(locaisentrega))
        for i in all_permutations:
            temp = self.pesoCaminho(i, velocidadeMedia, encomendas)
            if pentempo == 0:
                valor = temp[0]
                mp = temp[1]
                pentempo = temp[2]
                perm = i
            if temp[2] < pentempo:
                valor = temp[0]
                mp=temp[1]
                pentempo = temp[2]
                perm = i
        return valor,mp,perm,pentempo

    def pesoCaminho(self, locaisentrega, velocidadeMedia, encomendas):
        t = ([],0)
        valor = 0
        tp = 0
        caminho = []
        for i in locaisentrega:
            t = g.procura_BFS(self.localizacao, i)
            for j in encomendas:
                if j.localizacao == i:
                    tp = j.tempoPedido
            pen = t[1] / velocidadeMedia
            if(tp < pen):
                pen = pen - tp
            caminho.append(t[0])
            valor+=t[1]
            self.localizacao = i
        return valor,caminho,pen

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

        distancia = self.melhorCaminho(locaisEntrega, vm, encomendas)  # distancia[0] = distancia total, distancia[1] = caminho, distancia[2] = locaisEntrega
        valortotal = distancia[0]
        caminho = distancia[1]
        ordem = distancia[2]

        iterar = 0
        for i in caminho:
            while(i!=ordem[iterar]):
                distanciapornodo += g.procura_BFS(self.localizacao, i)[1]
            if(i==ordem[iterar]):
                tempogastoporencomenda = distanciapornodo/self.velocidadeMedia
                pen = self.calculaPenalizacao(self.veiculo, tempogastoporencomenda, encomendas[iterar].tempoEntrega, ratingdadocliente, timeatual)
                rate = 5 - pen
                self.mudaRating(rate)
                iterar+=1

        # Redifine tudo para o estado inicial
        self.velocidadeMaxima = info.infoVelocidadeMedia[self.veiculo]
        self.localizacao = locaisEntrega[-1]
        self.disponivel = True

