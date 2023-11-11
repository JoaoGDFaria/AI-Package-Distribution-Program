import info
import encomenda
import random
import Graph as g
from itertools import permutations

class Estafeta:

    def __init__(self, veiculo, id, localizacao):
        self.veiculo = veiculo
        self.id = id
        self.ranking = 0
        self.atraso = 0
        self.localizacao = localizacao
        self.pesoMaximo = info.infoPesoMaximo[veiculo]
        self.velocidadeMedia = info.infoVelocidadeMedia[veiculo]
        self.perdaPorKg = info.infoPerdaPorKg[veiculo]
        self.disponivel = True

    # Função para determinar o tempo de entrega de uma encomenda
    def tempoEntrega(self, encomenda):
        tempo = 0



    # Função para determinar a penalização do rating de um estafeta
    # com base no seu atraso em horas
    def penalizacaoEstafeta(self):
        ranking = self.ranking - encomenda.penalizacaoEncomenda
        if(ranking < 0):
            self.ranking = 0
            
        return ranking

    def melhorCaminho(self, locaisentrega):
        valor=0
        temp=0
        all_permutations = list(permutations(locaisentrega))
        for i in all_permutations:
            temp = self.pesoCaminho(i)
            if temp < valor:
                valor = temp
        return valor

    def pesoCaminho(self, locaisentrega):
        valor = 0
        for i in locaisentrega:
            valor += g.procura_BFS(self.localizacao, i)
            self.localizacao = i
        return valor


    # Fazer uma determianda entrega com base nas encomendas a entregar
    def fazerEntrega(self, encomendas, locaisEntrega, metereologia):
        self.disponivel = False
        pesoTotalEncomendas = sum(encomendas.peso)
        self.velocidadeMedia -= self.perdaPorKg * pesoTotalEncomendas
        if metereologia == False and (self.veiculo == "bicicleta" or self.veiculo == "moto"): # False = chuva, veiculos que sofrem penalizacao
            self.velocidadeMedia*=0.8
        num = random.randint(1,100)
        rand = random.randint(1,80)
        rand /= 100
        if self.veiculo == "carro" and num < 10:
            self.velocidadeMedia *= rand
        elif self.veiculo == "moto" and num < 20:
            self.velocidadeMedia *= rand
        elif self.veiculo == "bicicleta" and num < 30:
            self.velocidadeMedia *= rand

        self.velocidadeMaxima = info.infoVelocidadeMedia[self.veiculo]
        self.localizacao = locaisEntrega[-1]
        self.disponivel = True





