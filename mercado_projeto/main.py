from persistencia import carregar_dados, salvar_dados
from interface import menu_principal

def main():
    print("============== Mercado Projeto ==============")
    print("Bem-vindo ao sistema de mercado!")
    print("============================================")

    produtos, carrinho, admins = carregar_dados()

    try:
        menu_principal(produtos, carrinho, admins)
    finally:
        salvar_dados(produtos, carrinho, admins)
        print("Dados salvos com sucesso. Até logo!")

if __name__ == "__main__":
    main()
