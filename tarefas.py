import sqlite3
from datetime import datetime, timedelta
from tinydb import TinyDB, Query
from funcoes import inserir_tarefa, buscar_tarefas, concluir_tarefa

db = TinyDB(r'.\banco_tarefas.json')

print('*' * 32)
print('-' * 4 + ' GERENCIADOR DE TAREFAS ' + '-' * 4)
print('*' * 32)

def menu():
    # Abertura
    while True:
        try:
            opcao = int(input('Digite a opção desejada:\n1) Cadastrar Tarefa\n2) Consultar Tarefas\n3) Encerrar Tarefa\n4) Sair\n>>> '))
            if opcao <= 0 or opcao >= 5:
                print('Opção inválida.\nPara cadastrar uma nova tarefa você pode digitar 1.\nPara consultar tarefas você pode digitar 2\nPara selecionar uma tarefa para concluir, você pode digitar 3.')
                continue
        except:
            print('Opção inválida.\nPara cadastrar uma nova tarefa você pode digitar 1.\nPara consultar tarefas você pode digitar 2\nPara selecionar uma tarefa para concluir, você pode digitar 3.')
            continue
        if opcao == 1:
            inserir_tarefa()
        elif opcao == 2:
            buscar_tarefas()
        elif opcao == 3:
            concluir_tarefa()
        else:
            break

if __name__ == "__main__":
    menu()