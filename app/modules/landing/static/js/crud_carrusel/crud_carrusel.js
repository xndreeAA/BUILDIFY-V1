// ======================================================================
// CRUD Carrusel - Frontend
// Manejo de DataTable, modal y peticiones AJAX/Fetch para el carrusel
// Incluye sistema de notificaciones unificado (mostrarNotificacion)
// ======================================================================

$(document).ready(function () {
    // 🔹 Token CSRF (definido en layout con meta)
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // ==================================================================
    // Inicialización DataTable
    // ==================================================================
    const tabla = $('#tabla-carrusel').DataTable({
        ajax: {
            url: "/api/v1/carrusel/", // Endpoint listar
            dataSrc: "data",
            error: function (xhr) {
                mostrarNotificacion("❌ Error cargando datos: " + (xhr.responseText || xhr.statusText), "error");
            }
        },
        columns: [
            { data: "id_carrusel" },
            { data: "titulo" },
            { data: "descripcion" },
            {
                data: "url_imagen",
                render: function (data, type, row) {
                    if (!data) return '';
                    return `<img src="${data}" alt="${row.titulo || ''}" class="thumb">`;
                }
            },
            {
                data: null,
                render: function (data, type, row) {
                    return `
                        <button class="btn btn-edit btn-edit-item" data-id="${row.id_carrusel}">Editar</button>
                        <button class="btn btn-delete btn-delete-item" data-id="${row.id_carrusel}">Eliminar</button>
                    `;
                }
            }
        ],
        language: {
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ items por página"
        },
    });

    // ==================================================================
    // Variables del modal y helpers
    // ==================================================================
    const modal = $('#modal-carrusel');
    const form = $('#form-carrusel');
    const modalTitle = $('#modal-title');
    const closeModal = $('#close-modal');

    function openModal(title, data = {}) {
        modalTitle.text(title);
        $('#id_carrusel').val(data.id_carrusel || '');
        $('#titulo').val(data.titulo || '');
        $('#descripcion').val(data.descripcion || '');
        $('#imagen').val('');
        modal.show();
    }

    function closeModalFn() {
        modal.hide();
        form.trigger("reset");
    }

    // ==================================================================
    // Eventos CRUD
    // ==================================================================

    //  Crear nuevo
    $('#btn-crear-item').on('click', function () {
        openModal("Crear Item Carrusel");
    });

    //  Cerrar modal
    closeModal.on('click', function () {
        closeModalFn();
    });

    // Editar item
    $(document).on('click', '.btn-edit-item', function () {
        const id = $(this).data('id');
        $.get(`/api/v1/carrusel/${id}`, function (res) {
            if (res.success) {
                openModal("Editar Item Carrusel", res.data);
            } else {
                mostrarNotificacion("⚠️ No se pudo cargar el item", "warning");
            }
        }).fail(function (xhr) {
            mostrarNotificacion("❌ Error al obtener item: " + (xhr.responseText || xhr.statusText), "error");
        });
    });

    //  Eliminar item
    $(document).on('click', '.btn-delete-item', function () {
        const id = $(this).data('id');
        if (confirm("¿Seguro que deseas eliminar este item?")) {
            $.ajax({
                url: `/api/v1/carrusel/${id}`,
                type: "DELETE", // DELETE nativo
                headers: { "X-CSRFToken": csrfToken },
                success: function (res) {
                    if (res.success) {
                        tabla.ajax.reload();
                        mostrarNotificacion("✅ Item eliminado correctamente", "success");
                    } else {
                        mostrarNotificacion("⚠️ No se pudo eliminar el item", "warning");
                    }
                },
                error: function (xhr) {
                    mostrarNotificacion("❌ Error al eliminar: " + (xhr.responseText || xhr.statusText), "error");
                }
            });
        }
    });

    //  Guardar (crear o editar)
    form.on('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const id = $('#id_carrusel').val();
        const isEdit = Boolean(id);

        const url = isEdit ? `/api/v1/carrusel/${id}` : "/api/v1/carrusel/";
        const method = isEdit ? "PUT" : "POST";

        try {
            const res = await fetch(url, {
                method: method,
                headers: { 'X-CSRFToken': csrfToken },
                body: formData
            });

            let json;
            try {
                json = await res.json();
            } catch {
                throw new Error("La respuesta del servidor no es JSON válido");
            }

            if (res.ok && json.success) {
                tabla.ajax.reload();
                closeModalFn();
                mostrarNotificacion(
                    isEdit ? "✅ Item actualizado correctamente" : "✅ Item creado correctamente",
                    "success"
                );
            } else {
                mostrarNotificacion("⚠️ Error al guardar: " + (json.message || "Desconocido"), "warning");
            }
        } catch (err) {
            mostrarNotificacion("❌ Error en la petición: " + err.message, "error");
        }
    });
});
