from funcoes.funcoes import cadastrar_produto, alterar_produto, deletar_lote_ou_produto, mostrar_produtos_registrados, mostrar_produto_com_lotes, verificar_estoque, alerta_validade
import mysql.connector
from datetime import datetime
from datetime import date, timedelta

def sqlconectar():
    bd = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1234",
            database="bancoestoque"
            
        )
    return bd # retorna tudo que eu criei para função
'''
    Função para cadastrar o produto, onde vai pegar tudo que o usuário digitou,
    e jogar nas váriaveis. usando %s significa que é um valor a ser preenchido.

'''



#--------------------------------------------CADASTRAMENTO DE PRODUTO

def cadastrar_produto():
    bd = sqlconectar() # pega minha função que conecta e joga na variavel bd
    cursorbd = bd.cursor() # pega a conexão e forma o cursor
    print("-" * 40)
    print("   C A D A S T R A R   P R O D U T O         ")
    print("-" * 40)

    #------------Informações de entrada para cadastrar o produto--------------
    # Entrada do nome do produto (não pode ser vazio ou conter número)
    while True:
        nome = input("Nome do produto: ").strip().title()
        if nome and not nome.isdigit():
            break
        print("❌ Digite novamente por favor! Pois nome só pode conter letras")


    # Entrada do preço do produto (não pode ser vazio ou conter letras)   
    while True:
        preco_input = input("Preço do produto(ex: 999.99): ").strip().replace(",", ".")
        try:
            preco_real = round(float(preco_input), 2)
            if preco_real < 0:
                print("❌ O preço não pode ser negativo.")
                continue
            break
        except ValueError:
            print("❌ Preço inválido. Use apenas números (ex: 99.99).")

    #Verifico se a categoria foi digitada(Com letras apenas e se digitou número)
    while True:
        categoria = input("Categoria do produto: ").strip().title()
        if categoria and not categoria.isdigit():
            break
        print("❌ Digite novamente por favor! Pois categoria só pode conter letras")

    #Verifico se o usuario digitou(Abaixo de 100 de estoque e digitou em formato int)
    while True:
        quantidade = input("Quantidade inicial no estoque: ").strip()
        if quantidade.isdigit():
            limite_est = 100
            quantidade_prod = int(quantidade)
            if quantidade_prod < 0:
                print("O número digitado não pode ser negativo! Digite novamente!")
            elif quantidade_prod > 100:
                print(f"O valor digitado não pode ser maior que o limite de {limite_est}")
            else:
                break
        else:
            print("❌ Quantidade inválida. Use apenas números inteiros! ")
    while True:
        """
        data_lote_str é uma string que o usuário nos dá (por exemplo: '23/05/2025').
        datetime é o módulo que sabe trabalhar com datas e horas.
        strptime (do módulo datetime) reconhece que é uma data e transforma a string em uma data completa (com hora).
        "%d/%m/%Y" define o formato da data: dia/mês/ano.
        .date() serve para pegar só a parte da data (sem hora).
        """
        data_lote_str = input("Data de validade do lote (formato DD/MM/AAAA): ").strip()
        try:
            data_validade = datetime.strptime(data_lote_str, "%d/%m/%Y").date()
            break
        except ValueError:
            print("❌ Data inválida! Use o formato DD/MM/AAAA")  
    while True:
        data_lote_str2 = input("Data de entrada do lote (formato DD/MM/AAAA): ").strip()
        try:
            data_entrada = datetime.strptime(data_lote_str2, "%d/%m/%Y").date()
            break
        except ValueError:
            print("❌ Data inválida! Use o formato DD/MM/AAAA") 

    # Verfico se o lote não ficou vazio
    while True:
        numero_lote = input("Número do lote: ").strip().upper()
        if numero_lote:
            break
        else:
            print("❌Este campo não pode estar vazio! Digite novamente")


    # Verificar se produto já existe
    cursorbd.execute("SELECT id FROM produtos WHERE nome = %s", (nome,))
    resultado = cursorbd.fetchone()#aqui vai puxar o id que peguei no cursor

    if resultado:
        # Produto existe: só adiciona lote e atualiza estoque somando quantidade
        id_produto = resultado[0] #onde

        # Atualizar estoque somando quantidade
        cursorbd.execute("SELECT quantidade FROM estoque WHERE id_produto = %s", (id_produto,))
        estoque_atual = cursorbd.fetchone()
        if estoque_atual:   
            nova_quantidade = estoque_atual[0] + quantidade_prod
            cursorbd.execute("UPDATE estoque SET quantidade = %s WHERE id_produto = %s",(nova_quantidade, id_produto))
        else:
            cursorbd.execute("INSERT INTO estoque (id_produto, quantidade) VALUES (%s, %s)",
                             (id_produto, quantidade_prod))

        # Inserir lote novo para o produto
        sql_lote = """INSERT INTO lotes (id_produto, numero_lote, quantidade, data_lote_entrada, data_lote_validade) 
                      VALUES (%s, %s, %s, %s, %s)"""
        dados_lote = (id_produto, numero_lote, quantidade_prod, data_entrada, data_validade)
        cursorbd.execute(sql_lote, dados_lote)

        print(f"\nLote {numero_lote} adicionado para o produto {nome} com quantidade {quantidade_prod}.")

    else:
    
        # Inserir produto na tabela produtos
        sql_produto = "INSERT INTO produtos (nome, preco, categoria) VALUES (%s, %s, %s)"
        dados_produto = (nome, preco_real, categoria) #vai pegar as entradas que eu forneci e jogar 
        cursorbd.execute(sql_produto, dados_produto) #Junto tudo pois apenas executa dois comandos e dou commit
        bd.commit() # Tem que excutar esse primeiro por ser o principal

        # cursorbd.lastrowid pega a ultimo id para usarmos como base para o estoque e lote
        idnovo_prod = cursorbd.lastrowid

        # Inserir estoque na tabela estoque
        sql_estoque = "INSERT INTO estoque (id_produto, quantidade) VALUES (%s, %s)"
        estoque_valor = (idnovo_prod, quantidade_prod) 
        cursorbd.execute(sql_estoque, estoque_valor)


        # Inserir lote na tabela lotes
        sql_lote = "INSERT INTO lotes (id_produto, numero_lote, quantidade, data_lote_entrada, data_lote_validade) VALUES (%s, %s, %s, %s, %s)"
        dados_lote = (idnovo_prod, numero_lote, quantidade, data_entrada,data_validade)
        cursorbd.execute(sql_lote, dados_lote)

        bd.commit()
        print(f"\n\nSeu produto {nome}, valor {preco_real}, categoria {categoria}, quantidade de estoque {quantidade_prod} e numero do lote {numero_lote}")
        print("\n\n ---------------✅FOI CADASTRADO COM SUCESSO✅---------------")

    bd.commit()

    cursorbd.close()
    bd.close()

