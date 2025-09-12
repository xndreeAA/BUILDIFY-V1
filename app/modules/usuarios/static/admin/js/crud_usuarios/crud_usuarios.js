let tablaUsuarios;

$(document).ready(function() {
    tablaUsuarios = $('#tabla-usuarios').DataTable({
        ajax: {
            url: "/api/v1/usuarios/",
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
            { data: "rol_nombre" },
            {
                data: null,
                orderable: false,
                render: function(data, type, row) {
                    return `<div class="btn-group">
                        <button class="btn btn-sm btn-danger" onClick="viewDeleteUsuario({ id_usuario: ${row.id_usuario} })">🗑️</button>
                        <button class="btn btn-sm btn-info" onClick="viewDetailsUsuario({ id_usuario: ${row.id_usuario} })">✏️</button>
                    </div>`;
                }
            }
        ],
        dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>" +
                "<'row'<'col-sm-12'B>>",  
        buttons: [
            { extend: 'excel', text: 'Excel', className: 'btn btn-success', exportOptions: { columns: [0,1,2,3,4,5,6] } },
            { extend: 'csv', text: 'CSV', className: 'btn btn-info', exportOptions: { columns: [0,1,2,3,4,5,6] } },
            { extend: 'pdf', text: 'PDF', className: 'btn btn-danger', exportOptions: { columns: [0,1,2,3,4,5,6] },
                customize: function (doc) {
                    doc.content[1].table.widths = Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                }},
            { extend: 'print', text: 'Imprimir', className: 'btn btn-warning', exportOptions: { columns: [0,1,2,3,4,5,6] } }
        ],
        language: {
            info: "_START_ a _END_ de _TOTAL_ usuarios",
            paginate: { previous: "‹", next: "›" },
            buttons: { excel: "Excel", csv: "CSV", pdf: "PDF", print: "Imprimir" },
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ usuarios por página",
        },
    });
});
