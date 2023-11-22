from Global import Global
class Cliente:

    def __init__(self, nome, localizacao, gl):
        self.encomendas = []
        self.localizacao = localizacao
        self.nome = nome
        self.gl = gl
        self.gl.add_cliente(self)


    def criarEncomenda(self):
        pass

    def mudarLocalizacao(self, localizacao):
        self.localizacao = localizacao


    def definirRanking(self, idEncomenda):
        pass



    def printAll(self):
        self.gl.printAllGlobal()