#--------------------------------------------MOSTRAR O PRODUTOS V2

def mostrar_produtos_registrados():
    bd = sqlconectar()
    cursorbd = bd.cursor()
    print("-" * 40)
    print("   M O S T R A R - P R O D U T O    ")
    print("-" * 40)
    cursorbd.execute("""SELECT produtos.nome, lotes.numero_lote, lotes.quantidade, produtos.id, produtos.preco, lotes.data_lote_entrada, lotes.data_lote_validade
                        FROM lotes
                        JOIN produtos ON lotes.id_produto = produtos.id
                     """)

    '''
    select vai selecionar as colunas, e from é de que tabela vai selecionar, join vai unir com outra tabela e 
    on vai expecficar a referência que uniu os dois. aqui usamos o id que era foreign de produtos, e referenciamos
    que é a mesma coisa que o id original ou seja o de produto
    '''
    motlote = cursorbd.fetchall() #Retorna todos os resultados da consulta e os armazena como uma lista de tuplas.

    #faço uma lista/loop e puxo todos o números
    for vasco in motlote:
        print("─" * 40)  # Linha separadora
        print(f"📦 Produto: {vasco[0]}")# número do produto na tupla
        print(f"🔢 Lote: {vasco[1]}")# número do lote na tupla
        print(f"📦 Quantidade: {vasco[2]}")# número da quantidade na tupla
        print(f"🆔 ID: {vasco[3]}")# número do id na tupla
        print(f"R$ PREÇO DO PRODUTO: {vasco[4]}")# número do entrada na tupla
        print(f"📅 Entrada do lote: {vasco[5]}")# número do entrada na tupla
        print(f"📅 Validade do produto: {vasco[6]}")# número do validade na tupla
    print("─"*40)
    print("\n")
    
    cursorbd.close()
    bd.close()
        
#--------------------------------------------Verificar estoque

