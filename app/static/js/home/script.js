document.addEventListener("DOMContentLoaded", () => {
    fetch('/api/productos/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const productos = data.data;
                console.log(productos);
                
                const contenedor = document.getElementById('fila-productos-mas-vendidos');

                for (let i = 0; i < 5 && i < productos.length; i++) {
                    
                    const elemento = document.createElement('a');
                    elemento.href = `/producto/${productos[i].id_producto}`; // Puedes ajustar esto
                    elemento.className = 'tarjeta-producto';
                    
                    elemento.innerHTML = `
                        <article>
                            <picture>
                                <button class="btn-ampliar">
                                    <svg xmlns="http://www.w3.org/2000/svg" height="16px" viewBox="0 -960 960 960" width="16px"
                                        fill="#FFFFFF">
                                        <path d="m243-240-51-51 405-405H240v-72h480v480h-72v-357L243-240Z" />
                                    </svg>
                                </button>
                               
                                <img src="/static/${productos[i].imagenes[0].ruta}" alt="${productos[i].nombre}">
                            </picture>
                            <div class="tarjeta-producto-info">
                                <h4>${productos[i].nombre}</h4>
                                <div class="categoria-marca-info">
                                    <p><span>Categoria: <b>${productos[i].categoria}</b></span></p>
                                    <p><span>Marca: <b>${productos[i].marca}</b></span></p>
                                </div>
                                <p class="p-precio"><b>$${productos[i].precio.toLocaleString('es-CO')}</b></p>
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