import info

class Estafeta:

    def __init__(self, veiculo, id):
        self.veiculo = veiculo
        self.id = id
        self.ranking = 0
        self.pesoMaximo = info.infoPesoMaximo[veiculo]
        self.velocidadeMaxima = info.infoVelocidadeMedia[veiculo]
        self.perdaPorKg = info.infoPerdaPorKg[veiculo]
        self.disponivel = True


    # Função para determinar a penalização do rating de um estafeta
    # com base no seu atraso em horas
    def penalizacaoEstafeta(self):
        pass


    # Fazer uma determianda entrega com base nas encomendas a entregar
    def fazerEntrega(self, encomendas, locaisEntrega):
        self.disponivel = False
        pesoTotalEncomendas = sum(encomendas.peso)
        self.velocidadeMaxima -= self.perdaPorKg * pesoTotalEncomendas



        self.velocidadeMaxima = info.infoVelocidadeMedia[self.veiculo]
        self.disponivel = True