def verificar_estoque():
    
    bd = sqlconectar()
    cursorbd = bd.cursor()
    print("-" * 40)
    print("   V E R I F I C A R - E S T O Q U E   ")
    print("-" * 40)
    ficaratento = 3
    limiteestoque = 2 # defino a quantidade limite de estoque


    cursorbd.execute(''' SELECT produtos.nome, estoque.quantidade
                         FROM estoque
                         JOIN produtos 
                         ON estoque.id_produto = produtos.id 

                     ''') 
    
    """
    Com o select eu escolho o que eu quero ver. nome e quantidade, from vai usar a tabela principal join vai juntar
    usando id produto eu defino que vai ser igual ao o id produto original
    """
    

    produtosestoque = cursorbd.fetchall() #retorna todo os valores, e transformna eles em uma lista de tupla. meio que "Me da tudo que retornou"
        
    alerta=[]
    atencao=[]
    tudobem=[]
    for nome_prod, quant_prod in produtosestoque:
        if quant_prod <= limiteestoque:
            alerta.append((nome_prod,quant_prod))
        elif quant_prod == ficaratento:
            atencao.append((nome_prod,quant_prod))
        else:
            tudobem.append((nome_prod,quant_prod))

    if alerta:
        print('\n\n --------⚠️  AVISO DE ESTOQUE BAIXO!⚠️-------\n')
        for vascao, vascudo in alerta:
            print(f'O produto 📦 {vascao} está com apenas {vascudo} unidades! Limite mínimo: {limiteestoque}❗')
    if atencao:
        print('\n\n --------!LEMBRETE DE PRODUTO!-------\n')
        for vascao, vascudo in atencao:
            print(f'Fique de olho o produto 📦 {vascao} está com {vascudo} unidades! Limite para ficar em atenção: {ficaratento}❗')
    if tudobem and not alerta and not atencao:
        print('\n✅ Estoque está em dia!')
    cursorbd.close()
    bd.close()

