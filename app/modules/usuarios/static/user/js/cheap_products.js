document.addEventListener("DOMContentLoaded", () => {
    fetch('/api/v1/productos/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let productos = data.data;

                // Ordenamos de menor a mayor precio
                productos.sort((a, b) => a.precio - b.precio);

                const contenedor = document.getElementById('contenedor-productos-baratos');

                // Mostramos los 5 más baratos (o menos si hay pocos productos)
                for (let i = 0; i < 5 && i < productos.length; i++) {
                    const producto = productos[i];

                    const elemento = document.createElement('a');
                    elemento.href = `/product_details/${producto.id_producto}`;
                    elemento.className = 'tarjeta-producto';
                    
                    elemento.innerHTML = `
                        <article>
                            <picture>
                                <button class="btn-ampliar">
                                    <svg xmlns="http://www.w3.org/2000/svg" height="16px" 
                                        viewBox="0 -960 960 960" width="16px" fill="#FFFFFF">
                                        <path d="m243-240-51-51 405-405H240v-72h480v480h-72v-357L243-240Z" />
                                    </svg>
                                </button>
                                <img src="${producto.imagenes[0]?.ruta || '/img/default.png'}" alt="${producto.nombre}">
                            </picture>
                            <div class="tarjeta-producto-info">
                                <h4>${producto.nombre}</h4>
                                <div class="categoria-marca-info">
                                    <p><span>Categoria: <b>${producto.categoria}</b></span></p>
                                    <p><span>Marca: <b>${producto.marca}</b></span></p>
                                </div>
                                <p class="p-precio"><b>$${producto.precio.toLocaleString('es-CO')}</b></p>
                            </div>
                            <p class="categoria-marca-info">envio gratis</p>
                        </article>
                    `;

                    contenedor.appendChild(elemento);
                }

            } else {
                console.error('Error al cargar productos');
            }
        })
        .catch(error => {
            console.error('Error en la petición:', error);
        });
});
