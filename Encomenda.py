import math
from datetime import timedelta

class Encomenda:

    def __init__(self, peso, preco, volume, localEntrega, idCliente, tempoInicio, prazoLimite, gl):
        self.idCliente = idCliente
        self.peso = peso
        self.preco = preco
        self.volume = volume
        self.localEntrega = localEntrega
        self.tempoInicio = tempoInicio
        self.prazoLimite = prazoLimite
        self.tempoEntrega = None
        self.rating = None
        self.idEstafeta = None
        self.gl = gl
        self.id = self.gl.add_encomenda(self)


    # Função para determinar a penalização de uma encomenda
    # com base no seu atraso em minutos
    def penalizacaoEncomenda(self, tempoEntrega):
        rating_final = 5
        tempoMinutos = 0

        if(tempoEntrega >= self.prazoLimite):
            tempoMinutos = ((tempoEntrega - self.prazoLimite).total_seconds()) / 60
            intervalos15Minutos = math.ceil(tempoMinutos // 15)
            rating_final = 5-(intervalos15Minutos * 0.5)
            if rating_final < 0: rating_final = 0

        return rating_final, timedelta(minutes=tempoMinutos)
             
           
        