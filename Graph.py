import math

from Nodo import Node

class Graph:

    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}  # dicionario para armazenar os nodos e arestas
        #self.m_h = {}  # dicionario para posterirmente armazenar as heuristicas para cada nodo -< pesquisa informada


    # Adicionar as arestas ao grafo
    def add_edge(self, node1, node2, weight):
        n1 = Node(node1)
        n2 = Node(node2)
        if (n1 not in self.m_nodes):
            n1_id = len(self.m_nodes)
            n1.setId(n1_id)
            self.m_nodes.append(n1)
            self.m_graph[node1] = []

        if (n2 not in self.m_nodes):
            n2_id = len(self.m_nodes)
            n2.setId(n2_id)
            self.m_nodes.append(n2)
            self.m_graph[node2] = []

        self.m_graph[node1].append((node2, weight))

        if not self.m_directed:
              self.m_graph[node2].append((node1, weight))


    # Devolver o custo de uma determianda aresta (caminho entre 2 nodos)
    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        a = self.m_graph[node1]
        for (nodo, custo) in a:
            if nodo == node2:
                custoT = custo

        return custoT


    # Para um determinado caminho, calcular o seu custo associado
    def calcula_custo(self, caminho):
        custo = 0
        i = 0
        while i + 1 < len(caminho):
            custo = custo + self.get_arc_cost(caminho[i], caminho[i + 1])
            i = i + 1
        return custo