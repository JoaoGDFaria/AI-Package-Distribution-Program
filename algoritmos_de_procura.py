class Algoritmos:
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
