import sqlite3
from datetime import datetime, timedelta
from tinydb import TinyDB, Query
import re

db_tarefas = TinyDB(r'.\banco_tarefas.json')
db_status = TinyDB(r'status_tarefas.json')
Localizar_Informacoes = Query()

def inserir_tarefa():
    while True:
        nome_tarefa = input('Dê um nome para a tarefa: ')
        nome_tarefa = manutencao_caracteres(nome_tarefa)
        consulta_tarefa_existente = listar_tarefas(4, nome_tarefa)
        if nome_tarefa == 'Sair':
            print('Nome inválido. "Sair" é uma palavra reservada e não pode ser usada.')
        elif len(consulta_tarefa_existente) == 0:
            break
        else:
            print(f'Já existe uma tarefa com o nome "{nome_tarefa}" cadastrada, informe um nome diferente.')
    categoria_tarefa = input('Qual a categoria? ')
    categoria_tarefa = manutencao_caracteres(categoria_tarefa)
    while True:
        try:
            num_prioridade = int(input('Informe qual o nível de prioridade:\n1) Baixa\n2) Média\n3) Alta\n>>> '))
            if num_prioridade > 0 and num_prioridade < 4:
                break
            else:
                print('Nível de prioridade inválido. Digite apenas números entre 1 e 3\n1 para prioridade Baixa\n2 para prioridade média\n3 para prioridade alta.')
        except:
            print('Nível de prioridade inválido. Digite apenas números entre 1 e 3\n1 para prioridade Baixa\n2 para prioridade média\n3 para prioridade alta.')
    print('Vamos definir o status da sua tarefa.\nOs status cadastrados são:')
    for index, info in enumerate(db_status.all()):
        status_cadastrado: str = info['status']
        if index == 0:
            print('0) Cadastrar novo Status')
            print(f'{index + 1}) {status_cadastrado.capitalize()}')
        else:
            print(f'{index + 1}) {status_cadastrado.capitalize()}')
    while True:
        try:
            status_tarefa = int(input('Selecione o número correspondente ao status cadastrado:\n>>> '))
            if status_tarefa == 0:
                novo_status = input('Informe o novo status:\n>>> ')
                status = {"status": manutencao_caracteres(novo_status)}
                db_status.insert(status)
                break
            elif status_tarefa > 0 and status_tarefa <= len(db_status.all()):
                todos_status = db_status.all()
                status = todos_status[status_tarefa - 1]['status']
                break
            else:
                print(f'Status com o índice {status_tarefa} não encontrado.')
        except:
            print('Você precisa informar o número do índice passado')
    while True:
        data_inicio = input('Informe a data para iniciar a tarefa no formato DD/MM/AAAA:\n>>> ')
        if verificar_data(data_inicio):
            break
        else:
            print('Data inválida, tente novamente.')
    while True:
        try:
            tem_data_fim = int(input('Você quer registrar uma previsão para fim desta tarefa?\n1) Sim\n2) Não\n>>> '))
            validador, resposta = duas_opcoes(tem_data_fim)
            if validador:
                break
            else:
                print('Opção inválida, tente novamente!')
        except:
            print('Você precisa digitar um número válido')
    if resposta == 'Sim':
        while True:
            data_fim = input(f'Informe a data de fim previsto para a tarefa {nome_tarefa} no formato DD/MM/AAAA:\n>>> ')
            if verificar_data(data_inicio):
                break
            else:
                print('Data inválida, tente novamente.')
    else:
        data_fim == "N/A"
    nova_tarefa = {
        "data_inclusao": datetime.now().strftime('%d/%m/%Y'),
        "data_inicio": data_inicio,
        "nome_tarefa": nome_tarefa,
        "categoria": categoria_tarefa,
        "prioridade": nivel_prioridade(num_prioridade),
        "data_prevista_fim": data_fim,
        "data_fim": "N/A",
        "status": status
    }
    db_tarefas.insert(nova_tarefa)
    print('Tarefa inserida com sucesso!')

def duas_opcoes(opcao):
    if opcao == 1:
        return (True, 'Sim')
    elif opcao == 2:
        return (True, 'Não')
    else:
        return (False, False)

def buscar_tarefas():
    lista_tipos = ['Categoria', 'Prioridade', 'Status']
    while True:
        try:
            tipo = int(input('Informe qual o tipo de consulta você deseja fazer:\n1) Categoria\n2) Prioridade\n3) Status\n4) Todas\n>>> '))
            if tipo in range(1, 5):
                break
            else:
                print('Índice de consulta inválido, tente novamente.')
        except:
            print('Tipo de consulta inválido, tente novamente.')
    if tipo < 4:
        tipo_identificado = lista_tipos[tipo - 1]
        descricao = input(f'Informe qual {tipo_identificado} você deseja consultar:\n>>> ')
        descricao = manutencao_caracteres(descricao)
        tarefas_encontradas = listar_tarefas(tipo, descricao)
        if len(tarefas_encontradas) == 0:
            print(f'Nenhuma tarefa encontrada com "{tipo_identificado}: {descricao}" encontrada.')
        else:
            print(imprimir_tarefas(tarefas_encontradas))
    else:
        print(imprimir_tarefas(db_tarefas.all()))

