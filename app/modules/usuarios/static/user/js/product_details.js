document.addEventListener("DOMContentLoaded", () => {
    const id = document.body.dataset.productId;

    if (!id) {
        console.error("No se encontró el ID del producto.");
        return;
    }

    // Llama a la API para obtener la información básica del producto
    fetch(`/api/v1/productos/${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderProducto(data.data);
                // Renderizar el producto, carga los detalles técnicos
                cargarDetallesTecnicos(data.data.id_producto);
            } else {
                console.error("Producto no encontrado");
            }
        })
        .catch(error => {
            console.error("Error al cargar el producto:", error);
        });
});

function renderProducto(producto) {
    const contenedor = document.getElementById("detalle-producto");

    contenedor.innerHTML = `
        <div class="details_product">
            <div class="img_product">
                <img src="${producto.imagenes[0].ruta}" alt="${producto.nombre}">
            </div>

            <div class="description_product">
                <div class="volver">
                    <p id="home_link">
                        ← Regresar al home <a href="/">Volver</a>
                    </p>
                </div>
                <h1>${producto.nombre}</h1>
                <h3>$${producto.precio.toLocaleString('es-CO')}</h3>
                <p>${producto.descripcion || "Descripción no disponible."}</p>
                
                <div class="boton_agregar_categoria">
                    <button id="agregar" class="btn-styled">Añadir al carrito</button>
                </div>

                <div class="cantidad">
                    <input type="number" name="cantidad" id="cantidad" placeholder="Cantidad" min="1" max="10" />
                </div>

                <div class="boton_agregar_categoria">
                    <button id="comprar-ahora" class="btn-styled">Comprar ahora</button>
                </div>
            </div>

            <div id="detalles-tecnicos" class="detalles-tecnicos">
                <!-- Aquí se insertarán los detalles técnicos -->
            </div>
        </div>
    `;

    document.getElementById('agregar')?.addEventListener('click', () => agregarAlCarrito(producto));
    document.getElementById('comprar-ahora')?.addEventListener('click', () => comprarAhora(producto));
}

function cargarDetallesTecnicos(idProducto) {
    fetch(`/api/v1/detalles/${idProducto}`)
        .then(res => res.json())
        .then(data => {
            const contenedorDetalles = document.getElementById("detalles-tecnicos");

            if (data.success) {
                const d = data.data;
                contenedorDetalles.innerHTML = `
                    <div id="conten-detalles-derecha">
                        <h3>Detalles del producto</h3>
                        <p><b>Marca:</b> ${d.marca.nombre}</p>
                        <p><b>Categoría:</b> ${d.categoria.nombre}</p>
                    </div>
                    <div id="conten-detalles-izquierda">
                        <h3>Detalles técnicos</h3>
                        ${
                            d.detalles ?
                            Object.entries(d.detalles)
                                .map(([k, v]) => `<p><b>${k.replace(/_/g, ' ')}:</b> ${v}</p>`)
                                .join('') :
                            '<p>No hay detalles técnicos disponibles.</p>'
                        }
                    </div>
                `;
            } else {
                contenedorDetalles.innerHTML = "<p>No se pudo cargar detalles técnicos.</p>";
            }
        })
        .catch(error => {
            console.error("Error al obtener detalles técnicos:", error);
            const contenedorDetalles = document.getElementById("detalles-tecnicos");
            contenedorDetalles.innerHTML = "<p>Error al cargar detalles técnicos.</p>";
        });
}

/* -----------------------------------------------
    FUNCIÓN AGREGADA: agregarAlCarrito(producto)
    Permite añadir un producto al carrito desde 
    la vista de detalles.
-------------------------------------------------- */
function agregarAlCarrito(producto) {
    const cantidadInput = document.getElementById("cantidad");
    const cantidad = parseInt(cantidadInput?.value) || 1;

    fetch("/api/v1/carrito/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        },
        body: JSON.stringify({
            id_producto: producto.id_producto,
            cantidad: cantidad
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Producto agregado al carrito correctamente");
        } else {
            alert(data.error || "No se pudo agregar al carrito");
        }
    })
    .catch(error => {
        console.error("Error al agregar al carrito:", error);
        alert("Ocurrió un error al intentar agregar el producto al carrito.");
    });
}
