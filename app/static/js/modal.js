// ========================================================
// VARIABLES DE DOM
// ========================================================
const modalDetalles     = document.querySelector('.modal-detalles');
const modalTitle        = document.getElementById('modal-title');
const closeModalBtn     = document.getElementById('close-modal-btn');
const detallesContainer = document.querySelector('.detalles-container');

let productoGlobal = null;

// ========================================================
// CERRAR MODAL
// ========================================================
const closeModal = () => modalDetalles.style.display = 'none';

closeModalBtn?.addEventListener('click', e => {
  e.preventDefault();
  closeModal();
});

window.addEventListener('click', e => {
  if (e.target === modalDetalles) closeModal();
});

// ========================================================
// FETCH GET PRODUCTO
// ========================================================
const fetchData = async ({ id_producto, categoria }) => {
  const url = `/admin/api/productos/detalles?id_producto=${id_producto}&categoria=${categoria}`;
  const res = await fetch(url, { credentials:'include' });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
};

// ========================================================
// FETCH PUT ACTUALIZAR PRODUCTO
// ========================================================
const handleSubmit = async data => {
  try {
    const res = await fetch(`/admin/api/productos/${data.id_producto}`, {
      method: 'PUT',
      credentials: 'include',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    console.log('Producto actualizado:', await res.json());
    closeModal();
    // aquí refrescas UI…
  } catch (err) {
    console.error('Error actualizando producto:', err);
  }
};

// ========================================================
// RENDERIZA EL MODAL CON CAMPOS DISABLED
// ========================================================
const viewProduct = async ({ id_producto, categoria }) => {
  const producto = await fetchData({ id_producto, categoria });
  productoGlobal = producto;
  modalDetalles.style.display = 'flex';
  modalTitle.textContent = `Producto #${producto.id_producto}`;

  // Campos estáticos
  let html = `
    <label class="label_field">Precio:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="number"
               name="precio" value="${producto.precio}">
        <button type="button" class="btn-edit">✏️</button>
      </div>
    </label>
    <label class="label_field">Marca:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="text"
               name="marca" value="${producto.marca.nombre}">
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
    <label class="label_field">Imagen:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="text"
               name="imagen" value="${producto.imagen}">
        <button type="button" class="btn-edit">✏️</button>
      </div>
    </label>
  `;

  // Campos dinámicos, incluyendo booleanos tratados como checkbox
  for (const key in producto.detalles) {
    const val = producto.detalles[key];
    let type, extra = '';
    if (typeof val === 'boolean') {
      type = 'checkbox';
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

  // Botón PUT
  html += `<button type="button" id="submit-btn">Guardar cambios</button>`;
  detallesContainer.innerHTML = html;
};

// ========================================================
// DELEGACIÓN DE EVENTOS
//  - Toggle edit en cada campo
//  - Captura submit sin volver a asignar listeners
// ========================================================
detallesContainer.addEventListener('click', e => {
  // 1) Edit toggle
  if (e.target.classList.contains('btn-edit')) {
    const inp = e.target.closest('.input-container').querySelector('input');
    inp.disabled = !inp.disabled;
    e.target.textContent = inp.disabled ? '✏️' : '✔️';
    return;
  }
  // 2) Submit PUT
  if (e.target.id === 'submit-btn') {
    e.preventDefault();
    const formInputs = document.querySelectorAll('#modal-content input');
    const data = { detalles: {} };

    formInputs.forEach(input => {
      let val;
      if (input.type === 'checkbox') {
        val = input.checked;
      } else {
        val = input.type === 'number' ? Number(input.value) : input.value;
      }
      if (input.dataset.static) {
        data[input.name] = val;
      } else {
        data.detalles[input.name] = val;
      }
    });

    data.id_producto = productoGlobal.id_producto;
    data.categoria   = { nombre: productoGlobal.categoria.nombre };
    data.marca       = { nombre: productoGlobal.marca.nombre };

    handleSubmit(data);
  }
});
