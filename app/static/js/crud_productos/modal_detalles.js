const modalDetalles = document.getElementById('modal-detalles');
const modalTitle = document.getElementById('modal-detalles-title');
const closeModalBtn = document.getElementById('close-modal-btn');
const detallesContainer = document.getElementById('detalles-container');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


let productoGlobal = null;

const closeModal = () => modalDetalles.style.display = 'none';

closeModalBtn?.addEventListener('click', e => {
  e.preventDefault();
  closeModal();
});

window.addEventListener('click', e => {
  if (e.target === modalDetalles) closeModal();
});

const fetchMarcas = async () => {
  const url = '/api/marcas';
  const res = await fetch(url, { credentials:'include' });
  const json = await res.json();
  
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return json.data;
}

const fetchData = async ({ id_producto }) => {
  const url = `/api/detalles/${id_producto}`
  const res = await fetch(url, { credentials:'include' });
  const json = await res.json();
  
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return json.data;
};

const viewDetailsProduct = async ({ id_producto }) => {
  const producto = await fetchData({ id_producto });
  const marcas = await fetchMarcas();

  productoGlobal = producto
  modalDetalles.style.display = 'flex';
  modalTitle.textContent = `Producto #${producto.id_producto}`;

  let html = `
    <label class="label_field">Nombre:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="text"
               name="nombre" value="${producto.nombre}">
        <button type="button" class="btn-edit">✏️</button>
      </div>
    </label>
    <label class="label_field">Precio:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="number"
               name="precio" value="${producto.precio}">
        <button type="button" class="btn-edit">✏️</button>
      </div>
    </label>
    <label class="label_field">Stock:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="number"
               name="stock" value="${producto.stock}">
        <button type="button" class="btn-edit">✏️</button>
      </div>
    </label>
  `;
  

  const optionsHtml = marcas.map(marca => `
    <option 
      ${marca.id_marca === producto.marca.id_marca ? 'selected' : ''} 
      value="${marca.id_marca}">
      ${marca.nombre}
    </option>
  `).join('');

  html += `
    <label class="label_field">Marca:
      <div class="input-container select">
        <select data-static="true" class="input_field" name="id_marca" disabled>
          ${optionsHtml}
        </select>
        <button type="button" class="btn-edit select">✏️</button>
      </div>
    </label>
  `;

  producto.imagenes.forEach((e, i) => {
    const ruta = e.ruta;

    html += `
      <label class="label_field">Imagen numero: ${ i + 1 }:
        <div class="input-container">
          <input disabled data-static="true" class="input_field" type="text"
                 name="${ruta}" value="${ruta}">
          <button type="button" class="btn-edit">✏️</button>
        </div>
      </label>
    `;
  });

  for (const key in producto.detalles) {
    const val = producto.detalles[key];
    let type, extra = '';
    if (typeof val === 'boolean') {
      type = 'input';
      extra = val ? ' checked' : '';
    } else if (!isNaN(val) && val !== '') {
      type = 'number';
    } else {
      type = 'text';
    }

    html += `
      <label class="label_field">${key.charAt(0).toUpperCase()+key.slice(1)}:
        <div class="input-container">
          <input disabled class="input_field"
                 type="${type}"
                 name="${key}"
                 value="${type !== 'checkbox' ? val : ''}"
                 ${extra}>
          <button type="button" class="btn-edit">✏️</button>
        </div>
      </label>
    `;
  }

  html += `<button type="button" id="submit-btn">Guardar cambios</button>`;
  detallesContainer.innerHTML = html;
};

detallesContainer.addEventListener('click', e => {
  e.preventDefault();

  if (e.target.classList.contains('btn-edit' && 'select')) {
    const inp = e.target.closest('.input-container').querySelector('select');
    inp.disabled = !inp.disabled;
    e.target.textContent = inp.disabled ? '✏️' : '✔️';
    return;
  }

  if (e.target.classList.contains('btn-edit')) {
    const inp = e.target.closest('.input-container').querySelector('input');
    inp.disabled = !inp.disabled;
    e.target.textContent = inp.disabled ? '✏️' : '✔️';
    return;
  }

  if (e.target.id === 'submit-btn') {
    e.preventDefault();

    const formInputs = document.querySelectorAll('.input_field');
    const data = {
      id_marca: productoGlobal.marca.id_marca,
      precio: productoGlobal.precio,
      stock: productoGlobal.stock,
      imagen: productoGlobal.imagen,
      detalles: {}
    };

    formInputs.forEach(input => {
      const name = input.name;
      let val;

      if (input.type === 'checkbox') {
        val = input.checked;
      } else if (input.type === 'number') {
        val = Number(input.value);
      } else {
        val = input.value;
      }

      if (input.dataset.static) {
        data[name] = val;
      } else {
        data.detalles[name] = val;
      }
    });

    fetch(`/api/detalles/${productoGlobal.id_producto}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      credentials: 'include',
      body: JSON.stringify(data)
    })
    .then(res => {
      if (!res.ok) throw new Error(`Error HTTP ${res.status}`);
      return res.json();
    })
    .then(json => {
      alert('Producto actualizado correctamente');
      closeModal();
    })
    .catch(err => {
      console.error('Error al actualizar producto:', err);
      alert('Hubo un error al guardar los cambios');
    });
  }
});
