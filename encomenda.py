class Encomenda:

    def __init__(self, idEncomenda, peso, volume, localizacao, idCliente):
        self.idEncomenda = idEncomenda
        self.idCliente = idCliente
        self.peso = peso
        self.volume = volume
        self.precoBase = 5 * self.volume / self.peso
        self.localizacao = localizacao
        self.determinarVeiculo()


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