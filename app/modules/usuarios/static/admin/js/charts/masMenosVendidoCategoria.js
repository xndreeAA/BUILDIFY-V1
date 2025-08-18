const fetchData = async (params) => {
  const menos_value = params.menos_vendido_categoria ?? '';
  const mas_value = params.mas_vendido_categoria ?? '';
  
  const url = `/api/v1/pedidos/mas-menos?menos_vendido_categoria=${menos_value}&mas_vendido_categoria=${mas_value}`;

  const resp = await fetch(url);
  const json = await resp.json();

  if (params.mas_vendido_categoria !== undefined) {
    return json.data?.mas_vendido_categoria || null;
  }
  if (params.menos_vendido_categoria !== undefined) {
    return json.data?.menos_vendido_categoria || null;
  }
  return null;
};

async function cargarCategorias(contenedor) {
  const res = await fetch('/api/v1/categorias');
  const json = await res.json();
  const categorias = json.data;

  contenedor.innerHTML = `<option value="default">Seleccione una categoría</option>`;
  categorias.forEach(cat => {
    const option = document.createElement('option');
    option.value = cat.nombre;
    const nombre = cat.nombre[0].toUpperCase() + cat.nombre.slice(1);
    option.textContent = nombre;
    contenedor.appendChild(option);
  });
}

const crearCajaProducto = (producto) => {
  if (!producto) {
    const contenedor = document.createElement('div');
    contenedor.classList.add('producto-vacio');
    contenedor.innerHTML = `
      <div class="producto-vacio-icono">📦</div>
      <div class="producto-vacio-texto">
        <h3>Aún no has seleccionado una categoría</h3>
        <p>Elige una para ver los productos más y menos vendidos.</p>
      </div>
    `;
    return contenedor;
  }

  const contenedor = document.createElement('div');
  contenedor.classList.add('producto-info');

  const nombre = document.createElement('h5');
  nombre.classList.add('producto-nombre');
  nombre.textContent = producto.nombre;

  const lista = document.createElement('ul');
  lista.classList.add('producto-info-lista');


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

    selectMasVendido.value = 'default';
    selectMenosVendido.value = 'default';

    const productoMas = await fetchData({ mas_vendido_categoria: '' });
    mas_vendido.innerHTML = '';
    mas_vendido.appendChild(crearCajaProducto(productoMas));

    const productoMenos = await fetchData({ menos_vendido_categoria: '' });
    menos_vendido.innerHTML = '';
    menos_vendido.appendChild(crearCajaProducto(productoMenos));

    selectMasVendido.addEventListener('change', async () => {
      if (selectMasVendido.value === 'default') {
        const producto = await fetchData({ mas_vendido_categoria: '' });
        mas_vendido.innerHTML = '';
        mas_vendido.appendChild(crearCajaProducto(producto));
        return;
      }
      const producto = await fetchData({ mas_vendido_categoria: selectMasVendido.value });
      mas_vendido.innerHTML = '';
      mas_vendido.appendChild(crearCajaProducto(producto));
    });

    selectMenosVendido.addEventListener('change', async () => {
      if (selectMenosVendido.value === 'default') {
        const producto = await fetchData({ menos_vendido_categoria: '' });
        menos_vendido.innerHTML = '';
        menos_vendido.appendChild(crearCajaProducto(producto));
        return;
      }
      const producto = await fetchData({ menos_vendido_categoria: selectMenosVendido.value });
      menos_vendido.innerHTML = '';
      menos_vendido.appendChild(crearCajaProducto(producto));
    });

  } catch (error) {
    console.error("Error al cargar categorías o renderizar:", error);
  }
};

export default renderMasMenosVendidoCategoria;
