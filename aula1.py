"""
Sistema de Mercado em Python
----------------------------
Este programa simula um sistema de mercado com dois modos de operação:

1. Cliente:
   - Visualizar produtos
   - Adicionar itens ao carrinho
   - Remover itens do carrinho
   - Ver carrinho e total
   - Finalizar compra

2. Administrador:
   - Cadastrar novos produtos
   - Editar produtos existentes
   - Remover produtos
   - Listar produtos

Recursos implementados:
- Controle de estoque por produto
- Carrinho de compras associado ao cliente
- Modo Admin protegido por senha simples
"""

# =========================
# Dados iniciais do sistema
# =========================

# Produtos disponíveis (código → nome, preço e estoque)
produtos = {
    1: {"nome": "Arroz", "preco": 20.00, "estoque": 10},
    2: {"nome": "Feijão", "preco": 8.50, "estoque": 8},
    3: {"nome": "Macarrão", "preco": 5.00, "estoque": 15},
    4: {"nome": "Óleo", "preco": 7.00, "estoque": 5},
    5: {"nome": "Açúcar", "preco": 4.50, "estoque": 12}
}

# Carrinho do cliente (lista de dicionários)
carrinho = []

# Senha do administrador
senha_admin = "1234"


# =========================
# Funções do modo Cliente
# =========================

def mostrar_produtos():
    """
    Exibe a lista de produtos disponíveis com código, nome, preço e estoque.
    """
    print("\nProdutos disponíveis:")
    for codigo, item in produtos.items():
        print(f"{codigo} - {item['nome']} (R$ {item['preco']:.2f}) | Estoque: {item['estoque']}")


def adicionar_carrinho(codigo: int, quantidade: int):
    """
    Adiciona um produto ao carrinho de compras, respeitando o estoque disponível.

    Parâmetros:
        codigo (int): código do produto no dicionário 'produtos'
        quantidade (int): quantidade desejada
    """
    if codigo in produtos:
        produto = produtos[codigo]
        if quantidade <= 0:
            print("A quantidade deve ser maior que 0.")
        elif produto["estoque"] >= quantidade:
            carrinho.append({"codigo": codigo, "nome": produto["nome"], "preco": produto["preco"], "quantidade": quantidade})
            produto["estoque"] -= quantidade
            print(f"{quantidade}x {produto['nome']} foi adicionado ao carrinho!")
        else:
            print(f"Estoque insuficiente! Disponível: {produto['estoque']}")
    else:
        print("Código inválido.")


def ver_carrinho():
    """
    Exibe os itens no carrinho com quantidades e valor total.
    """
    if not carrinho:
        print("\nCarrinho vazio!")
        return
    
    print("\nSeu carrinho:")
    total = 0
    for i, item in enumerate(carrinho, 1):
        subtotal = item['preco'] * item['quantidade']
        print(f"{i}. {item['nome']} x{item['quantidade']} - R$ {subtotal:.2f}")
        total += subtotal
    print(f"Total: R$ {total:.2f}")


def remover_carrinho(indice: int):
    """
    Remove um item do carrinho e devolve sua quantidade ao estoque.

    Parâmetros:
        indice (int): posição do item no carrinho (base 0)
    """
    if 0 <= indice < len(carrinho):
        item = carrinho.pop(indice)
        produtos[item["codigo"]]["estoque"] += item["quantidade"]
        print(f"{item['quantidade']}x {item['nome']} foi removido do carrinho e devolvido ao estoque.")
    else:
        print("Índice inválido!")


def finalizar_compra():
    """
    Exibe o resumo da compra e limpa o carrinho.
    """
    if not carrinho:
        print("\nCarrinho está vazio!")
        return
    
    ver_carrinho()
    print("\nCompra finalizada. Obrigado pela preferência!")
    carrinho.clear()


# =========================
# Funções do modo Admin
# =========================

