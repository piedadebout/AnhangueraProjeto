# models.py

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
        self.itens = {}

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
