from itertools import permutations
from Graph import Graph as gr
import info

class Global:
    def __init__(self):
        self.todos_clientes = {}
        self.todos_encomendas = {}
        self.todos_estafetas = {}

    def add_cliente(self, cliente):
        total_length = len(self.todos_clientes)
        self.todos_clientes[total_length+1] = cliente
        return total_length+1

    def add_encomenda(self, encomenda):
        total_length = len(self.todos_encomendas)
        self.todos_encomendas[total_length+1] = encomenda
        return total_length + 1

    def add_estafeta(self, estafeta):
        total_length = len(self.todos_estafetas)
        self.todos_estafetas[total_length+1] = estafeta
        return total_length + 1


    def get_cliente(self, id):
        return self.todos_clientes.get(id, None)

    def get_encomenda(self, id):
        return self.todos_encomendas.get(id, None)

    def get_estafeta(self, id):
        return self.todos_estafetas.get(id, None)

    def get_estafetasByVehicle(self, veiculo):
        all_estaf = []
        for estafeta in self.todos_estafetas.values():
            all_estaf.append(estafeta)
        return all_estaf

    def get_all_estafetas_available(self, peso):
        todas_possibilidades = {}
        for estafeta in self.todos_estafetas.values():
            if estafeta.disponivel and estafeta.pesoMaximo >= peso:
                value = (estafeta.rating, estafeta.veiculo, estafeta.localizacao)
                key = (value[2], value[1])
                rat = value[0]

                if key in todas_possibilidades:
                    rating_estafeta = todas_possibilidades.get(key)

                    if rating_estafeta < rat:
                        todas_possibilidades[key] = rat

                else:
                    todas_possibilidades[key] = rat

        return todas_possibilidades


    def get_estafeta_available_by_location(self, localizacao, veiculo):
        for estafeta in self.todos_estafetas.values():
            if estafeta.disponivel and estafeta.veiculo == veiculo and estafeta.localizacao == localizacao:
                return estafeta

    def get_encomendas_sem_entregador(self):
        all_enc = []
        for encomenda in self.todos_encomendas.values():
            if encomenda.idEstafeta is None:
                all_enc.append(encomenda)
        return all_enc


    def printAllGlobal(self):
        for id, info in self.todos_clientes.items():
            print(f"ID: {id}, Nome: {info.nome}, Localizacao: {info.localizacao}, Encomendas: {info.encomendas}")
        print("-----------------------------")
        for id, info in self.todos_estafetas.items():
            print(f"ID: {id}, Nome: {info.nome}, Localizacao: {info.localizacao}, Veiculo: {info.veiculo}, Rating: {info.rating}, Número de Viagens: {info.numentregas} , Disponível: {info.disponivel}")
        print("-----------------------------")
        for id, info in self.todos_encomendas.items():
            print(f"ID: {id}, IdCliente: {info.idCliente}, Peso: {info.peso}, Preço Base: {info.precoBase}, Local Entrega: {info.localEntrega}, Tempo Inicio: {info.tempoInicio}, Prazo Limite: {info.prazoLimite}, Tempo Entrega: {info.tempoEntrega}, Rating: {info.rating}")

    def veiculoMax(self, encomendas):

        pesoTotal = sum(encomenda.peso for encomenda in encomendas)
        (distanciaMaxBicicleta, distanciaMaxMota, distanciaMaxCarro) = (0, 0, 0)

        formulaBicicleta = info.horasMaximasDeTrabalho["bicicleta"] * (info.infoVelocidadeMedia["bicicleta"] - info.infoPerdaPorKg["bicicleta"] * pesoTotal)
        formulaMota = info.horasMaximasDeTrabalho["mota"] * (info.infoVelocidadeMedia["mota"] - info.infoPerdaPorKg["mota"] * pesoTotal)
        formulaCarro = info.horasMaximasDeTrabalho["carro"] * (info.infoVelocidadeMedia["carro"] - info.infoPerdaPorKg["carro"] * pesoTotal)

        if pesoTotal <= info.infoPesoMaximo["bicicleta"]:
            distanciaMaxBicicleta = formulaBicicleta
            distanciaMaxMota = formulaMota
            distanciaMaxCarro = formulaCarro

        elif pesoTotal <= info.infoPesoMaximo["mota"]:
            distanciaMaxMota = formulaMota
            distanciaMaxCarro = formulaCarro

        elif pesoTotal <= info.infoPesoMaximo["carro"]:
            distanciaMaxCarro = formulaCarro

        return distanciaMaxBicicleta, distanciaMaxMota, distanciaMaxCarro

    def qualFaz(self, g):
        encomendas = self.get_encomendas_sem_entregador()
        pontosEntrega = []

        for encomenda in encomendas:
            pontosEntrega.append(encomenda.localEntrega)


        minimum = 0

        (distanciaMaxBicicleta, distanciaMaxMota, distanciaMaxCarro) = self.veiculoMax(encomendas)

        permutation = list(permutations(encomendas))
        locInicial = entrega.estafeta.localizacao

        for path in permutation:
            custoDFS = 0
            custoBFS = 0
            custoAStar = 0
            custoGreedy = 0
            custoUniform = 0
            for next in path:
                custoDFS += gr.procura_DFS(g, locInicial, next.localEntrega)[1]
                custoBFS += gr.procura_BFS(g, locInicial, next.localEntrega)[1]
                custoAStar += gr.procura_aStar(g, locInicial, next.localEntrega)[1]
                custoGreedy += gr.greedy(g, locInicial, next.localEntrega)[1]
                custoUniform += gr.procura_UCS(g, locInicial, next.localEntrega)[1]
                locInicial = next.localEntrega

            temp = min(custoDFS, custoBFS, custoAStar, custoGreedy, custoUniform)
            if (temp < minimum or temp == 0):
                minimum = temp

        if (minimum <= distanciaMaxBicicleta):
            return "bicicleta"
        elif (distanciaMaxBicicleta < minimum <= distanciaMaxMota):
            return "mota"
        elif (distanciaMaxMota < minimum <= distanciaMaxCarro):
            return "carro"
        else:
            return None
