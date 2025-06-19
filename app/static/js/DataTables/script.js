console.log('te amo js')

$(document).ready(function() {
    $('#tabla-productos').DataTable({
        ajax: {
            url: "/admin/api/productos",
            dataSrc: "",
            error: function(xhr) { console.error('AJAX Error:', xhr); }
        },
        columns: [
            { data: "id_producto" },
            { data: "nombre" },
            { 
                data: "precio",
                render: function(data) {
                    const price = parseFloat(data);
                    return isNaN(price) ? "$0.00" : `$${price.toFixed(2)}`;
                }
            },
            { data: "stock" },
            { data: "categoria" },
            { data: "marca" },
            {
                data: null,
                orderable: false,
                render: function(data, type, row) {
                    return `<div class="btn-group">
                        <a href="/admin/eliminar-producto/${row.id_producto}" class="btn btn-sm btn-danger">🗑️</a>
                        <button class="btn btn-sm btn-info view-product" data-id="${row.id_producto}" onClick="viewProduct({ id_producto: ${row.id_producto}, categoria: '${row.categoria}' })">✏️</button>
                    </div>`;
                }
            }
        ],
        language: {
        "url": "//cdn.datatables.net/plug-ins/1.11.5/i18n/es-ES.json",
        "info": "_START_ a _END_ de _TOTAL_ productos",
        "paginate": {
            "previous": "‹",
            "next": "›"
        }
    },
    });
});