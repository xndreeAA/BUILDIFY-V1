const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
let container = document.getElementById("carrito-container");

const recalculateTotal = () => {
    const productCards = document.querySelectorAll(".producto-carrito");
    let total = 0;

    productCards.forEach(card => {
        const precioText = card.querySelector(".precio-original")?.textContent;
        const cantidadInput = card.querySelector("input[name='cantidad']");

        if (precioText && cantidadInput) {
            const precio = parseFloat(precioText.replace(/[^\d.-]/g, ''));
            const cantidad = parseInt(cantidadInput.value);
            if (!isNaN(precio) && !isNaN(cantidad)) {
                total += precio * cantidad;
            }
        }
    });

    const totalDisplay = document.querySelector(".cart-total h3");
    if (totalDisplay) {
        totalDisplay.textContent = `Total: ${formatPrice(total)}`;
    }
};

function hdlEliminar({ id_producto }) {
    fetch(`/api/carrito/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ id_producto })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const card = document.querySelector(`#producto-${id_producto}`);
            if (card) card.remove();

            recalculateTotal();
        } else {
            alert(data.error);
        }
    });
}

const getCsrfToken = () => {
    const token = document.querySelector('meta[name="csrf-token"]');
    if (!token) throw new Error('CSRF token not found');
    return token.getAttribute('content');
};

const getUserId = () => {
    const userId = document.body.dataset.userId;
    if (!userId) throw new Error('User ID not found');
    return userId;
};

const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'COP'
    }).format(price);
};

const createCartItemTemplate = (producto) => `
    <article class="producto-carrito" id="producto-${producto.id_producto}">
        <img src="/static/${producto.imagenes[0].ruta}" alt="${producto.nombre}" /> 
        <div class="info-producto">
            <h3>${producto.nombre}</h3>
            <p>Color: black</p>
            <p class="precio-original">Precio: ${formatPrice(producto.precio)}</p>
            <div class="cantidad-container">
                <label for="cantidad-${producto.id_producto}">Cantidad: </label>
                <input 
                    type="number" 
                    name="cantidad" 
                    id="cantidad-${producto.id_producto}" 
                    value="${producto.cantidad || 1}"
                    min="1"
                    max="${producto.stock}"
                    onchange="handleQuantityChange(event, ${producto.id_producto})"
                />
            </div>
            <button 
                class="eliminar" 
                onclick="confirmDelete(${producto.id_producto})"
            >Eliminar</button>
        </div>
    </article>
`;

let quantityUpdateTimeout;
const handleQuantityChange = (event, productId) => {
    clearTimeout(quantityUpdateTimeout);
    const quantity = parseInt(event.target.value);
    
    if (isNaN(quantity) || quantity < 1) {
        event.target.value = 1;
        return;
    }
    
    quantityUpdateTimeout = setTimeout(() => {
        updateQuantity(productId, quantity);
    }, 500);
};

const confirmDelete = (productId) => {
    if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
        hdlEliminar({ id_producto: productId });
    }
};

const showLoading = () => {
    container.innerHTML = '<div class="loading">Cargando...</div>';
};

const showError = (message) => {
    container.innerHTML = `<div class="error">${message}</div>`;
};

document.addEventListener("DOMContentLoaded", async () => {
    try {

        showLoading();
        
        const response = await fetch(`/api/carrito/`);
        if (!response.ok) throw new Error('Error al cargar el carrito');
        
        const data = await response.json();
        if (!data.success) throw new Error(data.message || 'Error desconocido');
        
        const { carrito } = data;
        const html = carrito.items.length > 0
            ? carrito.items.map(createCartItemTemplate).join('')
            : '<article class="producto-carrito"><p>El carrito está vacío</p></article>';
            
        container.innerHTML = html; 
        
        if (carrito.items.length > 0) {
            container.insertAdjacentHTML('beforeend', `
                <div class="cart-total">
                    <h3>Total: ${formatPrice(carrito.total)}</h3>
                </div>
            `);

            const total = document.getElementById("total");
            total.textContent = `Total: ${formatPrice(carrito.total)}`;
        }
    } catch (error) {
        console.error(error);
        showError('No se pudo cargar el carrito. Por favor, intenta de nuevo más tarde.');
    }
});