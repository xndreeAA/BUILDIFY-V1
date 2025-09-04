const modalDetalles = document.getElementById('modal-detalles');
const modalTitle = document.getElementById('modal-detalles-title');
const closeModalBtn = document.getElementById('close-modal-btn');
const detallesContainer = document.getElementById('detalles-container');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

let categoriaGlobal = null;

const closeModal = () => modalDetalles.style.display = 'none';

closeModalBtn?.addEventListener('click', e => {
    e.preventDefault();
    closeModal();
});

window.addEventListener('click', e => {
    if (e.target === modalDetalles) closeModal();
});

const fetchData = async ({ id_categoria }) => {
    const url = `/api/v1/categorias/${id_categoria}`;   
    const res = await fetch(url, { credentials: 'include' });
    const json = await res.json();

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return json.data;
};

const viewDetailsCategoria = async ({ id_categoria }) => {
    const categoria = await fetchData({ id_categoria });
    categoriaGlobal = categoria;
    modalTitle.textContent = `Categoría #${categoria.id_categoria}`;
    modalDetalles.style.display = 'flex';

    let html = `
        <label class="label_field">Nombre:
        <div class="input-container">
            <input disabled data-static="true" class="input_field" type="text"
                name="nombre" value="${categoria.nombre}">
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
        const inp = e.target.closest('.input-container').querySelector('input');
        inp.disabled = !inp.disabled;
        e.target.textContent = inp.disabled ? '✏️' : '✔️';
        return;
    }

    if (e.target.id === 'submit-btn') {
        e.preventDefault();

        const formInputs = document.querySelectorAll('.input_field');
        const data = {
            nombre: formInputs[0].value,
        };

        fetch(`/api/v1/categorias/${categoriaGlobal.id_categoria}`, {   // ✅ corregido
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
        .then(result => {
            console.log('Guardado con éxito:', result);
            closeModal();
        })
        .catch(err => console.error('Error al guardar:', err));
    }
});