#--------------------------------------------ALTERAR OS PRODUTO JÁ CADASTRADOS
def alterar_produto():
    bd = sqlconectar()  # Conecta ao banco de dados
    cursorbd = bd.cursor()  # Cria um cursor para executar comandos SQL
    print("-" * 40)
    print("   A L T E R A R - P R O D U T O    ")
    print("-" * 40)
    cursorbd.execute("""SELECT produtos.nome, lotes.numero_lote, lotes.quantidade, produtos.id
                        FROM lotes
                        JOIN produtos ON lotes.id_produto = produtos.id
                     """)
    motlote = cursorbd.fetchall() #Retorna todos os registros como uma lista de tuplas.

    #faço uma lista/loop e puxo todos o números
    for vasco in motlote:
            print("─" * 40)  # Linha separadora
            print(f"📦 Produto: {vasco[0]}")# número do produto na tupla
            print(f"🔢 Lote: {vasco[1]}")# número do lote na tupla
            print(f"📦 Quantidade: {vasco[2]}")# número da quantidade na tupla
            print(f"🆔 ID: {vasco[3]}")# número do id na tupla
    print("─"*40)
    print("\n")

    # Menu de escolha para o usuário decidir se quer alterar o produto pelo ID ou pelo nome
    escolha = input("Você quer alterar por:\n1 - ID\n2 - Nome\nEscolha (1 ou 2): ")

    if escolha == "1":
        try:
            id_prod = int(input("Digite o ID do produto: "))  # Lê o ID do produto e converte para inteiro
        except ValueError:
            print("ID inválido. Deve ser um número.")
            return  # Encerra a função se o ID não for válido

        # Coleta os novos dados do produto
        novo_nome = input("Novo nome: ").title()
        preco1 = input("Novo preço: ")
        novo_preco = float(preco1.replace(",", "."))  # Converte o preço para float, trocando vírgula por ponto
        nova_categoria = input("Nova categoria: ").title()

        # Atualiza os dados do produto na tabela produtos
        cursorbd.execute("UPDATE produtos SET nome = %s, preco = %s, categoria = %s WHERE id = %s",
                         (novo_nome, novo_preco, nova_categoria, id_prod))
        bd.commit()  # Salva as alterações no banco

        print("Produto atualizado com sucesso!")

        # Busca os lotes relacionados ao produto
        cursorbd.execute("SELECT id, numero_lote, quantidade, data_lote_entrada, data_lote_validade FROM lotes WHERE produto_id = %s", (id_prod,))
        lotes = cursorbd.fetchall()  # Recupera todos os lotes encontrados

        if lotes:
            print("\nLotes encontrados:")
            # Mostra todos os lotes encontrados para o usuário
            for lote in lotes:
                print(f"ID do Lote: {lote[0]}, Número: {lote[1]}, Quantidade: {lote[2]}, Entrada: {lote[3]}, Validade: {lote[4]}")

            # Pede ao usuário para escolher qual lote deseja alterar
            lote_id = int(input("\nDigite o ID do lote que deseja alterar: "))
            novo_numero_lote = input("Novo número do lote: ").upper()
            nova_quantidade = int(input("Nova quantidade: "))
            nova_data_entrada = input("Nova data de entrada (AAAA-MM-DD): ")
            nova_data_validade = input("Nova data de validade (AAAA-MM-DD): ")

            # Atualiza os dados do lote na tabela lotes
            cursorbd.execute("""
                UPDATE lotes 
                SET numero_lote = %s, quantidade = %s, data_entrada = %s, data_validade = %s 
                WHERE id = %s
            """, (novo_numero_lote, nova_quantidade, nova_data_entrada, nova_data_validade, lote_id))
            bd.commit()  # Salva as alterações

            print("Lote atualizado com sucesso!")

    elif escolha == "2":
        # Alteração usando o nome do produto como referência
        nome_antigo = input("Digite o nome atual do produto: ").title()
        novo_nome = input("Novo nome: ").title()
        preco_input = input("Novo preço: ")
        novo_preco = float(preco_input.replace(",", "."))  # Converte o preço para float
        nova_categoria = input("Nova categoria: ").title()

        # Atualiza os dados do produto na tabela produtos com base no nome
        cursorbd.execute("UPDATE produtos SET nome = %s, preco = %s, categoria = %s WHERE nome = %s",
                         (novo_nome, novo_preco, nova_categoria, nome_antigo))
        bd.commit()  # Salva as alterações

        # Busca o ID do produto pelo novo nome (caso o nome tenha sido alterado)
        cursorbd.execute("SELECT id FROM produtos WHERE nome = %s", (novo_nome,))
        resultado = cursorbd.fetchone()  # Pega apenas um resultado

        if resultado:
            id_prod = resultado[0]  # Pega o ID do produto encontrado

            # Busca os lotes desse produto
            cursorbd.execute("SELECT id, numero_lote, quantidade, data_entrada, data_validade FROM lotes WHERE produto_id = %s", (id_prod,))
            lotes = cursorbd.fetchall()  # Recupera todos os lotes

            if lotes:
                print("\nLotes encontrados:")
                # Exibe os dados de cada lote
                for lote in lotes:
                    print(f"ID do Lote: {lote[0]}, Número: {lote[1]}, Quantidade: {lote[2]}, Entrada: {lote[3]}, Validade: {lote[4]}")

                # Permite alterar os dados de um lote específico
                lote_id = int(input("\nDigite o ID do lote que deseja alterar: "))
                novo_numero_lote = input("Novo número do lote: ").upper()
                nova_quantidade = int(input("Nova quantidade: "))
                nova_data_entrada = input("Nova data de entrada (AAAA-MM-DD): ")
                nova_data_validade = input("Nova data de validade (AAAA-MM-DD): ")

                # Atualiza os dados do lote selecionado
                cursorbd.execute("""
                    UPDATE lotes 
                    SET numero_lote = %s, quantidade = %s, data_entrada = %s, data_validade = %s 
                    WHERE id = %s
                """, (novo_numero_lote, nova_quantidade, nova_data_entrada, nova_data_validade, lote_id))
                bd.commit()  # Salva as alterações

                print("Lote atualizado com sucesso!")

    else:
        # Caso o usuário digite algo diferente de 1 ou 2
        print("Opção inválida!")

    # Fecha a conexão com o banco de dados
    cursorbd.close()
    bd.close()
# ------------------------------------------ mostrar produto com produto com lote do mesmo

