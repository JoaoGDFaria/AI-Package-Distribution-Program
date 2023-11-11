class Global:
    def __init__(self):
        self.todos_clientes = {}
        self.todos_encomendas = {}
        self.todos_estafetas = {}

    def add_cliente(self, cliente):
        total_length = len(self.todos_clientes)
        self.todos_clientes[total_length+1] = cliente

    def add_encomenda(self, encomenda):
        total_length = len(self.todos_encomendas)
        self.todos_encomendas[total_length+1] = encomenda

    def add_estafeta(self, estafeta):
        total_length = len(self.todos_estafetas)
        self.todos_estafetas[total_length+1] = estafeta


    def get_cliente(self, id):
        return self.todos_clientes.get(id, None)

    def get_encomenda(self, id):
        return self.todos_encomendas.get(id, None)

    def get_estafeta(self, id):
        return self.todos_estafetas.get(id, None)

