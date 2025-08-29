const pedidosContainer = document.getElementById("mis_pedidos_container")

const res = await fetch(`/api/v1/pedidos/usuario/${id_usuario}`);
const data = await res.json();

console.log(data);
