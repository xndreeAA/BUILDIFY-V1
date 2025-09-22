/**
 * Script de gestión de filtros en la vista de categorías.
 * Funcionalidades:
 *  1. Cargar dinámicamente las marcas desde la API.
 *  2. Filtrar productos por categoría y marca.
 *  3. Renderizar dinámicamente las tarjetas de productos filtrados con la misma
 *     estructura que el HTML original (para que el carrito funcione).
 */

document.addEventListener("DOMContentLoaded", async function () {
    // Elementos del DOM
    const filtroMarca = document.getElementById("marca");
    const aplicarFiltro = document.getElementById("aplicar-filtro");
    const productosContainer = document.querySelector(".products-container");
    const categoria = document.getElementById("title_categorias").dataset.categoria;

    /**
     * Cargar marcas dinámicamente desde la API y añadirlas al <select>.
     */
    try {
        const res = await fetch("/api/v1/marcas/");
        const result = await res.json();

        if (result.success) {
            result.data.forEach(marca => {
                const option = document.createElement("option");
                option.value = marca.nombre.toLowerCase();
                option.textContent = marca.nombre;
                filtroMarca.appendChild(option);
            });
        }
    } catch (error) {
        console.error("❌ Error cargando marcas:", error);
    }

    /**
     * Cargar productos filtrados por categoría y marca desde la API.
     */
    async function cargarProductos() {
        const marca = filtroMarca.value;

        // Construir URL con parámetros de categoría y, opcionalmente, marca
        let url = `/api/v1/productos?categoria=${categoria}`;
        if (marca) {
            url += `&marca=${marca}`;
        }

        try {
            const response = await fetch(url);
            const result = await response.json();

            productosContainer.innerHTML = ""; // Limpiar contenedor antes de renderizar

            if (result.success && result.data.length > 0) {
                // Crear tarjeta para cada producto
                result.data.forEach(product => {
                    const card = `
                        <div class="cards_container">
                            <!-- Columna izquierda -->
                            <div class="product-left">
                                <a href="/productos/${product.id_producto}">
                                    <img src="${product.imagenes.length > 0 ? product.imagenes[0].ruta : '/static/img/default-product.png'}" 
                                        alt="${product.nombre}" />
                                </a>
                                <div class="product-info">
                                    <p class="categoria">${categoria}</p>
                                    <h3>${product.nombre}</h3>
                                </div>
                            </div>

                            <!-- Columna derecha -->
                            <div class="product-right">
                                <div class="precio">
                                    <p>$${new Intl.NumberFormat().format(product.precio)}</p>
                                </div>
                                <hr>
                                <div class="cantidad">
                                    <label for="cantidad-${product.id_producto}">Cantidad</label>
                                    <div class="cantidad-input">
                                        <input type="number" 
                                                id="cantidad-${product.id_producto}" 
                                                name="cantidad" 
                                                value="1" 
                                                min="1" 
                                                max="${product.stock}" />
                                        </div>
                                </div>
                                <div class="boton_agregar_producto">
                                    <button class="btn-styled btn-agregar" data-id="${product.id_producto}">
                                        + Añadir al carrito
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                    productosContainer.insertAdjacentHTML("beforeend", card);
                });
            } else {
                productosContainer.innerHTML = "<p>No hay productos en esta categoría con ese filtro.</p>";
            }
        } catch (error) {
            console.error("❌ Error al cargar productos:", error);
            productosContainer.innerHTML = "<p>Error al cargar productos.</p>";
        }
    }

    // Eventos: aplicar filtros manualmente o al cambiar de marca
    aplicarFiltro.addEventListener("click", cargarProductos);
    filtroMarca.addEventListener("change", cargarProductos);
});
