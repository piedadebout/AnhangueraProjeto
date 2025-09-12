"""
Sistema de Mercado em Python (versão final aprimorada)
------------------------------------------------------
- Carrinho consolidado com mini-tabela
- Validação de entrada para números e CPF
- Persistência em JSON (produtos, carrinho, administradores)
- Estrutura orientada a objetos (Produto e Carrinho)
- Login de administrador com CPF + senha
- Proteção do último administrador
- Menus visualmente melhorados
"""

import json
import os
import re

# =========================
# Funções utilitárias
# =========================
def input_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número inteiro válido.")

def input_float(msg: str) -> float:
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("Digite um número decimal válido.")

def validar_cpf(cpf: str) -> bool:
    """Valida se o CPF contém exatamente 11 números"""
    cpf = re.sub(r'\D', '', cpf)
    return len(cpf) == 11

# =========================
# Classes principais
# =========================
class Produto:
    def __init__(self, codigo: int, nome: str, preco: float, estoque: int):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def to_dict(self):
        return {"codigo": self.codigo, "nome": self.nome, "preco": self.preco, "estoque": self.estoque}

    @staticmethod
    def from_dict(data):
        return Produto(data["codigo"], data["nome"], data["preco"], data["estoque"])

class Carrinho:
    def __init__(self):
        self.itens = {}  # {codigo: {"produto": Produto, "quantidade": int}}

    def adicionar(self, produto: Produto, quantidade: int):
        if quantidade <= 0:
            print("A quantidade deve ser maior que 0.")
            return
        if produto.estoque < quantidade:
            print(f"Estoque insuficiente! Disponível: {produto.estoque}")
            return
        produto.estoque -= quantidade
        if produto.codigo in self.itens:
            self.itens[produto.codigo]["quantidade"] += quantidade
        else:
            self.itens[produto.codigo] = {"produto": produto, "quantidade": quantidade}
        print(f"{quantidade}x {produto.nome} adicionado ao carrinho!")

    def remover(self, codigo: int):
        if codigo in self.itens:
            item = self.itens.pop(codigo)
            produto = item["produto"]
            quantidade = item["quantidade"]
            produto.estoque += quantidade
            print(f"{quantidade}x {produto.nome} removido do carrinho.")
        else:
            print("Produto não encontrado no carrinho.")

    def ver(self):
        if not self.itens:
            print("\nCarrinho vazio!")
            return

        print("\n=== Seu Carrinho ===")
        print(f"{'Produto':<20} | {'Qtd':<4} | {'Preço Unit.':<12} | {'Subtotal':<10}")
        print("-" * 55)
        total = 0
        for item in self.itens.values():
            produto = item["produto"]
            quantidade = item["quantidade"]
            subtotal = produto.preco * quantidade
            print(f"{produto.nome:<20} | {quantidade:<4} | R$ {produto.preco:<10.2f} | R$ {subtotal:<8.2f}")
            total += subtotal
        print("-" * 55)
        print(f"{'TOTAL':<20} | {'':<4} | {'':<12} | R$ {total:<8.2f}")
        print("-" * 55)

    def finalizar(self):
        if not self.itens:
            print("\nCarrinho está vazio!")
            return
        self.ver()
        print("\nCompra finalizada. Obrigado pela preferência!")
        self.itens.clear()

    def to_dict(self):
        return {codigo: {"quantidade": item["quantidade"]} for codigo, item in self.itens.items()}

    def from_dict(self, data, produtos):
        for codigo, info in data.items():
            codigo = int(codigo)
            if codigo in produtos:
                self.itens[codigo] = {"produto": produtos[codigo], "quantidade": info["quantidade"]}

# =========================
# Persistência de dados
# =========================
ARQUIVO_DADOS = "mercado.json"

def salvar_dados(produtos, carrinho, admins):
    data = {
        "produtos": [p.to_dict() for p in produtos.values()],
        "carrinho": carrinho.to_dict(),
        "admins": admins
    }
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        admins = [{"cpf": "12345678901", "senha": "1234"}]
        return {}, Carrinho(), admins
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        data = json.load(f)
    produtos = {p["codigo"]: Produto.from_dict(p) for p in data.get("produtos", [])}
    carrinho = Carrinho()
    carrinho.from_dict(data.get("carrinho", {}), produtos)
    admins = data.get("admins", [{"cpf": "12345678901", "senha": "1234"}])
    return produtos, carrinho, admins

# =========================
# Interface
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
# Administradores
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

# =========================
# Menus
# =========================
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
            salvar_dados(produtos, carrinho, admins)
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida, tente novamente.")

# =========================
# Execução
# =========================
if __name__ == "__main__":
    print("============== Mercado Projeto ==============")
    print("Bem-vindo ao sistema de mercado!")
    print("============================================")

    produtos, carrinho, admins = carregar_dados()
    menu_principal(produtos, carrinho, admins)