def concluir_tarefa():
    while True:
        nome_pesquisa_tarefa = input('Informe o nome da tarefa que deseja concluir ou digite "Sair" para encerrar:\n>>> ')
        nome_pesquisa_tarefa = manutencao_caracteres(nome_pesquisa_tarefa)
        if nome_pesquisa_tarefa == 'sair':
            break
        else:
            consulta_tarefa_existente = listar_tarefas(4, nome_pesquisa_tarefa)
            if len(consulta_tarefa_existente) == 0:
                print(f'Nenhuma tarefa encontrada com o nome "{nome_pesquisa_tarefa}". Tente novamente.')
            else:
                if consulta_tarefa_existente[0]['status'] == 'concluida' or consulta_tarefa_existente[0]['status'] == 'cancelada':
                    print('Esta tarefa já está finalizada e não pode ser alterada.')
                    break
                lista_status_conclusao = ['concluida', 'cancelada']
                while True:
                    try:
                        num_descricao_conclusao = int(input('Com qual status você deseja encerrar a tarefa?\n1) Concluída\n2) Cancelada\n3) Sair\n>>> '))
                        if num_descricao_conclusao in range(1, 4):
                            descricao_conclusao = lista_status_conclusao[num_descricao_conclusao - 1]
                            break
                        else:
                            print('Índice inválido, tente novamente.')
                    except:
                        print('Opção inválida, tente novamente.')
                if num_descricao_conclusao == 3:
                    print('Nenhuma tarefa concluída ou cancelada.')
                    break
                db_tarefas.update({"data_fim": datetime.now().strftime('%d/%m/%Y'), "status": descricao_conclusao}, Localizar_Informacoes.nome_tarefa == nome_pesquisa_tarefa)
                print(f'Tarefa {nome_pesquisa_tarefa} concluída com sucesso.')
                break

def nivel_prioridade(nivel):
    if nivel == 1:
        return "Baixa"
    elif nivel == 2:
        return "Média"
    else:
        return "Alta"

def verificar_data(data):
    padrao = r'^\d{2}/\d{2}/\d{4}$'
    
    if re.match(padrao, data):
        dia, mes, ano = map(int, data.split('/'))
        meses_com_31_dias = [1, 3, 5, 7, 8, 10, 12]
        
        if mes < 1 or mes > 12:
            return False
        
        if mes in meses_com_31_dias:
            if dia < 1 or dia > 31:
                return False
        elif mes == 2:
            if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
                if dia < 1 or dia > 29:
                    return False
            else:
                if dia < 1 or dia > 28:
                    return False
        else:
            if dia < 1 or dia > 30:
                return False
        
        return True
    else:
        return False

def listar_tarefas(tipo, descricao):
    if tipo == 1:
        lista_de_tarefas = db_tarefas.search(Localizar_Informacoes.categoria == descricao)
    elif tipo == 2:
        lista_de_tarefas = db_tarefas.search(Localizar_Informacoes.prioridade == descricao)
    elif tipo == 3:
        lista_de_tarefas = db_tarefas.search(Localizar_Informacoes.status == descricao)
    elif tipo == 4:
        lista_de_tarefas = db_tarefas.search(Localizar_Informacoes.nome_tarefa == descricao)
    return lista_de_tarefas

def manutencao_caracteres(texto: str):
    especiais = ["á", "à", "â", "ã", "ä", "é", "è", "ê", "ë", "í", "ì", "î", "ï", "ó", "ò", "ô", "õ", "ö", "ú", "ù", "û", "ü", "ç"]
    mapa = {
        "a": ["á", "à", "â", "ã", "ä"],
        "e": ["é", "è", "ê", "ë"],
        "i": ["í", "ì", "î", "ï"],
        "o": ["ó", "ò", "ô", "ô", "ö"],
        "u": ["ú", "ù", "û", "ü"],
        "c": ["ç"]
    }
    novo_texto = ''
    for letra in texto.lower():
        if letra in especiais:
            for sub in mapa:
                if letra in mapa[sub]:
                    novo_texto += sub
                    break
        else:
            novo_texto += letra
    return novo_texto

def imprimir_tarefas(lista):
    retorno = 'Tarefas encontradas:'
    for tarefa in lista:
        nome_tarefa = tarefa['nome_tarefa']
        data_inicio = tarefa['data_inicio']
        categoria = tarefa['categoria']
        prioridade = tarefa['prioridade']
        data_prevista_fim = tarefa['data_prevista_fim']
        status = tarefa['status']
        data_fim = tarefa['data_fim']
        msg = f'\n\nTarefa: {nome_tarefa.capitalize()}\nData de início: {data_inicio}\nCategoria: {categoria.capitalize()}\nPrioridade: {prioridade.capitalize()}\nPrevisão de término: {data_prevista_fim}\nStatus: {status.capitalize()}\nData conclusão: {data_fim}'
        retorno += msg
    return retorno
