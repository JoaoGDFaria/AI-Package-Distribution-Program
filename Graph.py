import math
from queue import Queue
from Nodo import Node
import networkx as nx
import matplotlib.pyplot as plt

class Graph:

    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}  # Dicionário para armazenar os nodos e arestas
        #self.m_h = {}  # dicionario para posterirmente armazenar as heuristicas para cada nodo -< pesquisa informada


    def node_exists(self, node1):
        for node in self.m_nodes:
            if node.m_name == node1:
                return True
        print(f"Node {node1} não existe!")
        return False

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


    # Desenha o grafo
    def desenha(self, pos):
        ##criar lista de vertices
        lista_v = self.m_nodes
        lista_a = []
        g = nx.Graph()
        plt.figure(figsize=(12.8, 9.6))
        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
            for (adjacente, peso) in self.m_graph[n]:
                lista = (n, adjacente)
                # lista_a.append(lista)
                g.add_edge(n, adjacente, weight=peso)


        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
        plt.title("Freguesias de Famalicão")

        plt.draw()
        plt.show()












    # Procura em profundidade
    def procura_DFS(self, start, end, path=[], visited=set()):
        path.append(start)
        visited.add(start)

        # Se o percurso chegar ao fim, calcular o custo do caminho efetuado
        if start == end:
            custoT = self.calcula_custo(path)
            return (path, custoT)
        for (adjacente, peso) in self.m_graph[start]:
            if adjacente not in visited:
                resultado = self.procura_DFS(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado
        path.pop()  # Se nao encontra, remover o que está no caminho
        return None


    # Procura em largura
    def procura_BFS(self, start, end):

        # Definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()
        custo = 0

        # Adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # Garantir que o start node nao tem pais
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()

            # Chegou ao fim
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in self.m_graph[nodo_atual]:
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        # Reconstruir o caminho
        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()

            # Funçao calcula custo caminho
            custo = self.calcula_custo(path)
        return (path, custo)