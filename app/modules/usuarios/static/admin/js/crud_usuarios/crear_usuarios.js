const formNuevoUsuario = document.getElementById('form-nuevo-usuario');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

formNuevoUsuario.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(formNuevoUsuario);
    const payload = {
        nombre: formData.get("nombre"),
        apellido: formData.get("apellido"),
        email: formData.get("email"),
        telefono: formData.get("telefono"),
        direccion: formData.get("direccion"),
        id_rol: formData.get("id_rol"), 
        password: formData.get("password")
    };

    try {
        const res = await fetch('/api/v1/usuarios/', {   
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(payload)
        });

        const json = await res.json();

        if (res.ok && json.success) {
            alert('Usuario creado exitosamente con ID: ' + json.data.id_usuario);
            formNuevoUsuario.reset();

            if (typeof tablaUsuarios !== "undefined") {
                tablaUsuarios.ajax.reload(null, false);
            }
        } else {
            alert('Error al crear usuario: ' + (json.message || 'Desconocido'));
        }

    } catch (err) {
        console.error("Error en la petición:", err);
        alert('Error en la petición: ' + err.message);
    }
});
