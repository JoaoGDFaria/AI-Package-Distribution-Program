from time import perf_counter

import info
from itertools import permutations
from datetime import datetime, timedelta


class Entrega:
    def __init__(self, listaEncomendas, graph, metereologia, tempoInicio, tempoFim, pontosRecolha, gl):
        self.listaEncomendas = listaEncomendas
        self.graph = graph
        self.metereologia = metereologia
        self.tempoInicio = tempoInicio
        self.tempoFim = tempoFim
        self.locaisEntrega = [encomenda.localEntrega for encomenda in self.listaEncomendas]
        self.pesoTotalEncomendas = sum(encomenda.peso for encomenda in self.listaEncomendas)
        self.pontosRecolha = pontosRecolha
        self.gl = gl

        self.melhorCaminho()

        # self.calculaVelocidadeMedia(self.metereologia, self.pesoTotalEncomendas)
        # self.localizacaoInicio = self.estafeta.localizacao


    def melhorCaminho(self):
        all_permutations_path = list(permutations(self.locaisEntrega))
        start_time = perf_counter()
        list_information = []
        melhorEntregaVeiculo = {}


        print("\n\nListagem de todos os caminhos possíveis:")

        # Para todos os pontos de recolha da encomenda
        for pontoRecolha in self.pontosRecolha:
            for path in all_permutations_path:


                all_paths = [pontoRecolha] + list(path)


                # Verificar todos os estafetas disponíveis com base no peso total da encomenda
                for localizacao_veiculo in self.gl.get_all_estafetas_available(self.pesoTotalEncomendas):

                    posicaoInicial = localizacao_veiculo[0]
                    veiculo = localizacao_veiculo[1]


                    (path, custo) = self.calculaMelhorCaminho(posicaoInicial, all_paths)

                    aux = "Inicio:"+posicaoInicial + "||" + str(all_paths)
                    print(aux)


                    if veiculo in melhorEntregaVeiculo:
                        (p, c) = melhorEntregaVeiculo.get(veiculo)
                        if custo < c:
                            melhorEntregaVeiculo[veiculo] = (path, custo)
                    else:
                        melhorEntregaVeiculo[veiculo] = (path, custo)


        ab = melhorEntregaVeiculo.get("bicicleta")
        if ab is None:
            print("\nNão existe possibilidade de entrega da bicicleta")
            list_information.append(None)
        else:
            print(f"\nPath ideal bicicleta: {ab[0]}")
            print(f"Custo ideal bicicleta: {ab[1]}")
            velocidade_media = self.calculaVelocidadeDeEntrega(ab[1])
            print(f"Velocidade média: {velocidade_media} km/h")
            print(f"Peso: {self.pesoTotalEncomendas} kg")
            list_information.append((ab[0][0], velocidade_media))


        am = melhorEntregaVeiculo.get("mota")
        if am is None:
            print("\nNão existe possibilidade de entrega da mota")
            list_information.append(None)
        else:
            print(f"\nPath ideal mota: {am[0]}")
            print(f"Custo ideal mota: {am[1]}")
            velocidade_media = self.calculaVelocidadeDeEntrega(am[1])
            print(f"Velocidade média: {velocidade_media} km/h")
            print(f"Peso: {self.pesoTotalEncomendas} kg")
            list_information.append((am[0][0], velocidade_media))


        ac = melhorEntregaVeiculo.get("carro")
        if ac is None:
            print("\nNão existe possibilidade de entrega da mota")
            list_information.append(None)
        else:
            print(f"\nPath ideal carro: {ac[0]}")
            print(f"Custo ideal carro: {ac[1]}")
            velocidade_media = self.calculaVelocidadeDeEntrega(ac[1])
            print(f"Velocidade média: {velocidade_media} km/h")
            print(f"Peso: {self.pesoTotalEncomendas} kg")
            list_information.append((ac[0][0], velocidade_media))

        self.determina_estafeta(list_information)

        print(f"\nTime taken: {(perf_counter() - start_time) * 1000 :.2f} ms\n")


    def calculaVelocidadeDeEntrega(self, distancia):
        intervaloDeTempo = self.get_tempo_encomenda() - self.tempoInicio
        intervaloDeTempoEmHoras = intervaloDeTempo.total_seconds() / 3600

        velocidadeMedia = distancia/intervaloDeTempoEmHoras
        return round(velocidadeMedia, 2)


    def calculaMelhorCaminho(self, localinicial, locaisentrega):
        custo_final = 0
        caminho_final = []

        for local in locaisentrega:
            (path, custo) = self.graph.procura_BFS(localinicial, local)
            localinicial = local

            if caminho_final != [] and caminho_final[-1] == path[0]:
                caminho_final.extend(path[1:])
            else:
                caminho_final.extend(path)
            custo_final += custo

        return caminho_final, custo_final


    def get_tempo_encomenda(self):
        tempoMinimo = datetime.max
        for encomenda in self.listaEncomendas:
            if encomenda.tempoFim < tempoMinimo:
                tempoMinimo = encomenda.tempoFim
        return tempoMinimo


    def determina_estafeta(self, list_information):
        equacao_velocidade = self.perdaPorKg * self.pesoTotalEncomendas

        self.localizacao = localizacao
        self.pesoMaximo = info.infoPesoMaximo[veiculo]
        self.velocidadeMedia = info.infoVelocidadeMedia[veiculo]
        self.perdaPorKg = info.infoPerdaPorKg[veiculo]



        if (list_information[0] is not None and list_information[0][1]<=(10)):
            estafeta = self.gl.get_estafeta_available_by_location(list_information[0][0], "bicicleta")
        elif (list_information[1] is not None and list_information[1][1]<=35):
            estafeta = self.gl.get_estafeta_available_by_location(list_information[1][0], "mota")
        elif (list_information[2] is not None and list_information[2][1]<=50):
            estafeta = self.gl.get_estafeta_available_by_location(list_information[2][0], "carro")
        else:
            print(f"Não existe nenhum estafeta ")
            return


        print("\n\n---------------")
        print(estafeta.nome)
        print(estafeta.localizacao)
        print(estafeta.veiculo)
        estafeta.calculaVelocidadeMedia()

        return estafeta


    def fazerEntrega(self):

        multiplicador = self.calculaVelocidadeMedia(self.metereologia, self.pesoTotalEncomendas)
        self.localizacaoInicio = self.estafeta.localizacao

        tempoFinal = self.tempoInicio + timedelta(minutes=self.listaEncomendas.length)

        distancia = self.melhorCaminho()  # distancia[0] -> tempo geral penalização, distancia[1] -> caminho, distancia[2] -> ordem de entrega
        tempototalpenalizacao = distancia[0]
        caminho = distancia[1]
        ordem = distancia[2]
        timeatual = 0
        iterar = 0
        numparagens = self.listaEncomendas.length
        cont = 0

        for i in caminho:
            while cont < numparagens:
                self.distanciatotal += self.graph.get_arc_cost(self.estafeta.localizacao, i)
                self.estafeta.localizacao = i

                if i == ordem[iterar]:
                    tempogastoporencomenda = self.distanciatotal / self.estafeta.velocidadeMedia
                    pen = self.estafeta.calculaPenalizacao(self.estafeta.veiculo, tempogastoporencomenda,
                                                           self.listaEncomendas[iterar].tempoEntrega)
                    timeatual += tempogastoporencomenda

                    tempogastonestaencomenda = timeatual - self.tempoInicio
                    tempogastonestaencomenda -= self.listaEncomendas[iterar].tempoEntrega
                    if tempogastonestaencomenda <= 0:
                        tempogastonestaencomenda = 0

                    ratingdadocliente = int(input(
                        f"A encomenda chegou com {tempogastonestaencomenda} segundos de atraso \n Qual a avaliação que faz da entrega? -> "))
                    rate = 5 - (pen + (5 - ratingdadocliente)) / 2
                    self.estafeta.mudaRating(rate)

                    pesoEntrega = 0
                    for encomenda in self.listaEncomendas:
                        if i == encomenda.localEntrega:
                            pesoEntrega += encomenda.peso

                    self.estafeta.velocidadeMedia += self.estafeta.perdaPorKg * pesoEntrega * multiplicador
                    cont += 1
                    iterar += 1

        # Redifine tudo para o estado inicial
        self.estafeta.velocidadeMaxima = info.infoVelocidadeMedia[self.estafeta.veiculo]
        self.estafeta.localizacao = self.locaisEntrega[-1]
        self.estafeta.disponivel = True


