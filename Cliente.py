from Global import Global
from Encomenda import Encomenda

class Cliente:

    def __init__(self, nome, localizacao, gl):
        self.encomendas = []
        self.localizacao = localizacao
        self.nome = nome
        self.gl = gl
        self.id = self.gl.add_cliente(self)

    def criarEncomenda(self, peso, precoBase, tempoInicio, tempoFim):
        enc = Encomenda(peso, precoBase, self.localizacao, self.id, tempoInicio, tempoFim, self.gl)
        self.encomendas.append(enc)
        return enc

    def mudarLocalizacao(self, localizacao):
        self.localizacao = localizacao

    def definirRanking(self, idEncomenda):
        pass

    def printAll(self):
        self.gl.printAllGlobal()
