const pedidosContainer = document.getElementById("mis_pedidos_container")
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


const get_current_user = async () => {
    const res = await fetch(`/api/v1/usuarios/current_user`);
    const { data } = await res.json();
    return data
}

const fetchPedidos = async ({ id_usuario }) => {
    const url = `/api/v1/pedidos/usuario/${id_usuario}`
    const res = await fetch(url, { credentials:'include' });
    const json = await res.json();
    
    console.log(json);
    
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return json.data;
};

const renderEstadoCargando = () => {

    const html = `
        <article class="pedido_container">
            <div class="pedido_div pedido_header">
                <span><strong>Estamos cargando tus pedidos...</strong></span>
            </div>
        </article>
    `

    pedidosContainer.innerHTML = html
}

const renderPedidos = async () => {

    renderEstadoCargando();

    const { id_usuario } = await get_current_user();
    const pedidos = await fetchPedidos({ id_usuario });

    const html_pedidos = pedidos.map(pedido => (
        `
            <article class="pedido_container">
                <div class="pedido_div pedido_header">
                    <span><strong>${pedido.fecha_pedido}</strong></span>
                    <span><strong>ID pedido: ${pedido.id_pedido}</strong></span>
                </div>
                <div class="pedido_div">
                    <div class="detalles_pedido_container">
                        <h3>DETALLES DEL PAGO:</h3>

                        <p><span><strong>Total:</strong> $${pedido.valor_total}</span></p>
                        <p><span><strong>Fecha y hora del pago:</strong> ${pedido.fecha_pedido}</span></p>
                        <p><span><strong>Metodo de pago:</strong> Transferencia bancaria</span></p>
                        ${
                            (pedido.factura.factura_url_pdf_cloud || pedido.factura.factura_url_pdf_stripe)
                                ? `<a href="${pedido.factura.factura_url_pdf_cloud || pedido.factura.factura_url_pdf_stripe}"><span><strong>Ver factura</strong></span></a>`
                                : `<p><span><strong>Factura aun no disponible</strong></span></p>`
                        }
                    </div>
                </div>
                <div class="pedido_div">
                    <div class="detalles_pedido_container">
                        <h3>DETALLES DE ENTREGA</h3>

                        <p><span><strong>Estado:</strong> ${pedido.estado}</span></p>
                        <p><span><strong>Direccion de entrega:</strong></span> ${pedido.usuario.direccion}</p>
                        <p>¿Tienes problemas? Hablanos sobre tu compra <a href="">aqui</a></p>
                    </div>
                </div>
                <div class="pedido_div productos_pedidos_container">
                    <hr>
                    <h3>PRODUCTOS PEDIDOS:</h3>
                    ${pedido.productos_pedidos.map(producto => (
                        `
                            <section class="producto_pedido">
                                <div class="producto_info">
                                    <article>
                                        <img src="${producto.producto.imagenes[0].ruta}" alt="${producto.producto.nombre}">
                                    </article>
                                    <article>
                                        <p><strong>${producto.producto.nombre}</strong></p>
                                        <p><strong>Categoria:</strong> ${producto.producto.categoria}</p>
                                        <p><strong>Marca:</strong> ${producto.producto.marca}</p>
                                        <p><strong>Precio:</strong> ${producto.producto.precio}</p>
                                        <p><strong>Cantidad:</strong> ${producto.cantidad}</p>
                                        <p><a href="">editar opinion</a></p>
                                    </article>
                                </div>
                                <div>
                                    <hr>
                                </div>
                            </section>
                        `
                    ))}

                </div>
            </article>
        
        `
    ))



    pedidosContainer.innerHTML = `
        <div class="title_container">
            <h1>Mis pedidos</h1>
        </div>
        ${html_pedidos.join("")}
    `;

}   

renderPedidos();