$(document).ready(function() {
    $('#tabla-categorias').DataTable({
        ajax: {
            url: "/api/v1/categorias/",
            dataSrc: "data",
            error: function(xhr) { console.error('AJAX Error:', xhr); }
        },
        columns: [
            { data: "id_categoria" },
            { data: "nombre" },
            {
                data: null,
                orderable: false,
                render: function(data, type, row) {
                    return `<div class="btn-group">
                        <button class="btn btn-sm btn-danger" onClick="viewDeleteCategoria({ id_categoria: ${row.id_categoria} })">🗑️</button>
                        <button class="btn btn-sm btn-info" onClick="viewDetailsCategoria({ id_categoria: ${row.id_categoria} })">✏️</button>
                    </div>`;
                }
            }
        ],
        dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>" +
            "<'row'<'col-sm-12'B>>",  
        buttons: [
            {
                extend: 'excel',
                text: 'Excel',
                className: 'btn btn-success',
                exportOptions: { columns: [0, 1] }
            },
            {
                extend: 'csv',
                text: 'CSV',
                className: 'btn btn-info',
                exportOptions: { columns: [0, 1] }
            },
            {
                extend: 'pdf',
                text: 'PDF',
                className: 'btn btn-danger',
                exportOptions: { columns: [0, 1] },
                customize: function (doc) {
                    doc.content[1].table.widths = 
                        Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                }
            },
            {
                extend: 'print',
                text: 'Imprimir',
                className: 'btn btn-warning',
                exportOptions: { columns: [0, 1] }
            }
        ],
        language: {
            info: "_START_ a _END_ de _TOTAL_ categorías",
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
            lengthMenu: "Mostrar _MENU_ categorías por página",
        },
    });
});
