import info
import encomenda

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


    # Função para determinar a penalização do rating de um estafeta
    # com base no seu atraso em horas
    def penalizacaoEstafeta(self):
        ranking = self.ranking - encomenda.penalizacaoEncomenda
        if(ranking < 0):
            self.ranking = 0
            
        return ranking
        
        
            
            
        


    # Fazer uma determianda entrega com base nas encomendas a entregar
    def fazerEntrega(self, encomendas, locaisEntrega):
        self.disponivel = False
        pesoTotalEncomendas = sum(encomendas.peso)
        self.velocidadeMaxima -= self.perdaPorKg * pesoTotalEncomendas



        self.velocidadeMaxima = info.infoVelocidadeMedia[self.veiculo]
        self.disponivel = True





