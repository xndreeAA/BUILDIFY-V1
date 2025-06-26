const modalDetalles = document.querySelector('.modal-detalles');
const modalTitle = document.getElementById('modal-title');
const closeModalBtn = document.getElementById('close-modal-btn');
const detallesContainer = document.querySelector('.detalles-container');

let usuarioGlobal = null;

const closeModal = () => modalDetalles.style.display = 'none';

closeModalBtn?.addEventListener('click', e => {
  e.preventDefault();
  closeModal();
});

window.addEventListener('click', e => {
  if (e.target === modalDetalles) closeModal();
});

const fetchData = async ({ id_usuario }) => {
  const url = `/api/usuarios/${id_usuario}`
  const res = await fetch(url, { credentials:'include' });
  const json = await res.json();
  
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return json.data;
};

const viewUser = async ({ id_usuario }) => {
  const usuario = await fetchData({ id_usuario });

  usuarioGlobal = usuario
  modalDetalles.style.display = 'flex';
  modalTitle.textContent = `Usuarios #${usuario.id_usuario}`;

  let html = `
    <label class="label_field">Nombre:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="text"
               name="nombre" value="${usuario.nombre}">
        <button type="button" class="btn-edit">✏️</button>
      </div>
    </label>
    <label class="label_field">Apellido:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="text"
               name="apellido" value="${usuario.apellido}">
        <button type="button" class="btn-edit">✏️</button>
      </div>
    </label>
    <label class="label_field">Email:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="text"
               name="email" value="${usuario.email}">
        <button type="button" class="btn-edit">✏️</button>
      </div>
    </label>
    <label class="label_field">Telefono:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="text"
               name="telefono" value="${usuario.telefono}">
        <button type="button" class="btn-edit">✏️</button>
      </div>
    </label>
    <label class="label_field">Direccion:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="text"
               name="direccion" value="${usuario.direccion}">
        <button type="button" class="btn-edit">✏️</button>
      </div>
    </label>
    <label class="label_field">Rol:
      <div class="input-container">
        <input disabled data-static="true" class="input_field" type="text"
               name="rol" value="${usuario.id_rol}">
        <button type="button" class="btn-edit">✏️</button>
      </div>
    </label>
  `;

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
      nombre: usuarioGlobal.nombre,
      apellido: usuarioGlobal.apellido,
      email: usuarioGlobal.email,
      direccion: usuarioGlobal.direccion,
      telefono: usuarioGlobal.telefono,
      id_rol: usuarioGlobal.id_rol,
      password: usuarioGlobal.password
    };

    formInputs.forEach(input => {
      const name = input.name;
      let val;

      if (input.type === 'checkbox') {
        val = input.checked;
      } else if (input.type === 'number') {
        if (input.name === 'telefono') return;
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

    fetch(`/api/usuarios/${usuarioGlobal.id_usuario}`, {
      method: 'PUT',
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
      alert('Usuario actualizado correctamente');
      closeModal();
    })
    .catch(err => {
      console.error('Error al actualizar usuario:', err);
      alert('Hubo un error al guardar los cambios');
    });
  }
});
