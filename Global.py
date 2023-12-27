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
        todas_possibilidades = set()
        for estafeta in self.todos_estafetas.values():
            if estafeta.disponivel and estafeta.veiculo == veiculo:
                todas_possibilidades.add(estafeta.localizacao)

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

    def get_cliente_by_localizacao(self, localizacao):
        for cliente in self.todos_clientes.values():
            if cliente.localizacao == localizacao:
                return cliente

        return None

    def printAllGlobal(self):
        for id, info in self.todos_clientes.items():
            print(f"ID: {id}, Nome: {info.nome}, Localizacao: {info.localizacao}, Encomendas: {info.encomendas}")
        print("-----------------------------")
        for id, info in self.todos_estafetas.items():
            print(f"ID: {id}, Nome: {info.nome}, Localizacao: {info.localizacao}, Veiculo: {info.veiculo}, Rating: {info.rating}, Número de Viagens: {info.numentregas} , Disponível: {info.disponivel}")
        print("-----------------------------")
        for id, info in self.todos_encomendas.items():
            print(f"ID: {id}, IdCliente: {info.idCliente}, Peso: {info.peso}, Preço Base: {info.preco}, Local Entrega: {info.localEntrega}, Tempo Inicio: {info.tempoInicio}, Prazo Limite: {info.prazoLimite}, Tempo Entrega: {info.tempoEntrega}, Rating: {info.rating}")

    def printAllUtilizadores(self):
        for id, info in self.todos_clientes.items():
            print(f"ID: {id}, Nome: {info.nome}, Localizacao: {info.localizacao}, Encomendas: {info.encomendas}")
        print("-----------------------------")


    def printAllEstafetas(self):
        for id, info in self.todos_estafetas.items():
            print(f"ID: {id}, Nome: {info.nome}, Localizacao: {info.localizacao}, Veiculo: {info.veiculo}, Rating: {info.rating}, Número de Viagens: {info.numentregas} , Disponível: {info.disponivel}")
        print("-----------------------------")


    def printAllEncomendas(self):
        for id, info in self.todos_encomendas.items():
            print(f"ID: {id}, IdCliente: {info.idCliente}, Peso: {info.peso}, Preço Base: {info.preco}, Local Entrega: {info.localEntrega}, Tempo Inicio: {info.tempoInicio}, Prazo Limite: {info.prazoLimite}, Tempo Entrega: {info.tempoEntrega}, Rating: {info.rating}")
        print("-----------------------------")

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
