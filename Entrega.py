import math
from itertools import permutations



class Entrega:
    def __init__(self, listaEncomendas, graph, pontosRecolha, gl, algorithm, veiculo, pesoTotal, volumeTotal, fileName):
        self.listaEncomendas = listaEncomendas
        self.graph = graph
        self.tempoInicio = listaEncomendas[0].tempoInicio
        self.locaisEntrega = [encomenda.localEntrega for encomenda in self.listaEncomendas]
        self.pesoTotalEncomendas = pesoTotal
        self.volumeTotalEncomendas = volumeTotal
        self.pontosRecolha = pontosRecolha
        self.gl = gl
        self.veiculo = veiculo
        self.fileName = fileName

        self.melhorCaminho(algorithm)



    def melhorCaminho(self, algorithmFunction):
        all_permutations_path = list(permutations(self.locaisEntrega))
        #start_time = perf_counter()
        list_information = []
        melhorEntregaVeiculo = {}
        melhorCusto = math.inf
        melhorPath = []


        #print("\n\nListagem de todos os caminhos possíveis:", file= self.file)

        # Para todos os pontos de recolha da encomenda
        for pontoRecolha in self.pontosRecolha:
            for path in all_permutations_path:


                all_paths = [pontoRecolha] + list(path)


                # Verificar todos os estafetas disponíveis com base no peso total da encomenda
                for localizacao_estafeta in self.gl.get_all_estafetas_available_veiculo(self.veiculo):

                    (path, custo) = self.calculaMelhorCaminho(localizacao_estafeta, all_paths, algorithmFunction)

                    #aux = "Inicio:"+posicaoInicial + "||" + str(all_paths)
                    #print(aux)

                    if custo < melhorCusto:
                        melhorPath = path
                        melhorCusto = round(custo, 2)

        if melhorPath == []:
            if self.veiculo == "bicicleta":
                self.veiculo = "mota"
                self.melhorCaminho(algorithmFunction)
            elif self.veiculo == "mota":
                self.veiculo = "carro"
                self.melhorCaminho(algorithmFunction)
            else:
                print("Nao existem estafetas disponiveis neste momento para essa encomenda")
                return
        else:
            estafeta = self.gl.get_estafeta_available_by_location(melhorPath[0], self.veiculo)
            estafeta.calculaVelocidadeMedia(self.pesoTotalEncomendas)
            estafeta.efetuarEncomenda(melhorPath, self.tempoInicio, self.locaisEntrega, self.graph, self.listaEncomendas, self.pesoTotalEncomendas, self.volumeTotalEncomendas, self.pontosRecolha, self.fileName)


    def calculaMelhorCaminho(self, localinicial, locaisentrega, algorithmFunction):
        custo_final = 0
        caminho_final = []

        for local in locaisentrega:
            (path, custo) = algorithmFunction(localinicial, local)
            localinicial = local

            if caminho_final != [] and caminho_final[-1] == path[0]:
                caminho_final.extend(path[1:])
            else:
                caminho_final.extend(path)
            custo_final += custo

        return caminho_final, custo_final

