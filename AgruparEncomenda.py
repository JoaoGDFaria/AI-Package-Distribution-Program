import info
from Entrega import Entrega

class AgruparEncomenda:
    def __init__(self, pontosRecolha, gl, g):
        self.listaEncomendas = {}
        self.pontosRecolha = pontosRecolha
        self.gl = gl
        self.g = g

    def adicionarEncomenda(self, encomenda, veiculo, path, pontoRecolha):
        if veiculo in self.listaEncomendas:
            if pontoRecolha in self.listaEncomendas[veiculo]:
                self.listaEncomendas[veiculo][pontoRecolha].append((encomenda, path))
            else:
                self.listaEncomendas[veiculo][pontoRecolha] = [(encomenda, path)]
        else:
            self.listaEncomendas[veiculo] = {pontoRecolha: [(encomenda, path)]}

    def agruparPorEstafeta(self, algoritmo, fileName):
        flag = False
        for veiculo, dictPontoRecolha in self.listaEncomendas.items():
            for pontoRecolha, all_encomendas in dictPontoRecolha.items():
                if len(all_encomendas) == 1:
                    encomenda = all_encomendas[0][0]
                    path = all_encomendas[0][1]

                    self.listaEncomendas[veiculo][pontoRecolha].remove((encomenda, path))
                    estafeta = self.gl.get_estafeta_available_by_location(path[0], veiculo)
                    if estafeta is None:
                        flag = True
                        encomenda.redoEncomendaPath(algoritmo)
                    else:
                        estafeta.efetuarEncomenda(path, encomenda.tempoInicio, [encomenda.localEntrega], encomenda.g, [encomenda], encomenda.peso, encomenda.volume, self.pontosRecolha, fileName)
                    break


                elif len(all_encomendas) > 0:
                    peso_atual = 0
                    volume_atual = 0
                    lista_entrega = []

                    all_encomendas_ordered = sorted(all_encomendas, key=lambda x: (x[0].prazoLimite-x[0].tempoInicio))

                    for encomenda, path in all_encomendas_ordered:
                        if peso_atual + encomenda.peso <= info.infoPesoMaximo[veiculo] and volume_atual + encomenda.volume <= info.infoVolumeMaximo[veiculo]:
                            lista_entrega.append(encomenda)
                            peso_atual += encomenda.peso
                            volume_atual += encomenda.volume
                            self.listaEncomendas[veiculo][pontoRecolha].remove((encomenda, path))
                        else:

                            Entrega(lista_entrega, self.g, self.pontosRecolha, self.gl, algoritmo, veiculo, peso_atual, volume_atual, fileName)

                            peso_atual = encomenda.peso
                            volume_atual = encomenda.volume
                            lista_entrega = [encomenda]
                            self.listaEncomendas[veiculo][pontoRecolha].remove((encomenda, path))

                    Entrega(lista_entrega, self.g, self.pontosRecolha, self.gl, algoritmo, veiculo, peso_atual, volume_atual, fileName)

        if flag is True:
            self.agruparPorEstafeta(algoritmo, fileName)



    def imprimirEncomendas(self):
        print("\n")
        for veiculo, pontoRecolha_dict in self.listaEncomendas.items():
            print(f"Veiculo: {veiculo}")
            for pontoRecolha, encomendas_paths_list in pontoRecolha_dict.items():
                print(f"  Ponto de Recolha: {pontoRecolha}")
                for encomenda, path in encomendas_paths_list:
                    print(f"    Encomenda: {encomenda.id}, Path: {path}")
        print("\n\n")
