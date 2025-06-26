console.log("Usuarios");

$(document).ready(function() {
    $('#tabla-usuarios').DataTable({
        ajax: {
            url: "/api/usuarios",
            dataSrc: "data",
            error: function(xhr) { console.error('AJAX Error:', xhr); }
        },
        columns: [
            { data: "id_usuario" },
            { data: "nombre" },
            { data: "apellido" },
            { data: "email" },
            { data: "telefono" },
            { data: "direccion" },
            { data: "id_rol" },
            {
                data: null,
                orderable: false,
                render: function(data, type, row) {
                    return `<div class="btn-group">
                        <a href="/admin/eliminar-usuario/${row.id_usuario}" class="btn btn-sm btn-danger">🗑️</a>
                        <button class="btn btn-sm btn-info view-product" data-id="${row.id_usuario}" onClick="viewUser({ id_usuario: ${row.id_usuario} })">✏️</button>
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