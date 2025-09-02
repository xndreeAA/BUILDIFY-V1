const modalDetalles = document.getElementById('modal-detalles');
const modalTitle = document.getElementById('modal-detalles-title');
const closeModalBtn = document.getElementById('close-modal-btn');
const detallesContainer = document.getElementById('detalles-container');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


let marcaGlobal = null;

const closeModal = () => modalDetalles.style.display = 'none';

closeModalBtn?.addEventListener('click', e => {
    e.preventDefault();
    closeModal();
});

window.addEventListener('click', e => {
    if (e.target === modalDetalles) closeModal();
});

const fetchData = async ({ id_marca }) => {
    const url = `/api/v1/marcas/${id_marca}`
    const res = await fetch(url, { credentials:'include' });
    const json = await res.json();
    
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return json.data;
};

const viewDetailsMarca = async ({ id_marca }) => {
    const marca = await fetchData({ id_marca });
    marcaGlobal = marca
    modalTitle.textContent = `Marca #${marca.id_marca}`;
    modalDetalles.style.display = 'flex';

    let html = `
        <label class="label_field">Nombre:
        <div class="input-container">
            <input disabled data-static="true" class="input_field" type="text"
                name="nombre" value="${marca.nombre}">
            <button type="button" class="btn-edit">✏️</button>
        </div>
        </label>
        <button type="button" id="submit-btn">Guardar cambios</button>
    `
      detallesContainer.innerHTML = html;
}


detallesContainer.addEventListener('click', e => {
    e.preventDefault();

    if (e.target.classList.contains('btn-edit') && e.target.classList.contains('select')) {
        const inp = e.target.closest('.input-container').querySelector('select');
        inp.disabled = !inp.disabled;
        e.target.textContent = inp.disabled ? '✏️' : '✔️';
        return;
    }

    if (e.target.classList.contains('btn-edit')) {
        const inp = e.target.closest('.input-container').querySelector('input');
        inp.disabled = !inp.disabled;

        if (inp.type === 'checkbox') {
        if (inp.checked) inp.checked = false;
        else inp.checked = true;
        }
        e.target.textContent = inp.disabled ? '✏️' : '✔️';
        return;
    }

    if (e.target.id === 'submit-btn') {
        e.preventDefault();

        const formInputs = document.querySelectorAll('.input_field');
        console.log(formInputs);

        const data = {
            nombre: formInputs[0].value,
        };

        // console.log (data);

        fetch(`/api/v1/marcas/${marcaGlobal.id_marca}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            credentials: 'include',
            body: JSON.stringify(data)
        })
        .then(res => {
            if (!res.ok) throw new Error(`Error HTTP ${res.status}`, res);
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