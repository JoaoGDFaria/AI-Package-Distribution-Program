import math
import os
from datetime import timedelta,datetime
import info

class Encomenda:

    def __init__(self, peso, preco, volume, localEntrega, idCliente, tempoInicio, prazoLimite, pontosRecolha, gl, g, ag, algorithmFunction, fileName):
        self.idCliente = idCliente
        self.peso = peso
        self.preco = preco
        self.volume = volume
        self.localEntrega = localEntrega
        self.tempoInicio = tempoInicio
        self.prazoLimite= datetime.strptime(prazoLimite,"%Y-%m-%d %H:%M:%S")
        self.tempoEntrega = None
        self.rating = None
        self.idEstafeta = None
        self.pontosRecolha = pontosRecolha
        self.gl = gl
        self.g = g
        self.ag = ag
        self.id = self.gl.add_encomenda(self)
        self.fileName = fileName

        directory_path = f"./Outputs/{fileName}/Individuais/"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        with open(f'./Outputs/{self.fileName}/Individuais/Encomenda{self.id}.txt', 'a', encoding='utf-8') as file:
            file.truncate(0)
            self.file = file
            self.melhorCaminhoEncomenda(algorithmFunction)

    def melhorCaminhoEncomenda(self, algorithmFunction):
        list_information = []
        melhorEntregaVeiculo = {}


        # Para todos os pontos de recolha da encomenda
        for pontoRecolha in self.pontosRecolha:


            all_paths = [pontoRecolha, self.localEntrega]


            # Verificar todos os estafetas disponíveis com base no peso total da encomenda
            for localizacao_veiculo in self.gl.get_all_estafetas_available(self.peso, self.volume):

                posicaoInicial = localizacao_veiculo[0]
                veiculo = localizacao_veiculo[1]

                (path, custo) = self.calculaMelhorCaminho(posicaoInicial, all_paths, algorithmFunction)


                if veiculo in melhorEntregaVeiculo:
                    (p, c, pr) = melhorEntregaVeiculo.get(veiculo)
                    if custo < c:
                        melhorEntregaVeiculo[veiculo] = (path, round(custo, 2), pontoRecolha)
                else:
                    melhorEntregaVeiculo[veiculo] = (path, round(custo, 2), pontoRecolha)



        ab = melhorEntregaVeiculo.get("bicicleta")
        if ab is None:
            print("\nNão existe possibilidade de entrega da bicicleta", file=self.file)
            list_information.append(None)
        else:
            print(f"\nPath ideal bicicleta: {ab[0]}", file=self.file)
            print(f"Custo ideal bicicleta: {ab[1]}", file=self.file)
            velocidade_media = self.calculaVelocidadeDeEncomenda(ab[0])
            print(f"Velocidade média mínima: {velocidade_media} km/h", file=self.file)
            list_information.append((ab[0], velocidade_media, ab[1], ab[2]))


        am = melhorEntregaVeiculo.get("mota")
        if am is None:
            print("\nNão existe possibilidade de entrega da mota", file=self.file)
            list_information.append(None)
        else:
            print(f"\nPath ideal mota: {am[0]}", file=self.file)
            print(f"Custo ideal mota: {am[1]}", file=self.file)
            velocidade_media = self.calculaVelocidadeDeEncomenda(am[0])
            print(f"Velocidade média mínima: {velocidade_media} km/h", file=self.file)
            list_information.append((am[0], velocidade_media, am[1], am[2]))


        ac = melhorEntregaVeiculo.get("carro")
        if ac is None:
            print("\nNão existe possibilidade de entrega da mota", file=self.file)
            list_information.append(None)
        else:
            print(f"\nPath ideal carro: {ac[0]}", file=self.file)
            print(f"Custo ideal carro: {ac[1]}", file=self.file)
            velocidade_media = self.calculaVelocidadeDeEncomenda(ac[0])
            print(f"Velocidade média mínima: {velocidade_media} km/h", file=self.file)
            list_information.append((ac[0], velocidade_media, ac[1], ac[2]))
            print(f"\nPeso: {self.peso} kg", file=self.file)
            print(f"Volume: {self.volume} L", file=self.file)
        self.determina_veiculo(list_information)


    def distanceToEncomenda(self, path):
        distancia = 0
        posicaoAnterior = path[0]
        for posicao in path:
            distancia += self.g.get_arc_cost(posicaoAnterior, posicao)
            posicaoAnterior = posicao
        return round(distancia, 1)


    def calculaVelocidadeDeEncomenda(self, path):
        intervaloDeTempo = self.prazoLimite - self.tempoInicio
        intervaloDeTempoEmHoras = intervaloDeTempo.total_seconds() / 3600
        if intervaloDeTempoEmHoras == 0: velocidadeMedia=0
        else: velocidadeMedia = self.distanceToEncomenda(path)/intervaloDeTempoEmHoras

        return round(velocidadeMedia, 2)


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


    def determina_veiculo(self, list_information):
        if self.peso > info.infoPesoMaximo["bicicleta"]:
            equacao_velocidade_bicicleta = info.infoVelocidadeMedia["bicicleta"]
        else:
            equacao_velocidade_bicicleta = round(info.infoVelocidadeMedia["bicicleta"] - (info.infoPerdaPorKg["bicicleta"] * self.peso), 2)

        if self.peso > info.infoPesoMaximo["mota"]:
            equacao_velocidade_mota = info.infoVelocidadeMedia["mota"]
        else:
            equacao_velocidade_mota = round(info.infoVelocidadeMedia["mota"] - (info.infoPerdaPorKg["mota"] * self.peso), 2)

        equacao_velocidade_carro = round(info.infoVelocidadeMedia["carro"] - (info.infoPerdaPorKg["carro"] * self.peso), 2)

        print(f"\nVelocidade média da bicicleta: {equacao_velocidade_bicicleta} km/h", file=self.file)
        print(f"Velocidade média da mota: {equacao_velocidade_mota} km/h", file=self.file)
        print(f"Velocidade média do carro: {equacao_velocidade_carro} km/h", file=self.file)

        if (list_information[0] is not None and list_information[0][1]<=equacao_velocidade_bicicleta):
            veiculo = "bicicleta"
            path = list_information[0][0]
            pontoRecolha = list_information[0][3]

        elif (list_information[1] is not None and list_information[1][1]<=equacao_velocidade_mota):
            veiculo = "mota"
            path = list_information[1][0]
            pontoRecolha = list_information[1][3]

        elif (list_information[2] is not None):
            veiculo = "carro"
            path = list_information[2][0]
            pontoRecolha = list_information[2][3]

        else:
            print(f"\nNao existem estafetas disponiveis neste momento para esta encomenda!", file=self.file)
            return

        print(f"\n----> Veículo escolhido: {veiculo}", file=self.file)
        self.ag.adicionarEncomenda(self, veiculo, path, pontoRecolha)


    # Função para determinar a penalização de uma encomenda
    # com base no seu atraso em minutos
    def penalizacaoEncomenda(self, tempoEntrega):
        rating_final = 5
        tempoMinutos = 0

        if (tempoEntrega >= self.prazoLimite):
            tempoMinutos = ((tempoEntrega - self.prazoLimite).total_seconds()) / 60
            intervalos15Minutos = math.ceil(tempoMinutos // 15)
            rating_final = 5 - (intervalos15Minutos * 0.5)
            if rating_final < 0: rating_final = 0

        return rating_final, timedelta(minutes=tempoMinutos)


    def redoEncomendaPath(self, algorithmFunction):
        with open(f'./Outputs/{self.fileName}/Individuais/Encomenda{self.id}.txt', 'a', encoding='utf-8') as file:
            file.truncate(0)
            self.file = file
            self.melhorCaminhoEncomenda(algorithmFunction)
