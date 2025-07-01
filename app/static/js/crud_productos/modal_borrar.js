const modalBorrar = document.getElementById('modal-borrar');
const modalBorrarTitle = document.getElementById('modal-borrar-title');
const closeModalBorrarBtn = document.getElementById('close-modal-btn');
const borrarDetallesContainer = document.getElementById('borrar-detalles-container');

let productoGlobalBorrar = null;

const closeBorrarModal = () => modalBorrar.style.display = 'none';

closeModalBorrarBtn?.addEventListener('click', e => {
  e.preventDefault();
  closeBorrarModal();
});

window.addEventListener('click', e => {
  if (e.target === modalBorrar) closeBorrarModal();
});

const viewDeleteProduct = async ({ id_producto }) => {
    console.log(id_producto);
    
    const producto = await fetchData({ id_producto });
    const marcas = await fetchMarcas();

    modalBorrar.style.display = 'flex';
    modalBorrarTitle.textContent = `Producto #${producto.id_producto}`;

    let html = `
    <label class="label_field">Nombre:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="text"
               name="nombre" value="${producto.nombre}">
      </div>
    </label>
    <label class="label_field">Precio:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="number"
               name="precio" value="${producto.precio}">
      </div>
    </label>
    <label class="label_field">Stock:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="number"
               name="stock" value="${producto.stock}">
      </div>
    </label>
    <label class="label_field">Imagen:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="text"
               name="imagen" value="${producto.imagen}">
      </div>
    </label>
    `;

    html += `
      <label class="label_field">Marca:
        <div class="input-container">
          <input disabled data-static="true" class="input_field" type="text"
               name="marca" value="${producto.marca.nombre}">
        </div>
      </label>
    `;

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
  
          </div>
        </label>
      `;
    }

    html += `<button type="button" id="borrar-submit-btn">Guardar cambios</button>`;
    detallesContainer.innerHTML = html;

    borrarDetallesContainer.innerHTML = html;
}

borrarDetallesContainer.addEventListener('click', e => {
  e.preventDefault();
  if (e.target.id === 'borrar-submit-btn') {
    
    /* __________TODO__________ */

    fetch(`/api/detalles/${productoGlobal.id_producto}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
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
      }
    );
  }
});