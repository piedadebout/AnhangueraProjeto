
// Sistema de Mercado em Python
// ----------------------------
// Este programa simula um sistema de mercado com dois modos de operação:

// 1. Cliente:
//    - Visualizar produtos
//    - Adicionar itens ao carrinho
//    - Remover itens do carrinho
//    - Ver carrinho e total
//    - Finalizar compra

// 2. Administrador:
//    - Cadastrar novos produtos
//    - Editar produtos existentes
//    - Remover produtos
//    - Listar produtos

// Recursos implementados:
// - Controle de estoque por produto
// - Carrinho de compras associado ao cliente
// - Modo Admin protegido por senha simples


// =========================
// Dados iniciais do sistema
// =========================

// Produtos disponíveis (código → nome, preço e estoque)
let produtos = [
    {"nome": "Arroz", "preco": 20.00, "estoque": 10},
    {"nome": "Feijão", "preco": 8.50, "estoque": 8},
    {"nome": "Macarrão", "preco": 5.00, "estoque": 15},
    {"nome": "Óleo", "preco": 7.00, "estoque": 5},
    {"nome": "Açúcar", "preco": 4.50, "estoque": 12}
]

// Carrinho do cliente (lista de dicionários)
let carrinho = []

// Senha do administrador
let senhaAdmin = "1234"

// =========================
// Funções do modo Cliente
// =========================

function mostrarProdutos(){
    // Exibe a lista de produtos disponíveis com código, nome, preço e estoque.
    console.log("\nProdutos disponíveis:")
    for (let i=0; i < produtos.length; i++) {
        console.log(`${i+1} - ${produtos[i]["nome"]} (R$ ${produtos[i]["preco"]}) | Estoque: ${produtos[i]["estoque"]}`);
    }
}

mostrarProdutos()