def mostrar_produto_com_lotes():
    bd = sqlconectar()  # Conecta no banco de dados
    cursorbd = bd.cursor()  # Cria um cursor para executar comandos SQL
    print("-" * 40)
    print("   M O S T R A R - P R O D U T O - C O M - L O T E   ")
    print("-" * 40)
    try:
        # Executa uma consulta para pegar todos os produtos e seus lotes
        cursorbd.execute("""
            SELECT produtos.id, produtos.nome, produtos.preco, lotes.numero_lote,
                lotes.quantidade, lotes.data_lote_entrada, lotes.data_lote_validade
            FROM produtos
            LEFT JOIN lotes ON produtos.id = lotes.id_produto
            ORDER BY produtos.id, lotes.numero_lote
        """)
        resultados = cursorbd.fetchall()  # Busca todos os resultados da consulta

        # Se não encontrou nenhum produto, avisa e sai da função
        if not resultados:
            print("Nenhum produto encontrado.")
            return

        produto_atual = None  # Variável para guardar o último produto que mostramos

        # Percorre cada linha dos resultados (cada linha representa um lote de um produto)
        for row in resultados:
            # Descompacta os dados da linha em variáveis
            id_produto, nome_produto, preco, numero_lote, quantidade, entrada, validade = row

            # Se o produto atual for diferente do último que mostramos, mostramos o nome e preço dele
            if id_produto != produto_atual:
                print("\n" + "=" * 40)  # Linha separadora para facilitar a leitura
                print(f"Produto: {nome_produto} (ID: {id_produto}) - Preço: R$ {preco:.2f}")
                produto_atual = id_produto  # Atualiza o produto que estamos mostrando

            # Se existir um número de lote, mostramos os detalhes do lote
            if numero_lote:
                print(f" →  nome do produto:{nome_produto} Lote: {numero_lote} | Quantidade: {quantidade} | Entrada: {entrada.strftime('%d/%m/%Y')} | Validade: {validade.strftime('%d/%m/%Y')}")
            else:
                # Caso não tenha lote cadastrado para esse produto, avisa
                print("  → Nenhum lote cadastrado.")

    except mysql.connector.Error as err:
        # Se der erro ao executar a consulta no banco, mostra a mensagem de erro
        print(f"Erro ao buscar produtos com lotes: {err}")
        
    cursorbd.close()
    bd.close()

def alerta_validade():
    bd = sqlconectar()  # Conecta ao banco de dados (função externa que deve retornar a conexão)
    cursorbd = bd.cursor()  # Cria um cursor para executar comandos SQL no banco
    print("-" * 40)
    print("   A L E R T A - D E - P R O D U T O  ")
    print("-" * 40)
    hoje = date.today()  # Pega a data atual do sistema
    limite_alerta = hoje + timedelta(days=30)  # Define o limite para alerta: 30 dias a partir de hoje

    # Executa uma consulta SQL para buscar lotes cuja data de validade seja até 30 dias à frente (ou já vencidos)
    cursorbd.execute("""
        SELECT produtos.nome, lotes.numero_lote, lotes.quantidade, lotes.data_lote_validade
        FROM lotes
        JOIN produtos ON lotes.id_produto = produtos.id
        WHERE lotes.data_lote_validade <= %s
        ORDER BY lotes.data_lote_validade ASC
    """, (limite_alerta,))  # Passa limite_alerta como parâmetro para prevenir SQL Injection

    lotes_vencidos = cursorbd.fetchall()  # Busca todos os resultados da consulta

    # Se não houver lotes vencidos ou próximos da validade, informa que está tudo ok
    if not lotes_vencidos:
        print("\n✅ Nenhum lote vencido ou próximo da validade (30 dias).")
    else:
        # Se houver, imprime um alerta
        print("\n⚠️ ALERTA DE VALIDADE DOS LOTES ⚠️\n")
        for nome, lote, qtd, validade in lotes_vencidos:
            # Calcula quantos dias faltam para o lote vencer
            dias_para_validade = (validade - hoje).days
            # Define o status dependendo se o lote já venceu ou ainda falta dias
            status = "VENCIDO" if dias_para_validade < 0 else f"vence em {dias_para_validade} dias"
            # Exibe as informações formatadas para o usuário
            print(f"Produto: {nome} | Lote: {lote} | Quantidade: {qtd} | Validade: {validade.strftime('%d/%m/%Y')} ({status})")

    cursorbd.close()  # Fecha o cursor após o uso
    bd.close()  # Fecha a conexão com o banco de dados
