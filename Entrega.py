from time import perf_counter

import info
from itertools import permutations
from datetime import datetime, timedelta


class Entrega:
    def __init__(self, listaEncomendas, graph, tempoInicio, tempoFim, pontosRecolha, gl, algorithm, fileName, df, row):
        self.listaEncomendas = listaEncomendas
        self.graph = graph
        self.tempoInicio = tempoInicio
        self.tempoFim = tempoFim
        self.locaisEntrega = [encomenda.localEntrega for encomenda in self.listaEncomendas]
        self.pesoTotalEncomendas = sum(encomenda.peso for encomenda in self.listaEncomendas)
        self.pontosRecolha = pontosRecolha
        self.gl = gl
        self.df = df
        self.row = row


        with open(f'./Outputs/{fileName}.txt', 'a', encoding='utf-8') as file:
            file.truncate(0)
            self.file = file
            self.melhorCaminho(algorithm)




    def melhorCaminho(self, algorithmFunction):
        all_permutations_path = list(permutations(self.locaisEntrega))
        start_time = perf_counter()
        list_information = []
        melhorEntregaVeiculo = {}


        #print("\n\nListagem de todos os caminhos possíveis:", file= self.file)

        # Para todos os pontos de recolha da encomenda
        for pontoRecolha in self.pontosRecolha:
            for path in all_permutations_path:


                all_paths = [pontoRecolha] + list(path)


                # Verificar todos os estafetas disponíveis com base no peso total da encomenda
                for localizacao_veiculo in self.gl.get_all_estafetas_available(self.pesoTotalEncomendas):

                    posicaoInicial = localizacao_veiculo[0]
                    veiculo = localizacao_veiculo[1]


                    (path, custo) = self.calculaMelhorCaminho(posicaoInicial, all_paths, algorithmFunction)

                    #aux = "Inicio:"+posicaoInicial + "||" + str(all_paths)
                    #print(aux)


                    if veiculo in melhorEntregaVeiculo:
                        (p, c) = melhorEntregaVeiculo.get(veiculo)
                        if custo < c:
                            melhorEntregaVeiculo[veiculo] = (path, round(custo, 2))
                    else:
                        melhorEntregaVeiculo[veiculo] = (path, round(custo, 2))


        ab = melhorEntregaVeiculo.get("bicicleta")
        if ab is None:
            print("\nNão existe possibilidade de entrega da bicicleta", file= self.file)
            list_information.append(None)
        else:
            print(f"\nPath ideal bicicleta: {ab[0]}", file= self.file)
            print(f"Custo ideal bicicleta: {ab[1]}", file= self.file)
            velocidade_media = self.calculaVelocidadeDeEntrega(ab[0])
            print(f"Velocidade média mínima: {velocidade_media} km/h", file= self.file)
            print(f"Peso: {self.pesoTotalEncomendas} kg", file= self.file)
            list_information.append((ab[0], velocidade_media, ab[1]))


        am = melhorEntregaVeiculo.get("mota")
        if am is None:
            print("\nNão existe possibilidade de entrega da mota", file= self.file)
            list_information.append(None)
        else:
            print(f"\nPath ideal mota: {am[0]}", file= self.file)
            print(f"Custo ideal mota: {am[1]}", file= self.file)
            velocidade_media = self.calculaVelocidadeDeEntrega(am[0])
            print(f"Velocidade média mínima: {velocidade_media} km/h", file= self.file)
            print(f"Peso: {self.pesoTotalEncomendas} kg", file= self.file)
            list_information.append((am[0], velocidade_media, am[1]))


        ac = melhorEntregaVeiculo.get("carro")
        if ac is None:
            print("\nNão existe possibilidade de entrega da mota", file= self.file)
            list_information.append(None)
        else:
            print(f"\nPath ideal carro: {ac[0]}", file= self.file)
            print(f"Custo ideal carro: {ac[1]}", file= self.file)
            velocidade_media = self.calculaVelocidadeDeEntrega(ac[0])
            print(f"Velocidade média mínima: {velocidade_media} km/h", file= self.file)
            print(f"Peso: {self.pesoTotalEncomendas} kg", file= self.file)
            list_information.append((ac[0], velocidade_media, ac[1]))

        self.determina_estafeta(list_information, start_time)


    def distanceToEncomenda(self, path, posicaoEncomenda):
        flag = False
        distancia = 0
        posicaoAnterior = path[0]
        for posicao in path:
            distancia += self.graph.get_arc_cost(posicaoAnterior, posicao)
            if posicao in self.pontosRecolha: flag = True

            if posicaoEncomenda == posicao and flag is True:
                break

            posicaoAnterior = posicao
        return round(distancia, 1)

    def calculaVelocidadeDeEntrega(self, path):
        (tempoMinimo, encomenda) = self.get_tempo_encomenda()
        intervaloDeTempo = tempoMinimo - self.tempoInicio
        intervaloDeTempoEmHoras = intervaloDeTempo.total_seconds() / 3600

        velocidadeMedia = self.distanceToEncomenda(path, encomenda.localEntrega)/intervaloDeTempoEmHoras
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


    def get_tempo_encomenda(self):
        tempoMinimo = datetime.max
        fastest = None
        for encomenda in self.listaEncomendas:
            if encomenda.prazoLimite < tempoMinimo:
                tempoMinimo = encomenda.prazoLimite
                fastest = encomenda
        return tempoMinimo, fastest


    def determina_estafeta(self, list_information, start_time):
        equacao_velocidade_bicicleta = info.infoVelocidadeMedia["bicicleta"] - (info.infoPerdaPorKg["bicicleta"] * self.pesoTotalEncomendas)
        equacao_velocidade_mota = info.infoVelocidadeMedia["mota"] - (info.infoPerdaPorKg["mota"] * self.pesoTotalEncomendas)
        equacao_velocidade_carro = info.infoVelocidadeMedia["carro"] - (info.infoPerdaPorKg["carro"] * self.pesoTotalEncomendas)

        print(f"\nVelocidade média da bicicleta: {equacao_velocidade_bicicleta} km/h", file= self.file)
        print(f"Velocidade média da mota: {equacao_velocidade_mota} km/h", file= self.file)
        print(f"Velocidade média do carro: {equacao_velocidade_carro} km/h", file= self.file)


        if (list_information[0] is not None and list_information[0][1]<=equacao_velocidade_bicicleta):
            estafeta = self.gl.get_estafeta_available_by_location(list_information[0][0][0], "bicicleta")
            finalPath = list_information[0][0]
            custo = list_information[0][2]
            vm = equacao_velocidade_bicicleta
            veiculo = "bicicleta"
            vmin = list_information[0][1]

        elif (list_information[1] is not None and list_information[1][1]<=equacao_velocidade_mota):
            estafeta = self.gl.get_estafeta_available_by_location(list_information[1][0][0], "mota")
            finalPath = list_information[1][0]
            custo = list_information[1][2]
            vm = equacao_velocidade_mota
            veiculo = "mota"
            vmin = list_information[1][1]

        elif (list_information[2] is not None and list_information[2][1]<=equacao_velocidade_carro):
            estafeta = self.gl.get_estafeta_available_by_location(list_information[2][0][0], "carro")
            finalPath = list_information[2][0]
            custo = list_information[2][2]
            vm = equacao_velocidade_carro
            veiculo = "carro"
            vmin = list_information[2][1]

        else:
            print(f"Não existe nenhum estafeta", file= self.file)
            return


        self.df.at[self.row, 'Custo'] = custo
        self.df.at[self.row, 'Velocidade média'] = f"{vm} km/h"
        self.df.at[self.row, 'Veículo'] = veiculo
        self.df.at[self.row, 'Velocidade mínima'] = f"{vmin} km/h"

        print("\n\n---------------", file= self.file)
        print(f"Nome: {estafeta.nome}", file= self.file)
        print(f"Localização Inicial: {estafeta.localizacao}", file= self.file)
        print(f"Veículo: {estafeta.veiculo}", file= self.file)


        estafeta.calculaVelocidadeMedia(self.pesoTotalEncomendas)
        print("---------------\n", file= self.file)

        timeTaken = f"{(perf_counter() - start_time) * 1000 :.2f}"
        print(f"Time taken: {timeTaken} ms\n\n", file= self.file)
        self.df.at[self.row, 'Tempo execução'] = f"{timeTaken} ms"


        print("ENTREGAS:::::::::::::::\n")
        estafeta.efetuarEncomenda(finalPath, self.tempoInicio, self.locaisEntrega, self.graph, self.listaEncomendas, self.pesoTotalEncomendas, self.pontosRecolha, self.df, self.row)

        return estafeta


