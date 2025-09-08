function viewDeleteUsuario({ id_usuario }) {
    if (!id_usuario) return;

    const confirmado = confirm("¿Seguro que deseas eliminar este usuario?");
    if (!confirmado) return;

    fetch(`/api/v1/usuarios/${id_usuario}`, {
        method: 'DELETE',
        headers: { 'X-CSRFToken': csrfToken },
        credentials: 'include'
    })
    .then(res => res.json())
    .then(data => {
        alert("Usuario eliminado correctamente.");
        tablaUsuarios.ajax.reload(null, false);
    })
    .catch(err => alert("Error al eliminar usuario: " + err.message));
}
