import info
from Global import Global
class Encomenda:

    def __init__(self, idEstafeta, peso, volume, localizacao, idCliente, tempoInicio, tempoPedido, tempo, gl):
        self.idCliente = idCliente
        self.idEstafeta = idEstafeta
        self.peso = peso
        self.volume = volume
        self.precoBase = 5 * self.volume / self.peso
        self.localizacao = localizacao
        self.determinarVeiculo()
        self.tempoInicio = tempoInicio
        self.tempoPedido = tempoPedido
        self.tempo = tempo
        self.gl = gl
        self.gl.add_encomenda(self)


    # Determinar estafeta a utilizar
    def determinarEstafeta(self):
        if self.peso > 20:
            self.veiculo = "carro"


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
             
           
        