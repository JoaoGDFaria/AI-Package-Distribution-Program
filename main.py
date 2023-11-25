from Cliente import Cliente
from Estafeta import Estafeta
from Global import Global
from datetime import datetime
import csv
import os


datetimeStart = datetime(year=2023, month=11, day=22, hour=18, minute=30)

gl = Global()

estaf = os.path.join('files', 'estafetas.csv')
cli = os.path.join('files', 'clientes.csv')

with open(estaf, 'r') as estafetas:
    leitor_csv = csv.DictReader(estafetas)

    for linha in leitor_csv:
        veic = linha['veiculo']
        freg = linha['freguesia']
        no = linha['nome']
        Estafeta(veic, freg, no, gl)

with open(cli, 'r') as clientes:
    leitor_csv = csv.DictReader(clientes)

    for linha in leitor_csv:
        nome = linha['nome']
        freg = linha['localização']
        Cliente(nome, freg, gl)

# gl.printAllGlobal()