def cadastrar_produto():
    """
    Cadastra um novo produto no sistema.
    """
    try:
        codigo = max(produtos.keys()) + 1 if produtos else 1
        nome = input("Digite o nome do produto: ")
        preco = float(input("Digite o preço do produto: "))
        estoque = int(input("Digite a quantidade em estoque: "))
        produtos[codigo] = {"nome": nome, "preco": preco, "estoque": estoque}
        print(f"Produto {nome} cadastrado com sucesso! (Código: {codigo})")
    except ValueError:
        print("Erro: valores inválidos para preço ou estoque.")


def editar_produto():
    """
    Edita as informações de um produto existente.
    """
    mostrar_produtos()
    try:
        codigo = int(input("Digite o código do produto que deseja editar: "))
        if codigo in produtos:
            nome = input(f"Novo nome ({produtos[codigo]['nome']}): ") or produtos[codigo]['nome']
            preco = input(f"Novo preço ({produtos[codigo]['preco']}): ")
            estoque = input(f"Novo estoque ({produtos[codigo]['estoque']}): ")

            preco = float(preco) if preco else produtos[codigo]['preco']
            estoque = int(estoque) if estoque else produtos[codigo]['estoque']

            produtos[codigo] = {"nome": nome, "preco": preco, "estoque": estoque}
            print("Produto atualizado com sucesso!")
        else:
            print("Código inválido.")
    except ValueError:
        print("Erro: valores inválidos.")


def remover_produto():
    """
    Remove um produto do sistema permanentemente.
    """
    mostrar_produtos()
    try:
        codigo = int(input("Digite o código do produto que deseja remover: "))
        if codigo in produtos:
            nome = produtos[codigo]['nome']
            del produtos[codigo]
            print(f"Produto {nome} removido com sucesso!")
        else:
            print("Código inválido.")
    except ValueError:
        print("Erro: digite apenas números.")


def menu_admin():
    """
    Exibe o menu do administrador com as opções de gerenciamento de produtos.
    """
    while True:
        print("\n====== MENU ADMIN ======")
        print("1 - Cadastrar produto")
        print("2 - Editar produto")
        print("3 - Remover produto")
        print("4 - Listar produtos")
        print("5 - Sair do modo Admin")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            editar_produto()
        elif opcao == "3":
            remover_produto()
        elif opcao == "4":
            mostrar_produtos()
        elif opcao == "5":
            print("Saindo do modo Admin...")
            break
        else:
            print("Opção inválida.")


# =========================
# Menu principal do sistema
# =========================

def menu_principal():
    """
    Controla o fluxo principal do programa, exibindo opções para o cliente
    e acesso ao modo administrador.
    """
    while True:
        print("\n====== MENU PRINCIPAL ======")
        print("1 - Mostrar produtos")
        print("2 - Adicionar produto ao carrinho")
        print("3 - Ver carrinho")
        print("4 - Remover item do carrinho")
        print("5 - Finalizar compra")
        print("6 - Acessar modo Admin")
        print("7 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            mostrar_produtos()
        elif opcao == "2":
            mostrar_produtos()
            try:
                codigo = int(input("Digite o código do produto: "))
                quantidade = int(input("Digite a quantidade desejada: "))
                adicionar_carrinho(codigo, quantidade)
            except ValueError:
                print("Digite apenas números válidos.")
        elif opcao == "3":
            ver_carrinho()
        elif opcao == "4":
            ver_carrinho()
            try:
                indice = int(input("Digite o número do item para remover: ")) - 1
                remover_carrinho(indice)
            except ValueError:
                print("Digite apenas números válidos.")
        elif opcao == "5":
            finalizar_compra()
        elif opcao == "6":
            senha = input("Digite a senha do Admin: ")
            if senha == senha_admin:
                menu_admin()
            else:
                print("Senha incorreta!")
        elif opcao == "7":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida, tente novamente.")


# =========================
# Execução do programa
# =========================
if __name__ == "__main__":
    print("============== Mercado Projeto ==============")
    print("Bem-vindo ao sistema de mercado!")
    print("============================================")
    menu_principal()
