import math
from datetime import timedelta
import info


class Encomenda:

    def __init__(self, peso, preco, volume, localEntrega, idCliente, tempoInicio, prazoLimite, pontosRecolha, gl, g, ag):
        self.idCliente = idCliente
        self.peso = peso
        self.preco = preco
        self.volume = volume
        self.localEntrega = localEntrega
        self.tempoInicio = tempoInicio
        self.prazoLimite = prazoLimite
        self.tempoEntrega = None
        self.rating = None
        self.idEstafeta = None
        self.pontosRecolha = pontosRecolha
        self.gl = gl
        self.g = g
        self.ag = ag
        self.id = self.gl.add_encomenda(self)
        self.melhorCaminhoEncomenda(self.g.procura_BFS)


    def melhorCaminhoEncomenda(self, algorithmFunction):
        #start_time = perf_counter()
        list_information = []
        melhorEntregaVeiculo = {}


        #print("\n\nListagem de todos os caminhos possíveis:" )

        # Para todos os pontos de recolha da encomenda
        for pontoRecolha in self.pontosRecolha:


            all_paths = [pontoRecolha, self.localEntrega]


            # Verificar todos os estafetas disponíveis com base no peso total da encomenda
            for localizacao_veiculo in self.gl.get_all_estafetas_available(self.peso):

                posicaoInicial = localizacao_veiculo[0]
                veiculo = localizacao_veiculo[1]

                aux = "Inicio:"+posicaoInicial + "||" + str(all_paths)
                print(aux)


                (path, custo) = self.calculaMelhorCaminho(posicaoInicial, all_paths, algorithmFunction)


                if veiculo in melhorEntregaVeiculo:
                    (p, c, pr) = melhorEntregaVeiculo.get(veiculo)
                    if custo < c:
                        melhorEntregaVeiculo[veiculo] = (path, round(custo, 2), pontoRecolha)
                else:
                    melhorEntregaVeiculo[veiculo] = (path, round(custo, 2), pontoRecolha)



        ab = melhorEntregaVeiculo.get("bicicleta")
        if ab is None:
            print("\nNão existe possibilidade de entrega da bicicleta")
            list_information.append(None)
        else:
            print(f"\nPath ideal bicicleta: {ab[0]}")
            print(f"Custo ideal bicicleta: {ab[1]}")
            velocidade_media = self.calculaVelocidadeDeEncomenda(ab[0])
            print(f"Velocidade média mínima: {velocidade_media} km/h")
            print(f"Peso: {self.peso} kg" )
            list_information.append((ab[0], velocidade_media, ab[1], ab[2]))


        am = melhorEntregaVeiculo.get("mota")
        if am is None:
            print("\nNão existe possibilidade de entrega da mota")
            list_information.append(None)
        else:
            print(f"\nPath ideal mota: {am[0]}" )
            print(f"Custo ideal mota: {am[1]}" )
            velocidade_media = self.calculaVelocidadeDeEncomenda(am[0])
            print(f"Velocidade média mínima: {velocidade_media} km/h")
            print(f"Peso: {self.peso} kg" )
            list_information.append((am[0], velocidade_media, am[1], am[2]))


        ac = melhorEntregaVeiculo.get("carro")
        if ac is None:
            print("\nNão existe possibilidade de entrega da mota")
            list_information.append(None)
        else:
            print(f"\nPath ideal carro: {ac[0]}" )
            print(f"Custo ideal carro: {ac[1]}" )
            velocidade_media = self.calculaVelocidadeDeEncomenda(ac[0])
            print(f"Velocidade média mínima: {velocidade_media} km/h")
            print(f"Peso: {self.peso} kg" )
            list_information.append((ac[0], velocidade_media, ac[1], ac[2]))

        self.determina_veiculo(list_information)


    def distanceToEncomenda(self, path, posicaoEncomenda):
        flag = False
        distancia = 0
        posicaoAnterior = path[0]
        for posicao in path:
            distancia += self.g.get_arc_cost(posicaoAnterior, posicao)
            if posicao in self.pontosRecolha: flag = True

            if posicaoEncomenda == posicao and flag is True:
                break

            posicaoAnterior = posicao
        return round(distancia, 1)


    def calculaVelocidadeDeEncomenda(self, path):
        intervaloDeTempo = self.prazoLimite - self.tempoInicio
        intervaloDeTempoEmHoras = intervaloDeTempo.total_seconds() / 3600

        velocidadeMedia = self.distanceToEncomenda(path, self.localEntrega)/intervaloDeTempoEmHoras
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
        equacao_velocidade_bicicleta = info.infoVelocidadeMedia["bicicleta"] - (info.infoPerdaPorKg["bicicleta"] * self.peso)
        equacao_velocidade_mota = info.infoVelocidadeMedia["mota"] - (info.infoPerdaPorKg["mota"] * self.peso)
        equacao_velocidade_carro = info.infoVelocidadeMedia["carro"] - (info.infoPerdaPorKg["carro"] * self.peso)

        print(f"\nVelocidade média da bicicleta: {equacao_velocidade_bicicleta} km/h")
        print(f"Velocidade média da mota: {equacao_velocidade_mota} km/h")
        print(f"Velocidade média do carro: {equacao_velocidade_carro} km/h")

        if (list_information[0] is not None and list_information[0][1]<=equacao_velocidade_bicicleta):
            veiculo = "bicicleta"
            path = list_information[0][0]
            pontoRecolha = list_information[0][3]

        elif (list_information[1] is not None and list_information[1][1]<=equacao_velocidade_mota):
            veiculo = "mota"
            path = list_information[1][0]
            pontoRecolha = list_information[1][3]

        elif (list_information[2] is not None and list_information[2][1]<=equacao_velocidade_carro):
            veiculo = "carro"
            path = list_information[2][0]
            pontoRecolha = list_information[2][3]

        else:
            print(f"Não existe nenhum estafeta" )
            return

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

