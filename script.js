const produtos = [
  { nome: "Pizza Margherita", preco: 30 },
  { nome: "Pizza Calabresa", preco: 35 },
  { nome: "Pizza Quatro Queijos", preco: 38 },
  { nome: "Pizza Portuguesa", preco: 40 }
];

const carrinho = [];

function criarCardapio() {
  const menu = document.getElementById("menu");
  produtos.forEach((item, index) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${item.nome}</h3>
      <p>R$ ${item.preco.toFixed(2)}</p>
      <button onclick="adicionarAoCarrinho(${index})">Adicionar</button>
    `;
    menu.appendChild(card);
  });
}

function adicionarAoCarrinho(index) {
  carrinho.push(produtos[index]);
  atualizarCarrinho();
}

function atualizarCarrinho() {
  const lista = document.getElementById("carrinho");
  lista.innerHTML = "";
  carrinho.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.nome} - R$ ${item.preco.toFixed(2)}`;
    lista.appendChild(li);
  });
}

function enviarPedido() {
  const pedidoTexto = carrinho.map(item => item.nome).join(", ");
  alert(`Pedido enviado: ${pedidoTexto}`);
  // Aqui você pode integrar com o backend ou WhatsApp
}

criarCardapio();