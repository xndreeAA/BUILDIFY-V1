const modalDetalles = document.getElementById('modal-detalles-usuario');
const modalTitle = document.getElementById('modal-usuario-title');
const closeModalBtn = document.getElementById('close-modal-btn-usuario');
const detallesContainer = document.getElementById('detalles-container-usuario');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

let usuarioGlobal = null;

const closeModal = () => modalDetalles.style.display = 'none';

closeModalBtn?.addEventListener('click', e => { 
    e.preventDefault(); 
    closeModal(); 
});

window.addEventListener('click', e => { 
    if (e.target === modalDetalles) closeModal(); 
});

const fetchUsuario = async ({ id_usuario }) => {
    const res = await fetch(`/api/v1/usuarios/${id_usuario}`, { credentials: 'include' });
    const json = await res.json();
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return json.data;
};

const viewDetailsUsuario = async ({ id_usuario }) => {
    const usuario = await fetchUsuario({ id_usuario });
    usuarioGlobal = usuario;
    modalTitle.textContent = `Usuario #${usuario.id_usuario}`;
    modalDetalles.style.display = 'flex';

    let html = `
        <label>Nombre:
            <div class="input-container">
                <input disabled class="input_field" name="nombre" value="${usuario.nombre}">
                <button type="button" class="btn-edit">✏️</button>
            </div>
        </label>

        <label>Apellido:
            <div class="input-container">
                <input disabled class="input_field" name="apellido" value="${usuario.apellido}">
                <button type="button" class="btn-edit">✏️</button>
            </div>
        </label>

        <label>Email:
            <div class="input-container">
                <input disabled class="input_field" name="email" value="${usuario.email}">
                <button type="button" class="btn-edit">✏️</button>
            </div>
        </label>

        <label>Teléfono:
            <div class="input-container">
                <input disabled class="input_field" name="telefono" value="${usuario.telefono}">
                <button type="button" class="btn-edit">✏️</button>
            </div>
        </label>

        <label>Dirección:
            <div class="input-container">
                <input disabled class="input_field" name="direccion" value="${usuario.direccion}">
                <button type="button" class="btn-edit">✏️</button>
            </div>
        </label>

        <label>Rol:
            <div class="input-container">
                <select disabled class="input_field" name="id_rol">
                    <option value="1" ${usuario.id_rol == 1 ? "selected" : ""}>Usuario</option>
                    <option value="2" ${usuario.id_rol == 2 ? "selected" : ""}>Moderador</option>
                    <option value="3" ${usuario.id_rol == 3 ? "selected" : ""}>Administrador</option>
                </select>
                <button type="button" class="btn-edit">✏️</button>
            </div>
        </label>

        <button type="button" id="submit-btn">Guardar cambios</button>
    `;
    detallesContainer.innerHTML = html;
};

detallesContainer.addEventListener('click', e => {
    e.preventDefault();

    if (e.target.classList.contains('btn-edit')) {
        const inp = e.target.closest('.input-container').querySelector('.input_field');
        inp.disabled = !inp.disabled;
        e.target.textContent = inp.disabled ? '✏️' : '✔️';
        return;
    }

    if (e.target.id === 'submit-btn') {
        const formInputs = document.querySelectorAll('.input_field');
        const data = {};
        formInputs.forEach(input => { data[input.name] = input.value; });

        fetch(`/api/v1/usuarios/${usuarioGlobal.id_usuario}`, {
            method: 'PUT',
            headers: { 
                'Content-Type': 'application/json', 
                'X-CSRFToken': csrfToken 
            },
            body: JSON.stringify(data)
        })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(json => {
            alert('Usuario actualizado correctamente');
            closeModal();
            tablaUsuarios.ajax.reload(null, false);
        })
        .catch(err => console.error('Error al actualizar usuario:', err));
    }
});
