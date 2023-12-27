class Artigo:
    def __init__(self, nome, peso, volume, preco):
        self.nome = nome
        self.peso = peso
        self.volume = volume
        self.preco = preco


    def artigosPossiveisNaBicicleta(self, produtos):
        artigos = []
        for produto in produtos:
            if produto.volume <= 42 and produto.peso <= 5:
                artigos.append(produto)
        return artigos

    def artigosPossiveisNaMota(self, produtos):
        artigos = []
        for produto in produtos:
            if produto.volume <= 87 and produto.peso <= 20:
                artigos.append(produto)
        return artigos

    def artigosPossiveisNoCarro(self, produtos):
        artigos = []
        for produto in produtos:
            if produto.volume <= 2500 and produto.peso <= 100:
                artigos.append(produto)
        return artigos