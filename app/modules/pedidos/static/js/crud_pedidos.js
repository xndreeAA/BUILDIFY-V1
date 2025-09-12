// Obtener CSRF Token
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

let tablaPedidos;

$(document).ready(function () {
    // Inicializar DataTable
    tablaPedidos = $('#tabla-pedidos').DataTable({
        ajax: {
            url: "/api/v1/pedidos/", // Endpoint Flask que devuelve JSON
            type: "GET",
            dataSrc: "data" // en tu JSON, la lista está dentro de "data"
        },
        columns: [
            { data: "id_pedido" },
            { data: "usuario.nombre", defaultContent: "" }, // nombre cliente
            { data: "fecha_pedido" },
            { 
                data: "valor_total", 
                render: data => `$${parseFloat(data).toFixed(2)}` 
            },
            { data: "estado" },
            {
                data: null,
                render: function (row) {
                    return `<button class="btn-detalles" data-id="${row.id_pedido}">📋 Ver</button>`;
                }
            }
        ]
    });

    // Abrir modal con detalles
    $('#tabla-pedidos').on('click', '.btn-detalles', function () {
        const pedidoId = $(this).data('id');

        $.get(`/api/v1/pedidos/${pedidoId}`, function (pedido) {
            // Mapear campos del JSON
            $('#pedido-id').text(pedido.id_pedido);
            $('#pedido-cliente').text(pedido.usuario.nombre + " " + pedido.usuario.apellido);
            $('#pedido-fecha').text(pedido.fecha_pedido);
            $('#pedido-total').text(parseFloat(pedido.valor_total).toFixed(2));
            $('#estado-pedido').val(pedido.estado);

            // Llenar productos
            let productosHTML = "";
            if (pedido.productos_pedidos && pedido.productos_pedidos.length > 0) {
                pedido.productos_pedidos.forEach(p => {
                    productosHTML += `
                        <tr>
                            <td>${p.nombre}</td>
                            <td>${p.cantidad}</td>
                            <td>$${parseFloat(p.precio).toFixed(2)}</td>
                            <td>$${(p.precio * p.cantidad).toFixed(2)}</td>
                        </tr>
                    `;
                });
            } else {
                productosHTML = `<tr><td colspan="4">No hay productos en este pedido</td></tr>`;
            }
            $('#pedido-productos').html(productosHTML);

            $('#modal-detalles-pedido').fadeIn();
        });
    });

    // Cerrar modal
    $('#close-modal-pedido').on('click', function (e) {
        e.preventDefault();
        $('#modal-detalles-pedido').fadeOut();
    });

    // Guardar nuevo estado
    $('.btn-guardar').on('click', function (e) {
        e.preventDefault();

        const pedidoId = $('#pedido-id').text();
        const nuevoEstado = $('#estado-pedido').val();

        $.ajax({
            url: `/admin/pedidos/${pedidoId}/estado`,
            type: "POST",
            headers: { "X-CSRFToken": csrfToken },
            contentType: "application/json",
            data: JSON.stringify({ estado: nuevoEstado }),
            success: function () {
                alert("Estado actualizado ✅");
                $('#modal-detalles-pedido').fadeOut();
                tablaPedidos.ajax.reload();
            },
            error: function () {
                alert("❌ Error al actualizar");
            }
        });
    });
});
