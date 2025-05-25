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