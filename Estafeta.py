import info

#TODO - Verificar antes de encomenda qual o veiculo mais proveitoso para a entrega
#TODO - Verificar se é suposto escolher o veiculo aquando do pedido

class Estafeta:

    def __init__(self, veiculo, localizacao, nome, rating, num, gl):
        self.veiculo = veiculo
        self.id = id
        self.rating = rating
        self.atraso = 0
        self.nome = nome
        self.numentregas = num
        self.localizacao = localizacao
        self.pesoMaximo = info.infoPesoMaximo[veiculo]
        self.velocidadeMedia = info.infoVelocidadeMedia[veiculo]
        self.perdaPorKg = info.infoPerdaPorKg[veiculo]
        self.disponivel = True
        self.gl = gl
        self.gl.add_estafeta(self)
