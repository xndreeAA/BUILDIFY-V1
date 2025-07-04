$(document).ready(function() {
    $('#tabla-productos').DataTable({
        ajax: {
            url: "/api/productos",
            dataSrc: "data",
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
                        <button class="btn btn-sm btn-danger" data-id="${row.id_producto}" onClick="viewDeleteProduct({ id_producto: ${row.id_producto} })">🗑️</button>
                        <button class="btn btn-sm btn-info view-product" data-id="${row.id_producto}" onClick="viewDetailsProduct({ id_producto: ${row.id_producto} })">✏️</button>
                    </div>`;
                }
            }
        ],
        dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>" +
            "<'row'<'col-sm-12'B>>",  
        // dom: 'Bfrtip',  
        buttons: [
            {
                extend: 'excel',
                text: 'Excel',
                className: 'btn btn-success',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5] 
                }
            },
            {
                extend: 'csv',
                text: 'CSV',
                className: 'btn btn-info',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5]
                }
            },
            {
                extend: 'pdf',
                text: 'PDF',
                className: 'btn btn-danger',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5]
                },
                customize: function (doc) {
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                }
            },
            {
                extend: 'print',
                text: 'Imprimir',
                className: 'btn btn-warning',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5]
                }
            }
        ],
        language: {
            info: "_START_ a _END_ de _TOTAL_ productos",
            paginate: {
                "previous": "‹",
                "next": "›"
            },
            buttons: {
                excel: "Excel",
                csv: "CSV",
                pdf: "PDF",
                print: "Imprimir"
            },
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ productos por página",
        },
    });
});