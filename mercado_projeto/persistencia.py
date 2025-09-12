import json
import os
from models import Produto, Carrinho

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
