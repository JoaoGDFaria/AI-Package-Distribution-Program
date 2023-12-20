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
        self.veiculo = ""
        self.gl.add_encomenda(self)
        self.determinarEstafeta()

        # Segundos de diferença para calcular velocidade média
        seconds_difference = (tempoFim-tempoInicio).total_seconds()


    # Determinar estafeta a utilizar
    def determinarEstafeta(self):
        self.gl.get_estafetasByVehicle(self.veiculo)
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

    # Função para determinar a penalização em função
    # do tipo de veículo, estado de tempo e distância         
    def tempoEntrega(self, distancia):
        veiculo = self.gl.get_estafeta(self.idEstafeta).veiculo
        condicoesTransporte = info.infoTempo[[self.tempo], veiculo]
        
        penalizacao = condicoesTransporte * distancia
        
        return penalizacao
        
           
            
    # Função para determinar a penalização de uma encomenda
    # com base no seu atraso em minutos
    def penalizacaoEncomenda(self, tempoEntrega, id, distancia):
        tempoUtil = int (tempoEntrega - self.tempoInicio)/60
        
        if(tempoUtil >= self.tempoPedido):
            tempoMinutos = tempoUtil - self.tempoPedido
            penalizacaoEncomenda = tempoMinutos * tempoEntrega(self, id, distancia)

        return penalizacaoEncomenda
             
           
        