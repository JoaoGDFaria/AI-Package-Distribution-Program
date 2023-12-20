import math

import info
from Global import Global
class Encomenda:

    def __init__(self, peso, precoBase, localEntrega, idCliente, tempoInicio, tempoFim, localizacao, gl):
        self.idCliente = idCliente
        self.peso = peso
        self.localizacao = localizacao
        self.precoBase = precoBase
        self.localEntrega = localEntrega
        self.tempoInicio = tempoInicio
        self.tempoFim = tempoFim
        self.gl = gl
        self.gl.add_encomenda(self)


    # Determinar estafeta a utilizar
    def determinarEstafeta(self):
        self.precoEntrega()


    # Preço final
    def precoEntrega(self):
        # Bicicleta
        if self.veiculo == "bicicleta":
            self.precoBase *= 1.05
        # Mota
        elif self.veiculo == "moto":
            self.precoBase *= 1.3
        # Carro
        elif self.veiculo == "carro":
            self.precoBase *= 1.5

            
    # Função para determinar a penalização de uma encomenda
    # com base no seu atraso em minutos
    def penalizacaoEncomenda(self, tempoEntrega):
        rating_final = 5
        tempoMinutos = 0

        if(tempoEntrega >= self.tempoFim):
            tempoMinutos = ((tempoEntrega - self.tempoFim).total_seconds()) / 60
            intervalos15Minutos = math.ceil(tempoMinutos // 15)
            rating_final = 5-(intervalos15Minutos * 0.2)
            if rating_final < 0: rating_final = 0

        return (rating_final, tempoMinutos)
             
           
        