import math
import os
from datetime import timedelta

import info
import random

class Estafeta:

    def __init__(self, veiculo, localizacao, nome, rating, num, gl):
        self.veiculo = veiculo
        self.rating = rating
        self.nome = nome
        self.numentregas = num
        self.localizacao = localizacao
        self.pesoMaximo = info.infoPesoMaximo[veiculo]
        self.volumeMaximo = info.infoVolumeMaximo[veiculo]
        self.velocidadeMedia = info.infoVelocidadeMedia[veiculo]
        self.perdaPorKg = info.infoPerdaPorKg[veiculo]
        self.disponivel = True
        self.dataDisponivel = None
        self.gl = gl
        self.id = self.gl.add_estafeta(self)


    def calculaVelocidadeMedia(self, pesoTotalEncomendas):
        self.velocidadeMedia = round(info.infoVelocidadeMedia[self.veiculo] - (info.infoPerdaPorKg[self.veiculo] * pesoTotalEncomendas), 2)


    def efetuarEncomenda(self, path, tempoInicio, locaisEntrega, graph, listaEncomendas, pesoTotalEncomendas, volumeTotalEncomendas, pontosRecolha, fileName):
        self.disponivel = False
        name = ""

        for encomenda in listaEncomendas:
            encomenda.idEstafeta = self.id
            name += str(encomenda.id) + ","
        name = name[:-1]

        directory_path = f"./Outputs/{fileName}/Entregas/"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        with open(f'./Outputs/{fileName}/Entregas/Entrega{name}.txt', 'a', encoding='utf-8') as file:
            file.truncate(0)

            print(f"Estafeta: {self.nome}", file=file)
            print(f"Peso Total: {pesoTotalEncomendas}", file=file)
            print(f"Volume Total: {volumeTotalEncomendas}", file=file)
            print(f"Inicio da viagem: {encomenda.tempoInicio}\n", file=file)

            tempoFinal = tempoInicio + timedelta(minutes=len(locaisEntrega))
            distancia_percorrida = 0
            distancia_acumulativa = 0
            caminho_anterior = path[0]
            encomenda = None
            flag = False

            for caminho in path:
                self.localizacao = caminho

                print(caminho, file=file)

                distancia_percorrida += graph.get_arc_cost(caminho_anterior, caminho)
                distancia_acumulativa += distancia_percorrida

                if caminho in pontosRecolha:
                    if flag is False:
                        print("    --> Ponto de Recolha\n", file=file)
                    flag = True


                if flag:
                    while caminho in locaisEntrega:  # Entrega

                        for encomenda in listaEncomendas:
                            if encomenda.localEntrega == caminho:
                                listaEncomendas.remove(encomenda)
                                break

                        locaisEntrega.remove(caminho)


                        tempoGastoPorEncomenda = (tempoFinal + timedelta(hours=(distancia_percorrida / self.velocidadeMedia)) + timedelta(minutes=1)).replace(second=0, microsecond=0)
                        tempoFinal = tempoGastoPorEncomenda
                        distancia_percorrida = 0

                        (rating, atraso) = encomenda.penalizacaoEncomenda(tempoGastoPorEncomenda)

                        hours1, remainder1 = divmod((tempoFinal-tempoInicio).seconds, 3600)
                        minutes1 = remainder1 // 60

                        hours2, remainder2 = divmod(atraso.seconds, 3600)
                        minutes2 = remainder2 // 60

                        cliente = self.gl.get_cliente(encomenda.idCliente)
                        #ratingCliente = cliente.avaliarEstafeta(hours1, minutes1, hours2, minutes2, self.nome, encomenda.preco, encomenda.id)

                        ratingEntrega = round(rating, 1)

                        self.rating = round(((self.rating * self.numentregas) + ratingEntrega) / (self.numentregas + 1), 1)
                        self.numentregas += 1
                        encomenda.tempoEntrega = tempoFinal
                        encomenda.rating = ratingEntrega

                        distancia_em_10km = distancia_acumulativa // 10
                        if distancia_em_10km == 0: distancia_em_10km = 1
                        taxa = 1

                        if atraso.seconds >0: taxa = info.taxaAtraso["taxa"]
                        encomenda.preco = round((encomenda.preco + (distancia_em_10km * info.taxaEntrega[self.veiculo])*taxa), 2)

                        print(f"    --> Entrega encomenda {encomenda.id}\n"
                              f"            Hora de entrega {tempoFinal}\n"
                              f"            Atraso: {atraso}\n"
                              f"            Rating: {ratingEntrega}\n", file=file)

                        pesoTotalEncomendas -= encomenda.peso
                        self.calculaVelocidadeMedia(pesoTotalEncomendas)

                caminho_anterior = caminho
            # Redefine tudo para o estado inicial
            self.velocidadeMedia = info.infoVelocidadeMedia[self.veiculo]
            self.dataDisponivel = tempoFinal

            print(f"\nFim da viagem: {tempoFinal}\n", file=file)
            #df.at[row, 'Tempo de entrega'] = tempoFinal - tempoInicio

            #self.gl.printAllGlobal()
