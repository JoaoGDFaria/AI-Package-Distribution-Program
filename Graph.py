import heapq
import math
from copy import deepcopy
from queue import Queue

from Nodo import Node
import networkx as nx
import matplotlib.pyplot as plt

class Graph:

    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}  # Dicionário para armazenar os nodos e arestas
        self.m_h = {}  # Dicionario para armazenar as heuristicas para cada nodo <- Pesquisa informada


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
        if node1 == node2: return 0
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

    def desenha(self, pos, pontoslevantamento):
        # Lista de vértices
        lista_v = self.m_nodes

        g = nx.Graph()
        plt.figure(figsize=(12.8, 9.6))

        # Adiciona nós e arestas ao grafo
        for nodo in lista_v:
            n = nodo.getName()
            if n in pontoslevantamento:
                # Se o nó pertence à lista pontoslevantamento, pinte-o de verde claro
                g.add_node(n, pos=pos[n], color='lightgreen')
            else:
                g.add_node(n, pos=pos[n], color='skyblue')

        for nodo in lista_v:
            n = nodo.getName()
            for (adjacente, peso) in self.m_graph[n]:
                lista = (n, adjacente)
                g.add_edge(n, adjacente, weight=peso)

        # Desenha o grafo com os rótulos e distâncias
        node_colors = [g.nodes[n]['color'] for n in g.nodes]
        nx.draw(g, pos=pos, with_labels=True, font_weight='bold', font_size=13,
                node_size=400, node_color=node_colors, edge_color='gray')

        # Adiciona rótulos de distância acima das conexões
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, font_size=8)

        plt.title("Pontos de Famalicão, Braga e Barcelos")

        plt.draw()
        plt.show()

    # Adicionar eurísticas
    def add_heuristica(self, n, euristica):
        n1 = Node(n)
        if n1 in self.m_nodes:
            self.m_h[n] = euristica


    # Ter todos os vizinhos de um determiando nodo
    def getNeighbours(self,nodo):
        lista = []
        for(adjacente, peso) in self.m_graph[nodo]:
            lista.append((adjacente, peso))
        return lista



    def getNeighboursNames(self,nodo):
        lista = []
        for (adjacente, peso) in self.m_graph[nodo]:
            lista.append(adjacente)
        return lista

    def getH(self, node):
        return self.m_h[node]



    # Procura em profundidade
    def procura_DFS(self, start, end):
        return self.procura_DFS_aux(start, end, path=[], visited=set())


    def procura_DFS_aux(self, start, end, path, visited):
        path.append(start)
        visited.add(start)

        # Se o percurso chegar ao fim, calcular o custo do caminho efetuado
        if start == end:
            custoT = self.calcula_custo(path)
            return (path, custoT)
        for (adjacente, peso) in self.m_graph[start]:
            if adjacente not in visited:
                resultado = self.procura_DFS_aux(adjacente, end, path, visited)
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



    # Procura A*
    def procura_aStar(self, start, end):

        # open_list is a list of nodes which have been visited, but who's neighbors haven't all been inspected
        open_list = {start}

        # closed_list is a list of nodes which have been visited and who's neighbors have been inspected
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            # Find a node with the lowest value of f() - evaluation function
            n = None

            # Find a node with the lowest value of f() - evaluation function
            for v in open_list:
                if n is None or g[v] + self.getH(v) < g[n] + self.getH(n):  # Mudar o valor atual
                    n = v

            # Caso o caminho não exista
            if n is None:
                print('Path does not exist!')
                return None

            # If the current node is the stop_node then we begin reconstructing the path from it to the start_node
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            # For all neighbors of the current node do
            for (m, weight) in self.getNeighbours(n):  # definir função getneighbours  tem de ter um par nodo peso
                # If the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # Otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # Remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None


    # Procura greedy
    def greedy(self, start, end):

        # open_list is a list of nodes which have been visited, but who's neighbors haven't all been inspected
        open_list = {start}

        # closed_list is a list of nodes which have been visited and who's neighbors have been inspected
        closed_list = set([])

        # parents é um dicionário que mantém o antecessor de um nodo
        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            # Encontra nodo com a menor heurística
            for v in open_list:
                if n is None or self.m_h[v] < self.m_h[n]:
                    n = v

            # Caso o caminho não exista
            if n is None:
                print('Path does not exist!')
                return None

            # Se o nodo corrente é o destino reconstruir o caminho a partir desse nodo até ao start seguindo o antecessor
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            # Para todos os vizinhos  do nodo corrente
            for (m, weight) in self.getNeighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            # Remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None
    
    def procura_UCS(self, start, end):
        # fila prioridades composta por o custo acc, o nodo atual e o caminho percorrido desde o inicio até ao nodo
        fila_prioridades = [(0, start, [])]
        visitados = []

        while fila_prioridades:
            custo_atual, nodo_atual, caminho_atual = heapq.heappop(fila_prioridades)
            # Verifica se a rua atual é a rua objetivo
            if nodo_atual == end:
                return caminho_atual + [nodo_atual], custo_atual

            # marca o nodo atual como visitado
            visitados.append(nodo_atual)

            # verifica os vizinhos do nodo atual
            for vizinho, custo in self.getNeighbours(nodo_atual):
                if vizinho not in visitados:
                    # Calcula o custo desde o nodo atual até ao seu vizinho
                    custo_total = custo_atual + custo
                    # o append substitui a lista original logo não o podemos usar
                    heapq.heappush(fila_prioridades, (custo_total, vizinho, caminho_atual + [nodo_atual]))
                    
                    

    def procura_iterativa_aux(self, src, target, maxDepth):
        if src == target:
            return [src], 0  # Retorna o caminho e a profundidade se a solução for encontrada
        if maxDepth <= 0:
            return [], -1  # Retorna um caminho vazio e profundidade -1 se atingir a profundidade máxima
        for neighbor, distance in self.m_graph.get(src, []):
            path, depth = self.procura_iterativa_aux(neighbor, target, maxDepth - 1)
            if path:
                return [src] + path, depth + 1  # Adiciona o nó atual ao caminho
        return [], -1  # Retorna um caminho vazio e profundidade -1 se não encontrar a solução

    def procura_iterativa(self, src, target):
        maxDepth = 69
        step = 3
        for i in range(0, maxDepth, step):
            path, depth = self.procura_iterativa_aux(src, target, i)
            if path:
                return path, depth
            
    # Elimina uma aresta, se possível
    def del_route(self, node1, node2):

        vizinhos1 = self.getNeighbours(node1)
        vizinhos2 = self.getNeighbours(node2)
        flag = False

        copia = deepcopy(self.m_graph)

        for (node, peso) in vizinhos1:
            if node == node2:
                self.m_graph[node1].remove((node2, peso))
                flag = True
                break

        for (node, peso) in vizinhos2:
            if node == node1:
                self.m_graph[node2].remove((node1, peso))
                flag = True
                break

        if flag:

            if self.procura_DFS(node1, node2) is not None:
                print("Aresta removida com sucesso.")

            else:
                self.m_graph = copia.copy()
                print("Não é possível remover essa aresta. Grafo ficaria desconexo.")


        else:
            print("Não é possível remover essa aresta. Nodos não são vizinhos.")
