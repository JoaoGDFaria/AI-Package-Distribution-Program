from Global import Global
class Cliente:

    def __init__(self, localizacao):
        self.gl = Global()
        self.encomendas = []
        self.localizacao = localizacao
        self.gl.add_cliente(self)

    def criarEncomenda(self):
        pass


    def definirRanking(self, idEncomenda):
        pass


