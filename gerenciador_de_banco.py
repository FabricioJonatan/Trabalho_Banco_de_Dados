import mysql.connector

#       FUNÇÕES
class Fabrica_conexoes:
    def __init__(self, host, user, database, password):
        self.host = host
        self.user = user
        self.database = database
        self.password = password
        
    def conectar(self):
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            database = self.database,
            password = self.password
        )
        return banco

def get_tabelas(banco):
    conexao = banco.conectar()
    exec = conexao.cursor()

    exec.execute('SHOW TABLES')
    tabelas = exec.fetchall()

    exec.close()
    conexao.close()
    return tabelas

def menu_tabelas():
    print('\n   \033[35mQual tabela você gostaria de interagir?\033[m')
    contador = 1
    for tabela in tabelas:
        print(f'[ {contador} ] {tabela[0]}')
        contador += 1

def select_tabela(tabelas):
    while True:
        try:
            tabela = int(input('\n    \033[33mSua resposta : \033[m'))
            tabela -= 1
            tabela = tabelas[tabela][0]
        except:
            print('\033[31m\n    Opção inválida! por favor, digite novamente. . . \n\033[m')
        else:
            print('\033[32m\n    Tabela selecionada com sucesso!!\033[m')
            break
        
    return tabela

def get_colunas(banco, tabela):
    conexao = banco.conectar()
    exec = conexao.cursor()
    
    exec.execute(f'DESCRIBE {tabela}')
    colunas = exec.fetchall()
    
    exec.close()
    conexao.close()
    return colunas
    
def insert(banco, tabela, colunas):
    valores = []
    conexao = banco.conectar()
    exec = conexao.cursor()
    inserir = f'INSERT INTO {tabela} ('

    for coluna in range(len(colunas)):
        if coluna != len(colunas) -1:
            inserir += f'{colunas[coluna][0]}, '
        elif coluna == len(colunas) - 1:
            inserir += f'{colunas[coluna][0]}) VALUES ('

    for dado in range(len(colunas)):
        if colunas[dado][0] == 'id':
            inserir += 'DEFAULT, '
        elif dado != len(colunas) - 1:
            inserir += '%s, '
        elif dado == len(colunas) - 1:
            inserir += '%s)'
    
    for dado in range(len(colunas)):
        if colunas[dado][0] == 'id':
            default = 'DEFAULT'
        elif colunas[dado][1] == 'int':
            dado_usuario = int(input(f'Digite o(a) {colunas[dado][0]} (Digite em numero por favor) : '))
            valores.append(dado_usuario)
        elif colunas[dado][1] == 'float':
            dado_usuario = float(input(f'Digite o(a) {colunas[dado][0]} (Digite em numero por favor) : '))
            valores.append(dado_usuario)
        elif 'date' in colunas[dado][1]:
            dado_usuario = input(f'Digite o(a) {colunas[dado][0]} (ex : ano-mês-dia) : ')
            valores.append(dado_usuario)
        else:
            dado_usuario = input(f'Digite o(a) {colunas[dado][0]} : ').capitalize().strip()
            valores.append(dado_usuario)

    exec.execute(inserir, valores)
    conexao.commit()
    exec.close()
    conexao.close()
    print('\n    \033[32mDados adicionados com Sucesso!!\033[m')

def select(banco, tabela, colunas):
    print('\n', '==' * 60)
    conexao = banco.conectar()
    exec = conexao.cursor()
    exec.execute(f'SELECT * FROM {tabela}')
    dados = exec.fetchall()
    #print(dados)
    #print('{:^16}'.format(dados[0][4]))
    #print(dados[0][4])

    for coluna in colunas:
        print(f'{coluna[0]:^16}', end='')
    print('')

    for linha in range(len(dados)):
        for dado in range(len(colunas)):
            if dado == 0:
                print(f'\n{dados[linha][dado]:^16}', end='')
            else:
                print(f'{dados[linha][dado]:^16}', end='')
    print('\n', '==' * 60)

