const formNuevaCategoria = document.getElementById('form-nueva-categoria');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

formNuevaCategoria.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(formNuevaCategoria);
    const payload = { nombre: formData.get("nombre") };

    try {
        const res = await fetch('/api/v1/categorias/', {   
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(payload)
        });

        let json;
        try {
            json = await res.json();   
        } catch (parseErr) {
            throw new Error("La respuesta del servidor no es JSON válido");
        }

        if (res.ok && json.success) {
            const idCategoria = json.data.id_categoria;
            alert('Categoría creada exitosamente con ID: ' + idCategoria);
            formNuevaCategoria.reset();

            if (typeof tablaCategorias !== "undefined") {
                tablaCategorias.ajax.reload(null, false);
            } else {
                console.warn("tablaCategorias no está inicializada todavía.");
            }
        } else {
            alert('Error al crear categoría: ' + (json.message || 'Desconocido'));
        }

    } catch (err) {
        console.error("Error en la petición:", err);
        alert('Error en la petición: ' + err.message);
    }
});
