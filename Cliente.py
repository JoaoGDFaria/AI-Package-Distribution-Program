from Encomenda import Encomenda

class Cliente:

    def __init__(self, nome, localizacao, gl):
        self.encomendas = []
        self.localizacao = localizacao
        self.nome = nome
        self.gl = gl
        self.id = self.gl.add_cliente(self)

    def criarEncomenda(self, peso, precoBase, tempoInicio, tempoFim):
        if peso > 100:
            print("Não é possível transportar encomendas com mais de 100kg!")
            return
        enc = Encomenda(peso, precoBase, self.localizacao, self.id, tempoInicio, tempoFim,  self.gl)
        self.addEncomenda(enc)
        return enc

    def printAll(self):
        self.gl.printAllGlobal()

    def addEncomenda(self, enc):
        self.encomendas.append(enc)

    def avaliarEstafeta(self, hours1, minutes1, hours2, minutes2, nomeEstafeta):
        ratingCliente = float(input(f"Encomenda chegou {hours1} horas e {minutes1} minutos depois a {self.localizacao} com {hours2} horas e {minutes2} minutos de atraso!\nQue rating pretende dar à/ao estafeta {nomeEstafeta}? "))
        return ratingCliente