def where(banco, tabela, colunas):
    conexao = banco.conectar()
    exec = conexao.cursor()
    filtrar = f'SELECT * FROM {tabela} WHERE '
    contador = 1

    print('\n   \033[36mQual o tipo de dado que você gostaria de filtrar?\033[m')
    for coluna in colunas:
        print(f'[ {contador} ]  -- {coluna[0]}')
        contador += 1
    escolha = int(input('\n    \033[33mSua respostas : \033[m'))

    filtrar += f'{colunas[escolha-1][0]}=%s'
    while True:
        try:
            if colunas[escolha-1][1] == 'int':
                filtro = int(input(f'Digite o(a) {colunas[escolha-1][0]} de quem(o que) deseja encontrar [em números por favor] : '))
            elif 'char' in colunas[escolha-1][1]:
                filtro = input(f'Digite o(a) {colunas[escolha-1][0]}) de quem(o que) deseja encontrar : ').capitalize().strip()
            elif colunas[escolha-1][1] == 'float':
                filtro = float(input(f'Digite o(a) {colunas[escolha-1][0]}) de quem(o que) deseja encontrar [em números por favor] : '))
        except:
            print('\n       Dados Preenchidos incorretamente!!\n')
        else:
            print('\n   Coletando dados . . .')
            break
    valores = [filtro]
    exec.execute(filtrar, valores)
    dados = exec.fetchall()

    print('\n', '==' * 60)
    for coluna in colunas:
        print(f'{coluna[0]:^16}', end='')
    print('')

    for linha in range(len(dados)):
        for dado in range(len(colunas)):
            if dado == 0:
                print(f'\n{dados[linha][dado]:^16}', end='')
            else:
                print(f'{dados[linha][dado]:^16}', end='')
    print('\n', '==' * 60)

def update(banco, tabela, colunas):
    alterar = f'UPDATE {tabela} SET '
    valores = []
    conexao = banco.conectar()
    exec = conexao.cursor()
    id = int(input('\n   \033[35mDigite o id do elemento que deseja alterar : \033[m'))

    for coluna in range(len(colunas)):
        if coluna != 0 and coluna != len(colunas) - 1:
            alterar += f'{colunas[coluna][0]} = %s, '
        elif coluna == len(colunas) - 1:
            alterar += f'{colunas[coluna][0]} = %s '
        
    alterar += 'WHERE id = %s'

    for coluna in range(len(colunas)):
        if coluna != 0:
            if colunas[coluna][1] == 'int':
                dado_usuario = int(input(f'Digite o(a) {colunas[coluna][0]} (em numero por favor) : '))
            elif colunas[coluna][1] == 'float':
                dado_usuario = float(input(f'Digite o(a) {colunas[coluna][0]} (em numero por favor) : '))
            elif 'date' in colunas[coluna][1]:
                dado_usuario = input(f'Digite o(a) {colunas[coluna][0]} (ex : ano-mês-dia) : ')
            else:
                dado_usuario = input(f'Digite o(a) {colunas[coluna][0]} : ').strip().capitalize()

            valores.append(dado_usuario)
    valores.append(id)
    
    exec.execute(alterar, valores)
    conexao.commit()
    exec.close()
    conexao.close()
    print('\n    \033[32mDados alterados com Sucesso!!\033[m')

def delete(banco, tabela):
    conexao = banco.conectar()
    exec = conexao.cursor()
    id = int(input(f'\n\033[31mDigite o id do(a) {tabela} que deseja apagar : \033[m'))
    deletar = f'DELETE FROM {tabela} WHERE id = %s'
    valores = [id]

    exec.execute(deletar, valores)
    conexao.commit()
    exec.close()
    conexao.close()
    print('\n   \033[33mDados deletado com Sucesso!!\033[m')

