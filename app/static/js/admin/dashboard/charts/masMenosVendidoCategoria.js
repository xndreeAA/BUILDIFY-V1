const fetchData = async (params) => {
  const menos_value = params.menos_vendido_categoria ?? '';
  const mas_value = params.mas_vendido_categoria ?? '';
  
  const url = `/api/pedidos/mas-menos?menos_vendido_categoria=${menos_value}&mas_vendido_categoria=${mas_value}`;

  const resp = await fetch(url);
  const json = await resp.json();

  if (params.mas_vendido_categoria) {
    return json.data?.mas_vendido_categoria || null;
  }
  if (params.menos_vendido_categoria) {
    return json.data?.menos_vendido_categoria || null;
  }
  return null;
};

async function cargarCategorias(contenedor) {
  const res = await fetch('/api/categorias');
  const json = await res.json();
  const categorias = json.data;

  contenedor.innerHTML = `<option value="">Seleccione una categoría</option>`;
  categorias.forEach(cat => {
    const option = document.createElement('option');
    option.value = cat.nombre;
    option.textContent = cat.nombre;
    contenedor.appendChild(option);
  });
}

const crearCajaProducto = (producto) => {
  if (!producto) {
    const contenedor = document.createElement('div');
    contenedor.classList.add('producto-info');
    contenedor.textContent = "Sin datos disponibles";
    return contenedor;
  }

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

const renderMasMenosVendidoCategoria = async () => {
  const mas_vendido = document.getElementById('mas-vendido-por-categoria');
  const menos_vendido = document.getElementById('menos-vendido-por-categoria');
  const selectMasVendido = document.getElementById('select-mas-vendido-por-categoria');
  const selectMenosVendido = document.getElementById('select-menos-vendido-por-categoria');

  try {
    if (!mas_vendido || !menos_vendido) {
      return console.error("Elemento de contenedor no encontrado en el DOM");
    }
    if (!selectMasVendido || !selectMenosVendido) {
      return console.error("Elemento select no encontrado en el DOM");
    }

    await cargarCategorias(selectMasVendido);
    await cargarCategorias(selectMenosVendido);

    selectMasVendido.addEventListener('change', async () => {
      const producto = await fetchData({ mas_vendido_categoria: selectMasVendido.value });
      mas_vendido.innerHTML = '';
      mas_vendido.appendChild(crearCajaProducto(producto));
    });

    selectMenosVendido.addEventListener('change', async () => {
      const producto = await fetchData({ menos_vendido_categoria: selectMenosVendido.value });
      menos_vendido.innerHTML = '';
      menos_vendido.appendChild(crearCajaProducto(producto));
    });

  } catch (error) {
    console.error("Error al cargar categorías o renderizar:", error);
  }
};

export default renderMasMenosVendidoCategoria;