'''
while faz repetição até a expressão for verdadeira
caso eu ja deixe ele como verdadeiro ele vai repetir infinitamente até da break

'''
def deletar_lote_ou_produto():
    bd = sqlconectar()  # Conecta ao banco de dados
    cursorbd = bd.cursor()  # Cria um cursor para executar comandos SQL

    # Interface inicial
    print("-" * 40)
    print("     D E L E T A R - L O T E / PRODUTO     ")
    print("-" * 40)

    # Consulta para exibir todos os lotes existentes junto com o nome do produto
    cursorbd.execute("""
        SELECT produtos.id, produtos.nome, lotes.numero_lote, lotes.quantidade, lotes.id
        FROM lotes
        JOIN produtos ON lotes.id_produto = produtos.id
        ORDER BY produtos.nome
    """)
    lotes = cursorbd.fetchall()  # Recupera os resultados

    # Exibe todos os lotes com detalhes
    for lote in lotes:
        print("─" * 40)
        print(f"🆔 ID Produto: {lote[0]}")
        print(f"📦 Produto: {lote[1]}")
        print(f"🔢 Número do Lote: {lote[2]}")
        print(f"📦 Quantidade: {lote[3]}")
        print(f"🆔 ID do Lote: {lote[4]}")
    print("─" * 40)

    # Menu de escolha para o usuário
    print("\nO que você deseja excluir?")
    print("1 - Um lote específico")
    print("2 - Um produto por completo (todos os lotes e o produto)")
    opcao = input("Digite 1 ou 2: ")

    # Opção 1: Excluir um lote específico
    if opcao == "1":
        id_lote = input("Digite o ID do lote que deseja excluir: ")

        # Validação do ID: deve ser número
        if not id_lote.isdigit():
            print("❌ ID inválido. Digite apenas números.")
            return

        # Verifica se o lote existe
        cursorbd.execute("SELECT id FROM lotes WHERE id = %s", (int(id_lote),))
        if cursorbd.fetchone() is None:
            print("❌ Lote não encontrado.")
            return

        # Deleta o lote
        cursorbd.execute("DELETE FROM lotes WHERE id = %s", (int(id_lote),))
        bd.commit()  # Salva as mudanças no banco de dados
        print("\n✅ Lote excluído com sucesso!")

    # Opção 2: Excluir um produto inteiro e seus lotes
    elif opcao == "2":
        id_produto = input("Digite o ID do produto que deseja excluir por completo: ")

        # Validação do ID: deve ser número
        if not id_produto.isdigit():
            print("❌ ID inválido. Digite apenas números.")
            return

        # Verifica se o produto existe
        cursorbd.execute("SELECT id FROM produtos WHERE id = %s", (int(id_produto),))
        if cursorbd.fetchone() is None:
            print("❌ Produto não encontrado.")
            return

        # Deleta todos os lotes relacionados a esse produto
        cursorbd.execute("DELETE FROM lotes WHERE id_produto = %s", (int(id_produto),))
        # Deleta do estoque (caso exista entrada para esse produto)
        cursorbd.execute("DELETE FROM estoque WHERE id_produto = %s", (int(id_produto),))
        # Deleta o próprio produto
        cursorbd.execute("DELETE FROM produtos WHERE id = %s", (int(id_produto),))

        bd.commit()  # Salva todas as mudanças no banco de dados
        print("\n✅ Produto e todos os seus lotes excluídos com sucesso!")

    else:
        # Caso o usuário digite uma opção inválida
        print("❌ Opção inválida.")

    # Encerra a conexão com o banco de dados
    cursorbd.close()
    bd.close()
while True:
 
    print("\n\n\n|-------------------------Menu--------------------------|")
    print("\n1 - Cadastrar um novo produto")
    print("2 - Alterar produto cadastrado")
    print("3 - Excluir produto")
    print("4 - Mostrar produtos registrados no sistema")
    print("5 - Mostrar lotes dos produtos")
    print("6 - Emitir um alerta(produto com estoque baixo)")
    print("7 - Emitir alerta de validade")
    print("8 - Sair")
    print("\n|--------------------------------------------------------|")

    opcao = input("\nEscolha uma das opções acima: ")

    if opcao == "1":
        cadastrar_produto()
    elif opcao == "2":
        alterar_produto()
        print('\n\n Produto alterado com sucesso! ✅\n\n')
    elif opcao == "3":
        deletar_lote_ou_produto()
    elif opcao == "4":
        print("\n\nVerificando🟢🟢🟢\n\n")
        mostrar_produtos_registrados()
    elif opcao == "5":
        print("\n\nVerificando🟢🟢🟢\n\n")
        mostrar_produto_com_lotes()
    elif opcao == "6":
        print("\n\nVerificando🟢🟢🟢\n\n")
        verificar_estoque()
    elif opcao == "7":
        alerta_validade()
    elif opcao == '8':
        print('saindo....')
        break # quebra a repetição do while
        
    else:
        print('Opção inválida!, por favor digite a correta')