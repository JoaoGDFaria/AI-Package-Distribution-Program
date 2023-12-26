from itertools import permutations
from Graph import Graph as gr
import info
from itertools import chain, combinations

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
                key = (estafeta.localizacao, estafeta.veiculo)
                rat = None

                todas_possibilidades[key] = rat

        return todas_possibilidades.keys()



    def get_all_estafetas_available_veiculo(self, veiculo):
        todas_possibilidades = []

        for estafeta in self.todos_estafetas.values():
            if estafeta.disponivel and estafeta.veiculo == veiculo:

                if estafeta.localizacao not in todas_possibilidades:
                    todas_possibilidades.append(estafeta.localizacao)
        return todas_possibilidades


    def get_estafeta_available_by_location(self, localizacao, veiculo):
        rating = -1
        est = None
        for estafeta in self.todos_estafetas.values():
            if estafeta.disponivel and estafeta.veiculo == veiculo and estafeta.localizacao == localizacao and estafeta.rating > rating:
                rating = estafeta.rating
                est = estafeta
        return est

    def get_all_available_estafeta_location(self):
        different_locations = set()
        for estafeta in self.todos_estafetas.values():
            if estafeta.disponivel and estafeta.localizacao not in different_locations:
                different_locations.add(estafeta.localizacao)
        return different_locations

    def get_encomendas_sem_entregador(self):
        all_enc = []
        for encomenda in self.todos_encomendas.values():
            if encomenda.idEstafeta is None:
                all_enc.append(encomenda)


        all_enc_sorted = sorted(all_enc, key=lambda encomenda: encomenda.peso)

        lista_bicicleta = []
        lista_mota = []
        lista_carro = all_enc_sorted

        for enc in all_enc_sorted[::-1]:
            if enc.peso < info.infoPesoMaximo["bicicleta"]:
                lista_bicicleta.append(enc)
                lista_mota.append(enc)

            elif enc.peso < info.infoPesoMaximo["mota"]:
                lista_mota.append(enc)

        print(len(lista_bicicleta))

        return lista_bicicleta, lista_mota, lista_carro


    def printAllGlobal(self):
        for id, info in self.todos_clientes.items():
            print(f"ID: {id}, Nome: {info.nome}, Localizacao: {info.localizacao}, Encomendas: {info.encomendas}")
        print("-----------------------------")
        for id, info in self.todos_estafetas.items():
            print(f"ID: {id}, Nome: {info.nome}, Localizacao: {info.localizacao}, Veiculo: {info.veiculo}, Rating: {info.rating}, Número de Viagens: {info.numentregas} , Disponível: {info.disponivel}")
        print("-----------------------------")
        for id, info in self.todos_encomendas.items():
            print(f"ID: {id}, IdCliente: {info.idCliente}, Peso: {info.peso}, Preço Base: {info.precoBase}, Local Entrega: {info.localEntrega}, Tempo Inicio: {info.tempoInicio}, Prazo Limite: {info.prazoLimite}, Tempo Entrega: {info.tempoEntrega}, Rating: {info.rating}")

    def get_all_subsets(self, lst):
        subsets = []
        for subset_size in range(1, len(lst) + 1):
            subsets.extend(list(combination) for combination in combinations(lst, subset_size))
        return subsets

    def get_all_permutations(self, lst):
        all_subsets = lst.get_all_subsets()
        all_permutations = []
        for subset in all_subsets:
            all_permutations.extend(permutations(subset))
        return set(all_permutations)

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
        possibilidades = self.get_all_permutations(encomendas)
        pontosEntrega = []
        pesoTotal = sum(encomenda.peso for encomenda in encomendas)

        for encomenda in encomendas:
            pontosEntrega.append(encomenda.localEntrega)


        minimumCamPEstafeta = 0
        minTotal = 0
        maxPeso = 0

        (distanciaMaxBicicleta, distanciaMaxMota, distanciaMaxCarro) = self.veiculoMax(encomendas)



        for le in possibilidades:
            temp = sum(encomenda.peso for encomenda in le)
            pontosEntrega = []
            for encomenda in le:
                pontosEntrega += encomenda.localEntrega
            permutation = list(permutations(pontosEntrega))
            for estafeta in self.get_all_estafetas_available(pesoTotal):
                for path in permutation:
                    locInicial = estafeta.localizacao
                    custoDFS = 0
                    custoBFS = 0
                    custoAStar = 0
                    custoGreedy = 0
                    custoUniform = 0
                    pathDFS = []
                    pathBFS = []
                    pathAStar = []
                    pathGreedy = []
                    pathUniform = []
                    for next in path:
                        pathDFS += gr.procura_DFS(g, locInicial, next.localEntrega)[0]
                        pathBFS += gr.procura_BFS(g, locInicial, next.localEntrega)[0]
                        pathAStar += gr.procura_aStar(g, locInicial, next.localEntrega)[0]
                        pathGreedy += gr.greedy(g, locInicial, next.localEntrega)[0]
                        pathUniform += gr.procura_UCS(g, locInicial, next.localEntrega)[0]
                        locInicial = next.localEntrega

                    for i in range(len(pathDFS)-1):
                        custoDFS += g.get_edge(pathDFS[i], pathDFS[i+1]).weight
                    for i in range(len(pathBFS)-1):
                        custoBFS += g.get_edge(pathBFS[i], pathBFS[i+1]).weight
                    for i in range(len(pathAStar)-1):
                        custoAStar += g.get_edge(pathAStar[i], pathAStar[i+1]).weight
                    for i in range(len(pathGreedy)-1):
                        custoGreedy += g.get_edge(pathGreedy[i], pathGreedy[i+1]).weight
                    for i in range(len(pathUniform)-1):
                        custoUniform += g.get_edge(pathUniform[i], pathUniform[i+1]).weight


                    tempE = min(custoDFS, custoBFS, custoAStar, custoGreedy, custoUniform)
                    if tempE < minimumCamPEstafeta or tempE == 0:
                        minimumCamPEstafeta = tempE

                if minimumCamPEstafeta < minTotal or minTotal == 0:
                    minTotal = minimumCamPEstafeta

            if maxPeso < temp or maxPeso == 0:
                maxPeso = temp


        if minTotal <= distanciaMaxBicicleta:
            return "bicicleta"
        elif minTotal <= distanciaMaxMota:
            return "mota"
        elif minTotal <= distanciaMaxCarro:
            return "carro"
        else:
            return None