def comando_join(banco, tabela, tabelas, colunas):    
    conexao = banco.conectar()
    exec = conexao.cursor()
    juntar = 'SELECT '
    chave_estrangueira = 0
    colunas_escolhidas = []
    coluna_cursor = tabela_cursor = tabela_cursor_join = 0
    tabelas_escolhidas = []
    multi_colunas = False
    id_tabelas = []
    

    for coluna in range(len(colunas)):
        contador = 1
        coluna_escolhida = ''
        if '_id' in colunas[coluna][0] or 'id_' in colunas[coluna][0]:
            chave_estrangueira += 1
            id_tabela = colunas[coluna][0]
            id_tabelas.append(id_tabela)
            print('\n   \033[36mQual a tabela que essa coluna está se referindo?\033[m')
            print('=========',colunas[coluna][0], '\n')

            for table in tabelas:
                print(f'[ {contador} ] -- {table[0]}')
                contador += 1
                
            while True:
                try:
                    escolha = int(input('\n    \033[33mSua respostas : \033[m'))
                    tabela_ = tabelas[escolha-1][0]
                    exec.execute(f'DESCRIBE {tabela_}')
                    coluns = exec.fetchall()
                    contador = 1
                    tabelas_escolhidas.append(tabela_)
                except:
                    print('\n   \033[31mOPÇÃO INVÁLIDA!! Digite algumas das opções acima\033[m')
                else:
                    break

            print('\n   \033[36mE qual coluna deseja que seja apresentada?\033[m')
            for colun in coluns:
                print(f'[ {contador} ] -- {colun[0]}')
                contador += 1
            
            escolha = int(input('\n    \033[33mSua respostas : \033[m'))
            coluna_escolhida = coluns[escolha-1][0]
            colunas_escolhidas.append(coluna_escolhida)
            multi_colunas = True

        if coluna == len(colunas) - 1:
            if chave_estrangueira == 0:
                break

        if coluna != len(colunas) - 1:
            if multi_colunas:
                juntar += f'{tabelas_escolhidas[tabela_cursor]}.{colunas_escolhidas[coluna_cursor]}, '
                coluna_cursor += 1
                tabela_cursor += 1
                multi_colunas = False
            else:
                juntar += f'{tabela}.{colunas[coluna][0]}, '
        else:
            if multi_colunas:
                juntar += f'{tabelas_escolhidas[tabela_cursor]}.{colunas_escolhidas[coluna_cursor]} FROM {tabela} JOIN {tabelas_escolhidas[tabela_cursor_join]} ON {tabela}.{id_tabelas[tabela_cursor_join]}={tabelas_escolhidas[tabela_cursor_join]}.{coluns[0][0]}'
                coluna_cursor += 1
                tabela_cursor_join += 1
                multi_colunas = False
            else:
                juntar += f'{tabela}.{colunas[coluna][0]} FROM {tabela} JOIN {tabela_} ON {tabela}.{id_tabela}={tabela_}.{coluns[0][0]}'

    if len(tabelas_escolhidas) > 0:
        for tabela_escolhida in tabelas_escolhidas:
            if tabela_escolhida != tabelas_escolhidas[0]:
                juntar += f' JOIN {tabelas_escolhidas[tabela_cursor_join]} ON {tabela}.{id_tabelas[tabela_cursor_join]}={tabelas_escolhidas[tabela_cursor_join]}.{coluns[0][0]} '

    coluna_cursor = tabela_cursor = 0

    if chave_estrangueira == 0:
        print('\n','==' * 45)
        print('\033[31m\nNão tem como detalhar essa tabela pois ela não possui nada para detalhar, sinto muito.\033[m\n')
        print('','==' * 45)
        return None

    else:
        print('\n', '==' * 60)
        exec.execute(juntar)
        dados = exec.fetchall()

        for coluna in colunas:
            if 'id_' in coluna[0] or '_id' in coluna[0]:
                print(f'{colunas_escolhidas[coluna_cursor]+"_"+tabelas_escolhidas[tabela_cursor]:^20}', end='')
                coluna_cursor += 1
                tabela_cursor += 1
            else:
                print(f'{coluna[0]:^20}', end='')

        for linha in range(len(dados)):
            for dado in range(len(colunas)):
                if dado == 0:
                    print(f'\n{dados[linha][dado]:^20}', end='')
                else:
                    print(f'{dados[linha][dado]:^20}', end='')
        print('\n','==' * 60)
    
def sair():
    print('\n\033[34mTenha um bom dia!!\033[m\n')


#           MENU DO USUÁRIO

conexao = Fabrica_conexoes('localhost', 'root', 'os', '')
tabelas = get_tabelas(conexao)
menu_tabelas()
tabela = select_tabela(tabelas)
colunas = get_colunas(conexao, tabela)

while True:
    print('''\n   \033[35mO que deseja fazer com esta tabela?\033[m
[ 1 ] Adicionar Dados
[ 2 ] Listar os Dados
[ 3 ] Filtrar Dados
[ 4 ] Alterar Dados
[ 5 ] Apagar Dados
[ 6 ] Listar Dados Detalhadamente
[ 7 ] Trocar Tabela
[ 8 ] Sair''')

    try:
        escolha = int(input('\n \033[36mSua resposta\033[m : '))
    
    except:
        print('\n   \033[31mDigite um numero!\033[m')

    else:
        if escolha == 1:
            insert(conexao, tabela, colunas)

        elif escolha == 2:
            select(conexao, tabela, colunas)

        elif escolha == 3:
            where(conexao, tabela, colunas)

        elif escolha == 4:
            select(conexao, tabela, colunas)
            update(conexao, tabela, colunas)

        elif escolha == 5:
            select(conexao, tabela, colunas)
            delete(conexao, tabela)
        
        elif escolha == 6:
            comando_join(conexao, tabela, tabelas, colunas)

        elif escolha == 7:
            menu_tabelas()
            tabela = select_tabela(tabelas)
            colunas = get_colunas(conexao, tabela)

        elif escolha == 8:
            sair()
            break

        else:
            print('\n   \033[31mOPÇÃO INVÁLIDA!! Digite algumas das opções acima\033[m')
