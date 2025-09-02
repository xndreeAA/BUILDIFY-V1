document.addEventListener("DOMContentLoaded", () => {
    // Paso 1: Obtener el usuario actual
    fetch("/api/v1/usuarios/current_user", { credentials: "include" })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const idUsuario = data.data.id_usuario;
                cargarDatosUsuario(idUsuario); // Paso 2
            } else {
                document.getElementById("perfil-usuario").innerHTML =
                    "<p>Debes iniciar sesión.</p>";
            }
        })
        .catch(err => console.error("Error al obtener current_user:", err));
});

// Paso 2: Traer info completa del usuario
function cargarDatosUsuario(idUsuario) {
    fetch(`/api/v1/usuarios/${idUsuario}`, { credentials: "include" })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                renderFormularioUsuario(data.data); // Paso 3
            } else {
                document.getElementById("perfil-usuario").innerHTML =
                    "<p>No se encontró el usuario.</p>";
            }
        })
        .catch(err => console.error("Error al traer usuario:", err));
}

// Paso 3: Renderizar formulario con datos
function renderFormularioUsuario(usuario) {
    const contenedor = document.getElementById("perfil-usuario");

    contenedor.innerHTML = `
    <div class="container"> 
        <h2>Mi Perfil</h2>
        <form id="form-usuario">
            <label>Nombre:</label>
            <input type="text" name="nombre" value="${usuario.nombre}" />

            <label>Apellido:</label>
            <input type="text" name="apellido" value="${usuario.apellido}" />

            <label>Email:</label>
            <input type="email" name="email" value="${usuario.email}" />

            <label>Dirección:</label>
            <input type="text" name="direccion" value="${usuario.direccion}" />

            <label>Teléfono:</label>
            <input type="text" name="telefono" value="${usuario.telefono}" />

            <label>Contraseña:</label>
            <input type="password" name="password" value="${usuario.password}" />

            <input type="hidden" name="id_rol" value="${usuario.id_rol}" />

            <button type="submit">Guardar cambios</button>
        </form>
    </div>
    `;

    // Enviar formulario 
    document.getElementById("form-usuario").addEventListener("submit", (e) => {
        e.preventDefault();
        editarUsuario(usuario.id_usuario);
    });
}

// Paso 4: PUT para actualizar usuario
function editarUsuario(idUsuario) {
    const form = document.getElementById("form-usuario");
    const payload = {
        nombre: form.nombre.value,
        apellido: form.apellido.value,
        email: form.email.value,
        direccion: form.direccion.value,
        telefono: form.telefono.value,
        id_rol: form.id_rol.value,
        password: form.password.value
    };

    fetch(`/api/v1/usuarios/${idUsuario}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify(payload)
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Perfil actualizado correctamente ✅");
            } else {
                alert(data.error || "No se pudo actualizar el perfil");
            }
        })
        .catch(err => {
            console.error("Error al actualizar usuario:", err);
            alert("Ocurrió un error al intentar actualizar el perfil.");
        });
}
