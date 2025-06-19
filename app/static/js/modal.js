const modal = document.querySelector('.modal-detalles');
const modalTitle = document.getElementById('modal-title');
const closeModalBtn = document.getElementById('close-modal-btn');
const detallesContainer = document.querySelector('.detalles-container');

const fetchData = async ({ id_producto, categoria }) => {
    
    const url = `/admin/api/productos/detalles?id_producto=${id_producto}&categoria=${categoria}`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const producto = await response.json();
        console.log(producto);
        return producto;
    } catch (error) {
        console.error('Error al cargar el producto:', error);
        throw error;
    }
}

const viewProduct = async ({ id_producto, categoria }) => {
    const producto = await fetchData({ id_producto, categoria });
    modal.style.display = 'flex';

    modalTitle.textContent = `Id del producto: ${producto.id_producto}`;

    let html = "";
    html += 
        `   
            <label for="precio" class="label_field">Precio:
                <div class="input-container">
                    <input  class="input_field" type="number" name="precio" value="${producto.precio}" id="precio-producto">
                    <button class="btn-edit">✏️</button>
                </div>
            </label>
            <label for="precio" class="label_field">Marca:
                <div class="input-container">
                    <input  class="input_field" type="text" name="marca" value="${producto.marca.nombre}" id="marca-producto">
                    <button class="btn-edit">✏️</button>
                </div>
            </label>
            <label for="stock" class="label_field">Stock:
                <div class="input-container">
                    <input  class="input_field" type="number" name="stock" value="${producto.stock}" id="stock-producto">
                    <button class="btn-edit">✏️</button>
                </div>
            </label>
            <label for="imagen" class="label_field">Imagen:
                <div class="input-container">
                    <input  class="input_field" type="text" name="imagen" value="${producto.imagen}" id="imagen-producto">
                    <button class="btn-edit">✏️</button>
                </div>
            </label>
        `
    
    for (const key in producto.detalles) {
        html +=         
            `<label for="${key}" class="label_field">${key.charAt(0).toUpperCase() + key.slice(1)}:
                <div class="input-container">
                    <input  class="input_field" type="number" name="${key}" value="${producto.detalles[key]}" id="${key}-producto">
                    <button class="btn-edit">✏️</button>
                </div>
            </label>`
    }
    detallesContainer.innerHTML = html;
};

const closeModal = () => {
    console.log('Cerrando modal');
    modal.style.display = 'none';
};

if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeModal);
}

window.addEventListener('click', (event) => {
    if (event.target === modal) {
        closeModal();
    }
});