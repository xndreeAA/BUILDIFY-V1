// Espera que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
    // Obtiene el ID del producto desde el atributo data-product-id del body
    const id = document.body.dataset.productId;
    console.log("ID capturado:", id);

    if (!id) {
        console.error("No se encontró el ID del producto.");
        return;
    }

    // Llama a la API para obtener la información básica del producto
    fetch(`/api/productos/${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderProducto(data.data); // Renderiza la estructura del producto
            } else {
                console.error("Producto no encontrado");
            }
        })
        .catch(error => {
            console.error("Error al cargar el producto:", error);
        });
});

// Función principal para pintar el producto en pantalla
function renderProducto(producto) {
    const contenedor = document.getElementById("detalle-producto");

    // Construye la estructura HTML del producto
    contenedor.innerHTML = `
        <div class="details_product">
            <div class="img_product">
                <img src="/static/${producto.imagenes[0].ruta}" alt="${producto.nombre}">
            
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
                
                <a href="/carrito">
                    <div class="boton_agregar_categoria">
                        <button id="agregar" class="btn-styled">Añadir al carrito</button>
                    </div>
                </a>

                <div class="cantidad">
                    <input type="number" name="cantidad" id="cantidad" placeholder="Cantidad" min="1" max="10" />
                </div>

                <div class="boton_agregar_categoria">
                    <button id="comprar-ahora" class="btn-styled">Comprar ahora</button>
                </div>

                
                    <button id="ver-detalles" class="btn-styled">Ver detalles</button>
                
            </div>
        </div>

        <!-- Modal que se mostrará al hacer clic en "Ver detalles" -->

        <div id="modal-detalles" class="modal-detalles">
            <div class="modal-backdrop"></div>
            <div class="modal-contenido">
                <button id="cerrar-modal" class="cerrar-modal">X</button>
                <div id="contenido-detalles"></div>
            </div>
        </div>
    `;

    // Event listener para añadir producto al carrito
    document.getElementById('agregar')?.addEventListener('click', () => agregarAlCarrito(producto));

    // Event listener para comprar ahora
    document.getElementById('comprar-ahora')?.addEventListener('click', () => comprarAhora(producto));

    // Event listener para mostrar el modal con los detalles técnicos
    document.getElementById('ver-detalles').addEventListener('click', () => {
        const idProducto = producto.id_producto;
        const modal = document.getElementById("modal-detalles");
        const contenido = document.getElementById("contenido-detalles");

        // Llama al endpoint que devuelve los detalles técnicos del producto
        fetch(`/api/detalles/${idProducto}`)
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const d = data.data;
                    contenido.innerHTML = `
                        <h2>${d.nombre}</h2>
                        <p><b>Precio:</b> $${d.precio.toLocaleString('es-CO')}</p>
                        <p><b>Marca:</b> ${d.marca.nombre}</p>
                        <p><b>Categoría:</b> ${d.categoria.nombre}</p>
                        <hr/>
                        <h3>Detalles técnicos</h3>
                        ${
                            d.detalles ? 
                            Object.entries(d.detalles)
                                .map(([k, v]) => `<p><b>${k.replace(/_/g, ' ')}:</b> ${v}</p>`)
                                .join('') :
                            '<p>No hay detalles técnicos disponibles.</p>'
                        }
                    `;
                    modal.classList.add("show");
                } else {
                    contenido.innerHTML = "<p>No se pudo cargar detalles.</p>";
                    modal.classList.add("show");
                }
            })
            .catch(error => {
                console.error("Error al obtener detalles:", error);
                contenido.innerHTML = "<p>Error al cargar detalles.</p>";
                modal.classList.add("show");
            });

        // Cierra el modal al hacer clic en el botón X
        document.getElementById("cerrar-modal").addEventListener("click", () => {
            modal.classList.remove("show");
        });

        // Cierra el modal al hacer clic fuera del contenido
        window.addEventListener("click", (e) => {
            if (e.target === modal) {
                modal.classList.remove("show");
            }
        });
    });
}
