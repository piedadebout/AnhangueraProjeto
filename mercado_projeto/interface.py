from utils import input_int, input_float, validar_cpf
from models import Produto, Carrinho

# =========================
# Interface de Produtos
# =========================

def mostrar_produtos(produtos):
    if not produtos:
        print("\nNenhum produto cadastrado.")
        return
    print("\n=== Produtos Disponíveis ===")
    print(f"{'Código':<6} | {'Produto':<20} | {'Preço':<10} | {'Estoque':<6}")
    print("-" * 50)
    for p in produtos.values():
        print(f"{p.codigo:<6} | {p.nome:<20} | R$ {p.preco:<9.2f} | {p.estoque:<6}")
    print("-" * 50)

def cadastrar_produto(produtos):
    codigo = max(produtos.keys()) + 1 if produtos else 1
    nome = input("Digite o nome do produto: ")
    preco = input_float("Digite o preço do produto: ")
    estoque = input_int("Digite a quantidade em estoque: ")
    produtos[codigo] = Produto(codigo, nome, preco, estoque)
    print(f"Produto {nome} cadastrado com sucesso! (Código: {codigo})")

def editar_produto(produtos):
    mostrar_produtos(produtos)
    codigo = input_int("Digite o código do produto que deseja editar: ")
    if codigo in produtos:
        produto = produtos[codigo]
        nome = input(f"Novo nome ({produto.nome}): ") or produto.nome
        preco = input(f"Novo preço ({produto.preco}): ") or produto.preco
        estoque = input(f"Novo estoque ({produto.estoque}): ") or produto.estoque
        try:
            preco = float(preco)
            estoque = int(estoque)
        except ValueError:
            print("Valores inválidos.")
            return
        produto.nome = nome
        produto.preco = preco
        produto.estoque = estoque
        print("Produto atualizado com sucesso!")
    else:
        print("Código inválido.")

def remover_produto(produtos):
    mostrar_produtos(produtos)
    codigo = input_int("Digite o código do produto que deseja remover: ")
    if codigo in produtos:
        nome = produtos[codigo].nome
        del produtos[codigo]
        print(f"Produto {nome} removido com sucesso!")
    else:
        print("Código inválido.")

# =========================
# Interface de Admin
# =========================

def listar_admins(admins):
    if not admins:
        print("\nNenhum administrador cadastrado.")
        return
    print("\n=== Administradores Cadastrados ===")
    for i, adm in enumerate(admins, 1):
        print(f"{i}. CPF: {adm['cpf']}")
    print("-" * 40)

def cadastrar_admin(admins):
    cpf = input("Digite o CPF do novo Admin (somente números): ")
    if not validar_cpf(cpf):
        print("CPF inválido!")
        return
    for adm in admins:
        if adm["cpf"] == cpf:
            print("Admin já cadastrado!")
            return
    senha = input("Digite a senha do novo Admin: ")
    admins.append({"cpf": cpf, "senha": senha})
    print("Admin cadastrado com sucesso!")

def remover_admin(admins):
    if len(admins) == 1:
        print("Não é possível remover o último administrador!")
        return
    listar_admins(admins)
    cpf = input("Digite o CPF do Admin que deseja remover: ")
    for adm in admins:
        if adm["cpf"] == cpf:
            admins.remove(adm)
            print("Admin removido com sucesso!")
            return
    print("Admin não encontrado!")

def login_admin(admins):
    cpf = input("Digite o CPF do Admin (somente números): ")
    if not validar_cpf(cpf):
        print("CPF inválido! Deve conter 11 números.")
        return False
    senha = input("Digite a senha do Admin: ")
    for adm in admins:
        if adm["cpf"] == cpf and adm["senha"] == senha:
            return True
    print("CPF ou senha incorretos!")
    return False

def menu_admin(produtos, admins):
    while True:
        print("\n" + "=" * 40)
        print("         🔧 MENU ADMINISTRADOR        ")
        print("=" * 40)
        print("1️⃣  - Cadastrar produto")
        print("2️⃣  - Editar produto")
        print("3️⃣  - Remover produto")
        print("4️⃣  - Listar produtos")
        print("5️⃣  - Listar administradores")
        print("6️⃣  - Cadastrar administrador")
        print("7️⃣  - Remover administrador")
        print("8️⃣  - Sair do modo Admin")
        print("=" * 40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_produto(produtos)
        elif opcao == "2":
            editar_produto(produtos)
        elif opcao == "3":
            remover_produto(produtos)
        elif opcao == "4":
            mostrar_produtos(produtos)
        elif opcao == "5":
            listar_admins(admins)
        elif opcao == "6":
            cadastrar_admin(admins)
        elif opcao == "7":
            remover_admin(admins)
        elif opcao == "8":
            print("Saindo do modo Admin...")
            break
        else:
            print("Opção inválida.")

# =========================
# Menu Principal (ponto de entrada do sistema)
# =========================

def menu_principal(produtos, carrinho, admins):
    while True:
        print("\n" + "=" * 40)
        print("           🛒 MENU PRINCIPAL           ")
        print("=" * 40)
        print("1️⃣  - Mostrar produtos")
        print("2️⃣  - Adicionar produto ao carrinho")
        print("3️⃣  - Ver carrinho")
        print("4️⃣  - Remover item do carrinho")
        print("5️⃣  - Finalizar compra")
        print("6️⃣  - Acessar modo Admin")
        print("7️⃣  - Sair")
        print("=" * 40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            mostrar_produtos(produtos)
        elif opcao == "2":
            mostrar_produtos(produtos)
            codigo = input_int("Digite o código do produto: ")
            quantidade = input_int("Digite a quantidade desejada: ")
            if codigo in produtos:
                carrinho.adicionar(produtos[codigo], quantidade)
            else:
                print("Código inválido.")
        elif opcao == "3":
            carrinho.ver()
        elif opcao == "4":
            carrinho.ver()
            codigo = input_int("Digite o código do produto para remover: ")
            carrinho.remover(codigo)
        elif opcao == "5":
            carrinho.finalizar()
        elif opcao == "6":
            if login_admin(admins):
                menu_admin(produtos, admins)
        elif opcao == "7":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida, tente novamente.")
