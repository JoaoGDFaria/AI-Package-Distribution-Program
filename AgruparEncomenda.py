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

    def agruparPorEstafeta(self, algoritmo):
        encomenda = None
        path = None
        flag = False
        for veiculo, dictPontoRecolha in self.listaEncomendas.items():
            for pontoRecolha, all_encomendas in dictPontoRecolha.items():
                if len(all_encomendas) == 1:
                    encomenda = all_encomendas[0][0]
                    path = all_encomendas[0][1]

                    print(f"ENTREGA {pontoRecolha} - {veiculo}")

                    self.listaEncomendas[veiculo][pontoRecolha].remove((encomenda, path))
                    estafeta = self.gl.get_estafeta_available_by_location(path[0], veiculo)
                    if estafeta is None:
                        flag = True
                        encomenda.redoEncomendaPath(algoritmo)
                    else:
                        estafeta.efetuarEncomenda(path, encomenda.tempoInicio, [encomenda.localEntrega], encomenda.g, [encomenda], encomenda.peso, self.pontosRecolha)


                elif len(all_encomendas) > 0:
                    peso_atual = 0
                    lista_entrega = []

                    all_encomendas_ordered = sorted(all_encomendas, key=lambda x: (x[0].prazoLimite-x[0].tempoInicio))

                    for encomenda, path in all_encomendas_ordered:
                        if peso_atual + encomenda.peso <= info.infoPesoMaximo[veiculo]:
                            lista_entrega.append(encomenda)
                            peso_atual += encomenda.peso
                            self.listaEncomendas[veiculo][pontoRecolha].remove((encomenda, path))
                            print(f"------>{peso_atual}")
                            print(f"------>{lista_entrega}")
                        else:
                            print(f"------>{peso_atual}")
                            print(f"------>{lista_entrega}")

                            Entrega(lista_entrega, self.g, self.pontosRecolha, self.gl, algoritmo, veiculo, peso_atual)

                            peso_atual = encomenda.peso
                            lista_entrega = [encomenda]
                            self.listaEncomendas[veiculo][pontoRecolha].remove((encomenda, path))

                    Entrega(lista_entrega, self.g, self.pontosRecolha, self.gl, algoritmo, veiculo, peso_atual)

        if flag is True:
            self.agruparPorEstafeta(algoritmo)



    def imprimirEncomendas(self):
        print("\n")
        for veiculo, pontoRecolha_dict in self.listaEncomendas.items():
            print(f"Veiculo: {veiculo}")
            for pontoRecolha, encomendas_paths_list in pontoRecolha_dict.items():
                print(f"  Ponto de Recolha: {pontoRecolha}")
                for encomenda, path in encomendas_paths_list:
                    print(f"    Encomenda: {encomenda.id}, Path: {path}")
        print("\n\n")


