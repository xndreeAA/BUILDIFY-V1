const fetchData = async () => {
  const data = await fetch('/api/pedidos/mas-menos?menos_vendido=true&mas_vendido=true');
  const res = await data.json();
  return res.data;
};

const renderMasMenosVendido = async () => {
  const mas_vendido = document.getElementById('mas-vendido');
  const menos_vendido = document.getElementById('menos-vendido');

  if (!mas_vendido || !menos_vendido) {
    return console.error("Elemento no encontrado en el DOM");
  }

  try {
    const data = await fetchData();

    const crearCajaProducto = (producto) => {
      const contenedor = document.createElement('div');
      contenedor.classList.add('producto-info');

      const nombre = document.createElement('h5');
      nombre.classList.add('producto-nombre');
      nombre.textContent = producto.nombre;

      const lista = document.createElement('ul');

      const elementos = [
        { label: 'Marca', valor: producto.marca },
        { label: 'Categoría', valor: producto.categoria },
        { label: 'Precio unitario', valor: `$${Number(producto.precio).toLocaleString()}` },
        { label: 'Unidades vendidas', valor: producto.unidades_vendidas },
        { label: 'Ganancias totales', valor: `$${Number(producto.ganancias).toLocaleString()}` },
      ];

      elementos.forEach(({ label, valor }) => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${label}:</strong> ${valor}`;
        lista.appendChild(li);
      });

      contenedor.appendChild(nombre);
      contenedor.appendChild(lista);

      return contenedor;
    };

    mas_vendido.innerHTML = '';
    menos_vendido.innerHTML = '';

    mas_vendido.appendChild(crearCajaProducto(data.mas_vendido));

    menos_vendido.appendChild(crearCajaProducto(data.menos_vendido));

  } catch (error) {
    console.error("Error al obtener o renderizar datos:", error);
  }
};

export default renderMasMenosVendido